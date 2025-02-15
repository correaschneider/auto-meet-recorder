from services.notificators.linux_notifier import LinuxNotifier
from interfaces.notification_service import NotificationService

class NotificationFactory:
    @staticmethod
    def create() -> NotificationService:
        # No futuro, podemos adicionar lógica para escolher diferentes
        # implementações baseadas em configuração ou sistema operacional
        return LinuxNotifier()
