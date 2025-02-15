import obsws_python as obs
from config.settings import OBS_HOST, OBS_PORT, OBS_PASSWORD

class OBSController:
    def __init__(self):
        self.client = obs.ReqClient(
            host=OBS_HOST,
            port=OBS_PORT,
            password=OBS_PASSWORD,
            timeout=3
        )

    def is_recording(self) -> bool:
        return hasattr(self.client, 'get_record_status') and self.client.get_record_status().output_active

    def start_recording(self) -> None:
        self.client.start_record()

    def stop_recording(self) -> None:
        self.client.stop_record()
