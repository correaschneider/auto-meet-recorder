import time
from services.meet_detector import MeetDetector
from factories.service_factory import ServiceFactory

class MeetMonitor:
    def __init__(self):
        self.factory = ServiceFactory()
        self.notifier = self.factory.create_notification_service()
        self.obs = self.factory.create_obs_controller()
        self.recording_manager = self.factory.create_recording_manager(self.notifier)
        self.audio_extractor = self.factory.create_audio_extractor(self.notifier)
        self.transcriber = self.factory.create_transcriber(self.notifier)
        self.formatter = self.factory.create_formatter(self.notifier)

    def run(self):
        while True:
            meet_title = MeetDetector.get_meet_title()

            if meet_title and not self.obs.is_recording():
                self.notifier.send("Gravação iniciada", f"Gravando: {meet_title}")
                self.recording_manager.title_manager.save_title(meet_title)
                self.obs.start_recording()

            if not meet_title and self.obs.is_recording():
                self.notifier.send("Gravação finalizada", "Processando gravação...")
                self.obs.stop_recording()

                video_path = self.recording_manager.rename_recording()
                if not video_path:
                    self.notifier.send("Erro", "Não foi possível encontrar o arquivo de vídeo")
            
                audio_path = self.audio_extractor.extract_from_video(video_path)
                if not audio_path:
                    self.notifier.send("Erro", "Não foi possível extrair o áudio do vídeo")
            
                transcript_path = self.transcriber.transcribe(audio_path)
                if not transcript_path:
                    self.notifier.send("Erro", "Não foi possível transcrever o áudio")
                        
                formatted_path = self.formatter.format_transcription(transcript_path)
                if not formatted_path:
                    self.notifier.send("Erro", "Não foi possível formatar a transcrição")


            time.sleep(5)

if __name__ == "__main__":
    monitor = MeetMonitor()
    monitor.run()
