from abc import ABC, abstractmethod

class BaseAPI(ABC):

    name = "base"
    weight = 1.0

    @abstractmethod
    def scan(self, file_hash: str, file_path: str):
        pass
