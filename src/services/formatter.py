import os
import subprocess
import json
from openai import OpenAI
from config.settings import OPENAI_API_KEY, SAVE_DIR
from services.file_manager import FileManager
from interfaces.notification_service import NotificationService
from services.file.directory_manager import DirectoryManager
from typing import Optional
import concurrent.futures

class Formatter:
    """Organiza a transcrição em tópicos usando a OpenAI."""

    def __init__(self, notifier: NotificationService):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.notifier = notifier
        self.directory_manager = DirectoryManager()

    def format_transcription(self, transcript_path: str) -> Optional[str]:
        if os.path.exists(transcript_path):
            meet_dir = os.path.dirname(transcript_path)
            output_path = self.directory_manager.get_formatted_transcript_path(meet_dir)

            with open(transcript_path, "r") as f:
                transcription_data = json.loads(f.read())

            total_segments = len(transcription_data)

            def process_segment(args: tuple[int, dict]) -> str:
                index, segment = args
                self.notifier.send("Formatando", f"Processando segmento {index + 1} de {total_segments}")
                
                fragment = {
                    "text": segment["text"],
                    "segments": [
                        {
                            "start": segment["start"],
                            "end": segment["end"],
                            "text": segment["text"]
                        }
                        for segment in segment["segments"]
                    ]
                }

                prompt = f"""
                Segue uma parte de uma transcrição de reunião. Organize o texto em tópicos bem estruturados, 
                destacando os principais pontos discutidos. Mantenha a minutagem fornecida no início de cada tópico relevante:

                {fragment}

                Documentação do JSON
                fragment.text # texto completo
                fragment.segments # lista de segmentos com o tempo de início, fim e texto de cada segmento
                fragment.segments.start # tempo de início de cada segmento
                fragment.segments.end # tempo de fim de cada segmento
                fragment.segments.text # texto de cada segmento

                Retorne apenas o texto formatado, sem explicações adicionais.
                """

                response = self.client.chat.completions.create(
                    model="gpt-4-turbo",
                    messages=[
                        {"role": "system", "content": "Você é um assistente que organiza transcrições de reuniões."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3
                )

                return response.choices[0].message.content

            # Prepara os argumentos para cada segmento
            segment_args = [(i, segment) for i, segment in enumerate(transcription_data)]

            # Processa as formatações em paralelo mantendo a ordem
            with concurrent.futures.ThreadPoolExecutor() as executor:
                formatted_segments = list(executor.map(process_segment, segment_args))

            # Junta todos os segmentos formatados
            formatted_text = "\n\n".join(formatted_segments)

            with open(output_path, "w") as f:
                f.write(formatted_text)

            subprocess.run(["xdg-open", output_path])
            self.notifier.send("Formatação concluída", f"Texto formatado salvo em: {output_path}")
            return output_path
        return None
