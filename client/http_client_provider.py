from http_requests.client_interface import IClient
from http_requests.http_client import HttpClient

class HttpClientProvider:
    _instance: IClient = None
    @classmethod
    def get_client(cls):
        if cls._instance is None:
            cls._instance = HttpClient()
        return cls._instance