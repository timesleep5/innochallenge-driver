from client.components.transcriptors.interface import ITranscriptor
import requests
from requests import HTTPError


class Transcriptor(ITranscriptor):
    def __init__(self, transcription_service_url: str):
        self.transcription_service_url = transcription_service_url

    def transcribe(self, file_path: str) -> str:
        try:
            url = f"{self.transcription_service_url}?filepath={file_path}"
            response = requests.post(url)
            response.raise_for_status()
            return response.json().get('transcription', '')

        except FileNotFoundError:
            raise FileNotFoundError(f"The file at {file_path} was not found.")
        except HTTPError as e:
            raise HTTPError(f"Failed to transcribe the file: {e}")