import os
import tempfile
import wave
from threading import Thread

# import pyaudio
import requests
from dotenv import load_dotenv
from fastapi import UploadFile

load_dotenv()


class SpeechService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SpeechService, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "is_recording"):
            self.AZURE_API_URL = os.getenv("AZURE_API_URL")
            self.AZURE_API_KEY = os.getenv("AZURE_API_KEY")

            if not self.AZURE_API_URL or not self.AZURE_API_KEY:
                raise ValueError("AZURE_API_URL oder AZURE_API_KEY ist nicht gesetzt.")

            self.is_recording = False
            self.recognized_text = []
            self.audio_stream = None
            self.frames = []

    # def start_recording(self, sample_rate=16000, channels=1, chunk_size=1024):
    #     if self.is_recording:
    #         return {"message": "Die Aufnahme läuft bereits."}
    #
    #     self.is_recording = True
    #     self.frames = []
    #     print("Die Sprachaufnahme wurde gestartet.")
    #
    #     p = pyaudio.PyAudio()
    #     self.audio_stream = p.open(format=pyaudio.paInt16,
    #                                channels=channels,
    #                                rate=sample_rate,
    #                                input=True,
    #                                frames_per_buffer=chunk_size)
    #
    #     def record():
    #         while self.is_recording:
    #             data = self.audio_stream.read(chunk_size)
    #             self.frames.append(data)
    #
    #     self.recording_thread = Thread(target=record)
    #     self.recording_thread.start()
    #
    #     return {"message": "Die Sprachaufnahme wurde gestartet."}
    #
    # def stop_recording(self):
    #     if not self.is_recording:
    #         return {"message": "Es läuft keine Aufnahme, die beendet werden kann."}
    #
    #     self.is_recording = False
    #     self.recording_thread.join()
    #     self.audio_stream.stop_stream()
    #     self.audio_stream.close()
    #     print("Die Sprachaufnahme wurde beendet.")
    #
    #     with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
    #         wf = wave.open(tmpfile.name, 'wb')
    #         wf.setnchannels(1)
    #         wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
    #         wf.setframerate(16000)
    #         wf.writeframes(b''.join(self.frames))
    #         wf.close()
    #         tmpfile_path = tmpfile.name
    #
    #     print(f"Audio gespeichert unter: {tmpfile_path} ({os.path.getsize(tmpfile_path)} Bytes)")
    #     return tmpfile_path
    #
    # def save_recording(self):
    #     tmpfile_path = self.stop_recording()
    #
    #     data_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data"))
    #     if not os.path.exists(data_directory):
    #         os.makedirs(data_directory)
    #
    #     file_name = os.path.basename(tmpfile_path)
    #     target_path = os.path.join(data_directory, file_name)
    #
    #     os.rename(tmpfile_path, target_path)
    #
    #     return {"message": "Die Sprachaufnahme wurde beendet und gespeichert.", "file_path": target_path}

    def transcribe_recording(self, file: UploadFile):
        if file.content_type != "audio/wav":
            return {"error": "Nur WAV-Dateien werden unterstützt."}

        transcribed_text = self.send_to_azure(file.file)
        if transcribed_text:
            self.recognized_text = transcribed_text
            return {"message": "Die Datei wurde geladen und verarbeitet.", "transcription": transcribed_text}
        else:
            return {"error": "Die Datei konnte nicht transkribiert werden."}

    def send_to_azure(self, audio_file):
        headers = {
            "api-key": self.AZURE_API_KEY,
        }
        files = {
            "file": ("recording.wav", audio_file, "audio/wav"),
        }
        response = requests.post(self.AZURE_API_URL, headers=headers, files=files)

        if response.status_code == 200:
            result = response.json()
            return result.get("text", "")
        else:
            print(f"Fehler bei der Anfrage: {response.status_code}, {response.text}")
            return ""

    def get_results(self):
        """Gibt die erkannten Texte zurück."""
        return {"recognized_text": self.recognized_text}
