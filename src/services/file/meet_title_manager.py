import os
from config.settings import MEET_TITLE_FILE

class MeetTitleManager:
    @staticmethod
    def save_title(meet_title: str) -> None:
        with open(MEET_TITLE_FILE, "w") as f:
            f.write(meet_title)

    @staticmethod
    def get_saved_title() -> str:
        return open(MEET_TITLE_FILE).read().strip() if os.path.exists(MEET_TITLE_FILE) else "Reunião"

    @staticmethod
    def remove_title_file() -> None:
        if os.path.exists(MEET_TITLE_FILE):
            os.remove(MEET_TITLE_FILE) 