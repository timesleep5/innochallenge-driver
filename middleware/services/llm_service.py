import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    def __init__(self):
        self.LLM_API_URL = os.getenv("LLM_API_URL")
        self.LLM_API_KEY = os.getenv("LLM_API_KEY")

        if not self.LLM_API_URL or not self.LLM_API_KEY:
            raise ValueError("LLM_API_URL oder LLM_API_KEY ist nicht gesetzt.")

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
                        """You are tasked with validating input strings that describe entities of type Truck, Trailer, or Driver.
                            Instructions:

                            Identify the Entity Type and ID:

                            Driver:
                            - ID starts with an uppercase letter D.
                            - For single-digit IDs, a leading zero is included (e.g., "D01").

                            Truck and Trailer:
                            - IDs are in uppercase letters TK for truck and TR for trailer.
                            - No leading zeros are present (e.g., TK5).

                            Determine the Active Status:
                            - Analyze the accompanying description to ascertain if the entity is active.
                            - A Driver may be inactive due to reasons like being sick.
                            - A Trailer may be inactive if it's broken.
                            - A Truck may be inactive due to maintenance or other issues.

                            Output Format:
                            Return a JSON object with the following fields:
                            - "id": The entity's ID as provided.
                            - "type": One of "truck-drivers", "trucks", or "trailers".
                            - "active": A boolean indicating the entity's active status (true or false).

                            If any information is missing or cannot be determined, use empty strings for those fields."""
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
            structured_response_str = result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
            try:
                structured_response = json.loads(structured_response_str)

                reduced_response = {
                    "id": structured_response.get("id", ""),
                    "type": structured_response.get("type", ""),
                    "active": structured_response.get("active", False)
                }
                return reduced_response
            except json.JSONDecodeError:
                print("Fehler beim Parsen der LLM-Antwort als JSON.")
                return {"error": "Die Antwort des LLM konnte nicht als JSON geparst werden.", "raw_response": structured_response_str}
        else:
            print(f"Fehler bei der Anfrage: {response.status_code}, {response.text}")
            return {"error": f"Fehler bei der Kommunikation mit dem LLM: {response.text}"}