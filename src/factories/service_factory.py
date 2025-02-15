from interfaces.notification_service import NotificationService
from services.file.recording_manager import RecordingManager
from services.file.audio_extractor import AudioExtractor
from services.transcriber import Transcriber
from services.formatter import Formatter
from services.obs_controller import OBSController
from factories.notification_factory import NotificationFactory

class ServiceFactory:
    @staticmethod
    def create_notification_service() -> NotificationService:
        return NotificationFactory.create()

    @staticmethod
    def create_recording_manager(notifier: NotificationService) -> RecordingManager:
        return RecordingManager(notifier)

    @staticmethod
    def create_audio_extractor(notifier: NotificationService) -> AudioExtractor:
        return AudioExtractor(notifier)

    @staticmethod
    def create_transcriber(notifier: NotificationService) -> Transcriber:
        return Transcriber(notifier)

    @staticmethod
    def create_formatter(notifier: NotificationService) -> Formatter:
        return Formatter(notifier)

    @staticmethod
    def create_obs_controller() -> OBSController:
        return OBSController() 