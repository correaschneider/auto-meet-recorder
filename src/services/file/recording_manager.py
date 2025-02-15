import os
import time
import datetime
from typing import Optional
from interfaces.notification_service import NotificationService
from services.file.meet_title_manager import MeetTitleManager
from services.file.directory_manager import DirectoryManager
from config.settings import SAVE_DIR

class RecordingManager:
    def __init__(self, notifier: NotificationService):
        self.notifier = notifier
        self.title_manager = MeetTitleManager()
        self.directory_manager = DirectoryManager()

    def get_last_recorded_file(self) -> Optional[str]:
        # Procura em todas as pastas de reunião pelo arquivo de vídeo mais recente
        files = [f for f in os.listdir(SAVE_DIR) if f.endswith(".mkv")]
        return max(files, key=lambda f: os.path.getctime(os.path.join(SAVE_DIR, f))) if files else None

    def rename_recording(self) -> Optional[str]:
        time.sleep(5)
        last_file = self.get_last_recorded_file()
        
        if last_file:
            meet_title = self.title_manager.get_saved_title()
            meet_dir = self.directory_manager.create_meet_directory(meet_title)
            new_path = self.directory_manager.get_video_path(meet_dir)
            old_path = os.path.join(SAVE_DIR, last_file)
            os.rename(old_path, new_path)
            
            self.title_manager.remove_title_file()
            self.notifier.send("Gravação movida", f"Arquivo movido para: {new_path}")
            return new_path
        return None 