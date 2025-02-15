from abc import ABC, abstractmethod

class NotificationService(ABC):
    @abstractmethod
    def send(self, title: str, message: str) -> None:
        pass
