from abc import ABC, abstractmethod
from typing import Any, Dict


class IClient(ABC):
    @abstractmethod
    def get(self, url: str, headers: Dict[str, str] = None) -> Any:
        pass

    @abstractmethod
    def patch(self, url: str, json: Dict[str, Any] = None, headers: Dict[str, str] = None) -> Any:
        pass

    @abstractmethod
    def post(self, url: str, json: Dict[str, Any] = None, headers: Dict[str, str] = None) -> Any:
        pass