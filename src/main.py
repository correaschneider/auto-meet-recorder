import time
from services.meet_detector import MeetDetector
from factories.service_factory import ServiceFactory
from services.system_validator import SystemValidator
import sys

class MeetMonitor:
    def __init__(self, notifier, recording_manager, audio_extractor, transcriber, formatter, obs):
        self.notifier = notifier
        self.recording_manager = recording_manager
        self.audio_extractor = audio_extractor
        self.transcriber = transcriber
        self.formatter = formatter
        self.obs = obs

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

def main(notified: bool = False):
    # Valida os requisitos do sistema
    is_valid, errors = SystemValidator.validate_all()
    if not is_valid:
        if not notified:
            notifier = ServiceFactory.create_notification_service()
            title = "\n🚫 Erro: O sistema não atende aos requisitos necessários:"
            print(title)
            messages = []
            for error in errors:
                messages.append(error)
            print(error)
            footer = "\nPor favor, corrija os erros acima e tente novamente.\nVerifique no README como instalar os requisitos necessários."
            messages.append(footer)
            print(footer)
            notifier.send_error(title, "\n".join(messages))
        time.sleep(3)
        main(True)
        return None

    print("✅ Todas as validações passaram! Iniciando o monitor...")
    
    # Cria as instâncias dos serviços
    notifier = ServiceFactory.create_notification_service()
    recording_manager = ServiceFactory.create_recording_manager(notifier)
    audio_extractor = ServiceFactory.create_audio_extractor(notifier)
    transcriber = ServiceFactory.create_transcriber(notifier)
    formatter = ServiceFactory.create_formatter(notifier)
    obs = ServiceFactory.create_obs_controller()

    # Inicia o monitor
    monitor = MeetMonitor(
        notifier=notifier,
        recording_manager=recording_manager,
        audio_extractor=audio_extractor,
        transcriber=transcriber,
        formatter=formatter,
        obs=obs
    )
    
    monitor.run()

if __name__ == "__main__":
    main(False)
