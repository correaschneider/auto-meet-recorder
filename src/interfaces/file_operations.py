from abc import ABC, abstractmethod
from typing import Optional

class FileReader(ABC):
    @abstractmethod
    def read_file(self, path: str) -> str:
        pass

class FileWriter(ABC):
    @abstractmethod
    def write_file(self, path: str, content: str) -> None:
        pass

class FileRenamer(ABC):
    @abstractmethod
    def rename_file(self, old_path: str, new_path: str) -> None:
        pass

class FileRemover(ABC):
    @abstractmethod
    def remove_file(self, path: str) -> None:
        pass
