import os
import time
import subprocess
from datetime import datetime
from config.settings import SAVE_DIR, MEET_TITLE_FILE
from interfaces.notification_service import NotificationService

class FileManager:
    """Gerencia operações de arquivos como salvar títulos, renomear gravações e extrair áudio."""

    def __init__(self, notifier: NotificationService):
        self.notifier = notifier

    def save_meet_title(meet_title):
        with open(MEET_TITLE_FILE, "w") as f:
            f.write(meet_title)

    def get_saved_meet_title():
        return open(MEET_TITLE_FILE).read() if os.path.exists(MEET_TITLE_FILE) else "Reunião"

    def get_last_recorded_file():
        files = [f for f in os.listdir(SAVE_DIR) if f.endswith(".mkv")]
        return max(files, key=lambda f: os.path.getctime(os.path.join(SAVE_DIR, f))) if files else None

    def rename_recording(self):
        time.sleep(5)
        last_file = FileManager.get_last_recorded_file()
        if last_file:
            meet_title = FileManager.get_saved_meet_title()
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            new_name = f"{meet_title.replace(' ', '_')}_{timestamp}.mkv"
            old_path = os.path.join(SAVE_DIR, last_file)
            new_path = os.path.join(SAVE_DIR, new_name)
            os.rename(old_path, new_path)
            os.remove(MEET_TITLE_FILE)
            self.notifier.send("Gravação renomeada", f"Arquivo renomeado para: {new_name}")
            return new_name
        return None

    def extract_audio(self):
        last_file = FileManager.get_last_recorded_file()
        if last_file:
            input_path = os.path.join(SAVE_DIR, last_file)
            output_path = os.path.join(SAVE_DIR, last_file.replace('.mkv', '.mp3'))
            subprocess.run(["ffmpeg", "-i", input_path, "-q:a", "0", "-map", "a", output_path])
            self.notifier.send("Áudio extraído", f"Áudio salvo em: {output_path}")
            return output_path
        return None
