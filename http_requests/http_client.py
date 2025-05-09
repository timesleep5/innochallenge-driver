from typing import Any, Dict

import requests
from requests import Response

from http_requests.client_interface import IClient


class HttpClient(IClient):
    def get(self, url: str, headers: Dict[str, str] = None) -> Response:
        return requests.get(url=url, headers=headers)

    def patch(self, url: str, json: Dict[str, Any] = None, headers: Dict[str, str] = None) -> Response:
        return requests.patch(url=url, json=json, headers=headers)

    def post(self, url: str, json: Dict[str, Any] = None, headers: Dict[str, str] = None) -> Response:
        return requests.post(url=url, json=json, headers=headers)
