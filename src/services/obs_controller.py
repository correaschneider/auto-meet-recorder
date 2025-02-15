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

    def create_scene(self, scene_name: str) -> None:
        self.client.create_scene(scene_name)

    def set_scene(self) -> None:
        scene_name = 'Meet'

        scene_collection = self.client.get_scene_list()
        
        meet_scene = next((scene for scene in scene_collection.scenes if scene.get('sceneName') == scene_name), None)
        if not meet_scene:
            self.client.create_scene(scene_name)
            self.set_scene()
            return None

        self.client.set_current_program_scene(scene_name)

    def start_recording(self) -> None:
        self.set_scene()
        self.client.start_record()

    def stop_recording(self) -> None:
        self.client.stop_record()
