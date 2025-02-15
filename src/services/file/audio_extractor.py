import os
import subprocess
from typing import Optional
from interfaces.notification_service import NotificationService
from services.file.directory_manager import DirectoryManager

class AudioExtractor:
    def __init__(self, notifier: NotificationService):
        self.notifier = notifier
        self.directory_manager = DirectoryManager()

    def extract_from_video(self, video_path: str) -> Optional[str]:
        if os.path.exists(video_path):
            meet_dir = os.path.dirname(video_path)
            output_path = self.directory_manager.get_audio_path(meet_dir)
            
            subprocess.run(["ffmpeg", "-y", "-i", video_path, "-q:a", "0", "-map", "a", output_path])
            self.notifier.send("Áudio extraído", f"Áudio salvo em: {output_path}")
            return output_path
        return None
