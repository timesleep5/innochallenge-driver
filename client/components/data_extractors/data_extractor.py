from client.components.data_extractors.interface import IDataExtractor
import requests
from requests import HTTPError


class DataExtractor(IDataExtractor):
    def __init__(self, llm_service_url: str):
        self.llm_service_url = llm_service_url

    def extract_data(self, data: str) -> dict:
        if not data.strip():
            raise ValueError("The transcription text is empty.")

        try:
            response = requests.post(self.llm_service_url, json={"transcription": data})
            response.raise_for_status()
            return response.json()

        except HTTPError as e:
            raise HTTPError(f"Failed to extract data from LLM service: {e}")
