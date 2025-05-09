from client.components.data_senders.interface import IDataSender
from client.config.config import backend_url
from http_requests.client_interface import IClient
from http_requests.http_client_provider import HttpClientProvider


class DataSender(IDataSender):
    def __init__(self):
        self.base_url = backend_url
        self.client: IClient = HttpClientProvider.get_client()

    def send_data(self, data: dict) -> int:
        url = self._build_url(data)
        payload = self._build_payload(data)
        headers = self._build_headers()

        response = self.client.patch(url=url, json=payload, headers=headers)
        return response.status_code

    def _build_url(self, data: dict) -> str:
        object_id = data.get('id')
        object_type = data.get('type')
        url = f'{self.base_url}/{object_type}/{object_id}'
        return url

    def _build_payload(self, data: dict) -> dict:
        active = data.get('active')
        payload = {
            'active': active,
        }
        return payload

    def _build_headers(self) -> dict:
        headers = {
            'Content-Type': 'application/json'
        }
        return headers
