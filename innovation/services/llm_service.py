import requests
import json  # Importieren, um den JSON-String zu parsen

class LLMService:
    def __init__(self):
        # LLM API-Konfiguration
        self.LLM_API_URL = "https://innovationazur3213328481.openai.azure.com/openai/deployments/gpt-4.1/chat/completions?api-version=2025-01-01-preview"
        self.LLM_API_KEY = "G9cw5SDql7Tw5IMTnC8xv0e55RBOjA6D6xXUInhtm5IrcFe7qkaFJQQJ99BEACfhMk5XJ3w3AAAAACOGUNNO"

    def send_to_llm(self, text):
        """Sendet den Text an das LLM und gibt die strukturierte Antwort zurück."""
        headers = {
            "Authorization": f"Bearer {self.LLM_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Du bist ein Assistent, der wichtige Informationen aus Texten extrahiert. "
                        "Extrahiere die folgenden Informationen aus dem Text und gib sie in einem JSON-Format zurück: "
                        "1. Personalnummer, 2. Fahrtennummer, 3. Lastzugnummer, 4. Trailernummer, "
                        "5. Name des Anrufers (falls genannt), 6. Grund für den Anruf. "
                        "Falls eine Information nicht vorhanden ist, lasse das Feld leer."
                    )
                },
                {"role": "user", "content": text}
            ],
            "model": "gpt-4.1",
            "max_tokens": 500,
            "temperature": 0.7
        }
        response = requests.post(self.LLM_API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            result = response.json()
            # Extrahiere die Antwort aus der LLM-Antwort
            structured_response_str = result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
            try:
                # Versuche, den JSON-String in ein echtes JSON-Objekt zu konvertieren
                structured_response = json.loads(structured_response_str)
                return {"structured_response": structured_response}
            except json.JSONDecodeError:
                # Falls die Antwort kein gültiges JSON ist, gebe den ursprünglichen String zurück
                print("Fehler beim Parsen der LLM-Antwort als JSON.")
                return {"error": "Die Antwort des LLM konnte nicht als JSON geparst werden.", "raw_response": structured_response_str}
        else:
            print(f"Fehler bei der Anfrage: {response.status_code}, {response.text}")
            return {"error": f"Fehler bei der Kommunikation mit dem LLM: {response.text}"}