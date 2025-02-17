import os
from pathlib import Path
from config.settings import SAVE_DIR

class DirectoryManager:
    @staticmethod
    def create_meet_directory(meet_title: str) -> str:
        """
        Cria e retorna o diretório específico para a reunião.
        Se o diretório já existir, adiciona um número incremental.
        """
        base_dir = meet_title.replace(' ', '_')
        meet_dir = os.path.join(SAVE_DIR, base_dir)
        
        # Se o diretório já existe, adiciona um número incremental
        counter = 1
        while os.path.exists(meet_dir):
            meet_dir = os.path.join(SAVE_DIR, f"{base_dir}_{counter}")
            counter += 1
        
        os.makedirs(meet_dir, exist_ok=True)
        return meet_dir

    @staticmethod
    def get_video_path(meet_dir: str) -> str:
        return os.path.join(meet_dir, "video.mkv")

    @staticmethod
    def get_audio_path(meet_dir: str) -> str:
        return os.path.join(meet_dir, "audio.mp3")

    @staticmethod
    def get_transcript_path(meet_dir: str) -> str:
        return os.path.join(meet_dir, "transcript.json")

    @staticmethod
    def get_formatted_transcript_path(meet_dir: str) -> str:
        return os.path.join(meet_dir, "formatted_transcript.txt") 