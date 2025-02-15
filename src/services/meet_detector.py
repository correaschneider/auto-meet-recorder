import requests
from typing import Optional
from config.settings import BROWSER_API

class MeetDetector:
    @staticmethod
    def get_meet_title() -> Optional[str]:
        try:
            response = requests.get(BROWSER_API)
            tabs = response.json()

            for tab in tabs:
                if "meet.google.com" in tab.get("url", "") and "Meet:" in tab.get("title", ""):
                    return tab.get("title", "")
            return None
        except requests.exceptions.RequestException:
            return None
