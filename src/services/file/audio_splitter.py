import os
from pydub import AudioSegment
from typing import List, Tuple
from services.file.directory_manager import DirectoryManager
import concurrent.futures

class AudioSplitter:
    MAX_SIZE_MB = 24  # Deixando 1MB de margem para segurança

    def __init__(self):
        self.directory_manager = DirectoryManager()

    def split_audio(self, audio_path: str) -> List[str]:
        """
        Divide um arquivo de áudio em partes menores que 25MB.
        Retorna uma lista com os caminhos dos arquivos gerados.
        """
        if not os.path.exists(audio_path):
            return []

        # Carrega o arquivo de áudio
        audio = AudioSegment.from_mp3(audio_path)
        meet_dir = os.path.dirname(audio_path)
        
        # Calcula o tamanho do arquivo em MB
        file_size = os.path.getsize(audio_path) / (1024 * 1024)
        
        if file_size <= self.MAX_SIZE_MB:
            return [audio_path]

        # Calcula quantas partes serão necessárias
        num_parts = int(file_size / self.MAX_SIZE_MB) + 1

        # Calcula a duração de cada parte em milissegundos
        duration_ms = len(audio)
        part_duration = duration_ms // num_parts

        # Função auxiliar para processar cada parte do áudio
        def process_audio_part(args: Tuple[int, int, int]) -> str:
            i, start_ms, end_ms = args
            # Extrai a parte do áudio
            part = audio[start_ms:end_ms]
            
            # Salva a parte em um novo arquivo
            part_path = os.path.join(meet_dir, f"audio_part_{i+1}.mp3")
            part.export(part_path, format="mp3")
            
            # Verifica se o arquivo gerado está dentro do limite
            if os.path.getsize(part_path) / (1024 * 1024) > self.MAX_SIZE_MB:
                raise Exception(f"Parte {i+1} ainda está maior que {self.MAX_SIZE_MB}MB")
            
            return part_path

        # Prepara os argumentos para cada parte do áudio
        parts_args = [
            (i, 
             i * part_duration,
             (i + 1) * part_duration if i < num_parts - 1 else duration_ms)
            for i in range(num_parts)
        ]

        # Processa as partes em paralelo mantendo a ordem
        with concurrent.futures.ThreadPoolExecutor() as executor:
            split_files = list(executor.map(process_audio_part, parts_args))

        return split_files 

    def get_audio_duration(self, audio_path: str) -> float:
        """Retorna a duração do arquivo de áudio em segundos."""
        audio = AudioSegment.from_file(audio_path)
        return len(audio) / 1000.0  # Converte de milissegundos para segundos 