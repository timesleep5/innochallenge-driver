import requests
import pyaudio
import wave
import tempfile
import os
from threading import Thread

class SpeechService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SpeechService, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "is_recording"):  # Verhindert erneute Initialisierung
            # Azure API-Konfiguration
            self.AZURE_API_URL = "https://innovationazur3213328481.openai.azure.com/openai/deployments/gpt-4o-transcribe/audio/transcriptions?api-version=2025-03-01-preview"
            self.AZURE_API_KEY = "G9cw5SDql7Tw5IMTnC8xv0e55RBOjA6D6xXUInhtm5IrcFe7qkaFJQQJ99BEACfhMk5XJ3w3AAAAACOGUNNO"

            # Globale Variablen
            self.is_recording = False
            self.recognized_text = []
            self.audio_stream = None
            self.frames = []

    def start_recording(self, sample_rate=16000, channels=1, chunk_size=1024):
        """Startet die Sprachaufnahme."""
        if self.is_recording:
            return {"message": "Die Aufnahme läuft bereits."}

        self.is_recording = True
        self.frames = []
        print("Die Sprachaufnahme wurde gestartet.")

        # PyAudio initialisieren
        p = pyaudio.PyAudio()
        self.audio_stream = p.open(format=pyaudio.paInt16,
                                   channels=channels,
                                   rate=sample_rate,
                                   input=True,
                                   frames_per_buffer=chunk_size)

        def record():
            while self.is_recording:
                data = self.audio_stream.read(chunk_size)
                self.frames.append(data)

        # Aufnahme in einem separaten Thread starten
        self.recording_thread = Thread(target=record)
        self.recording_thread.start()

        return {"message": "Die Sprachaufnahme wurde gestartet."}

    def stop_recording(self):
        """Beendet die Sprachaufnahme, speichert die Datei und sendet sie an Azure."""
        if not self.is_recording:
            return {"message": "Es läuft keine Aufnahme, die beendet werden kann."}

        self.is_recording = False
        self.recording_thread.join()
        self.audio_stream.stop_stream()
        self.audio_stream.close()
        print("Die Sprachaufnahme wurde beendet.")

        # Temporäre Datei speichern
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
            wf = wave.open(tmpfile.name, 'wb')
            wf.setnchannels(1)
            wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
            wf.setframerate(16000)
            wf.writeframes(b''.join(self.frames))
            wf.close()
            tmpfile_path = tmpfile.name

        print(f"Audio gespeichert unter: {tmpfile_path} ({os.path.getsize(tmpfile_path)} Bytes)")

        # Datei an Azure senden
        transcribed_text = self.send_to_azure(tmpfile_path)
        if transcribed_text:
            self.recognized_text.append(transcribed_text)
            print(f"Erkannte Sprache: {transcribed_text}")

        return {"message": "Die Sprachaufnahme wurde beendet.", "file_path": tmpfile_path, "transcription": transcribed_text}

    def send_to_azure(self, audio_file_path):
        """Sendet die Audio-Datei an den Azure-Service und gibt die Transkription zurück."""
        headers = {
            "api-key": self.AZURE_API_KEY,
        }
        with open(audio_file_path, "rb") as audio_file:
            files = {
                "file": ("recording.wav", audio_file, "audio/wav"),
            }
            response = requests.post(self.AZURE_API_URL, headers=headers, files=files)

        # Temporäre Datei löschen
        # os.remove(audio_file_path)

        if response.status_code == 200:
            result = response.json()
            return result.get("text", "")
        else:
            print(f"Fehler bei der Anfrage: {response.status_code}, {response.text}")
            return ""

    def get_results(self):
        """Gibt die erkannten Texte zurück."""
        return {"recognized_text": self.recognized_text}