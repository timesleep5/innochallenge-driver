from abc import ABC, abstractmethod
from typing import Any, Dict

from requests import Response


class IClient(ABC):
    @abstractmethod
    def get(self, url: str, headers: Dict[str, str] = None) -> Response:
        pass

    @abstractmethod
    def patch(self, url: str, json: Dict[str, Any] = None, headers: Dict[str, str] = None) -> Response:
        pass

    @abstractmethod
    def post(self, url: str, json: Dict[str, Any] = None, headers: Dict[str, str] = None) -> Response:
        pass
