import subprocess
from interfaces.notification_service import NotificationService

class LinuxNotifier(NotificationService):
    def send(self, title: str, message: str) -> None:
        subprocess.run(["notify-send", title, message])
