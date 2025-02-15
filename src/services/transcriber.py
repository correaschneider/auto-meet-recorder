import os
from openai import OpenAI
from config.settings import OPENAI_API_KEY
from interfaces.notification_service import NotificationService
from services.file.directory_manager import DirectoryManager
from typing import List, Optional, Dict, Any
from services.file.audio_splitter import AudioSplitter
import json
import concurrent.futures

class Transcriber:
    """Realiza a transcrição de áudio usando a API da OpenAI."""

    def __init__(self, notifier: NotificationService):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.notifier = notifier
        self.directory_manager = DirectoryManager()
        self.audio_splitter = AudioSplitter()

    def transcribe(self, audio_path: str) -> Optional[str]:
        if not os.path.exists(audio_path):
            return None

        meet_dir = os.path.dirname(audio_path)
        output_path = self.directory_manager.get_transcript_path(meet_dir)
        
        try:
            # Divide o áudio em partes menores
            audio_parts = self.audio_splitter.split_audio(audio_path)
            total_parts = len(audio_parts)
            accumulated_duration = 0.0  # Controle do tempo acumulado

            def process_transcription(args: tuple[int, str, float]) -> Dict[str, Any]:
                i, part_path, start_time = args
                self.notifier.send("Transcrevendo", f"Processando parte {i} de {total_parts}")
                
                with open(part_path, "rb") as audio_file:
                    result = self.client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        response_format="verbose_json",
                        timestamp_granularities=["segment"]
                    )
                    
                # Ajusta os timestamps de cada segmento
                result_dict = result.model_dump()
                for segment in result_dict.get('segments', []):
                    segment['start'] += start_time
                    segment['end'] += start_time
                
                # Remove o arquivo temporário da parte
                if part_path != audio_path:
                    os.remove(part_path)
                    
                return result_dict

            # Prepara os argumentos para cada parte, incluindo o tempo inicial
            parts_args = []
            current_start_time = 0.0
            
            for i, part_path in enumerate(audio_parts):
                parts_args.append((i+1, part_path, current_start_time))
                # Obtém a duração do arquivo de áudio atual
                duration = self.audio_splitter.get_audio_duration(part_path)
                current_start_time += duration

            # Processa as transcrições em paralelo mantendo a ordem
            with concurrent.futures.ThreadPoolExecutor() as executor:
                transcriptions = list(executor.map(process_transcription, parts_args))
            
            # Combina todas as transcrições
            full_transcription = json.dumps(transcriptions, ensure_ascii=False, indent=2)
            
            # Salva a transcrição completa
            with open(output_path, "w") as f:
                f.write(full_transcription)
            
            self.notifier.send("Transcrição concluída", f"Transcrição salva em: {output_path}")
            return output_path
            
        except Exception as e:
            self.notifier.send("Erro na transcrição", f"Erro: {str(e)}")
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>')
            print('e', e)
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>')
            return None
