import os
import time
import subprocess
from datetime import datetime
import obsws_python as obs
import requests
from openai import OpenAI

# Configuração global
OBS_HOST = "localhost"
OBS_PORT = 4455
OBS_PASSWORD = ""  # Defina se houver senha
OPENAI_API_KEY = "SUA_CHAVE_AQUI"
SAVE_DIR = os.path.expanduser("~/Videos/Meet")
MEET_TITLE_FILE = f"{SAVE_DIR}/meet_title.txt"

# Garante que o diretório de gravação existe
os.makedirs(SAVE_DIR, exist_ok=True)


class Notifier:
    """Responsável por exibir notificações no sistema."""
    
    @staticmethod
    def send(title, message):
        subprocess.run(["notify-send", title, message])


class MeetDetector:
    """Responsável por detectar reuniões ativas no Google Meet."""

    @staticmethod
    def get_meet_title():
        try:
            response = requests.get("http://localhost:9222/json")
            tabs = response.json()

            for tab in tabs:
                if "meet.google.com" in tab.get("url", "") and "Meet:" in tab.get("title", ""):
                    return tab.get("title", "")
        except requests.exceptions.RequestException:
            return None


class OBSController:
    """Gerencia a gravação do OBS Studio via WebSocket."""

    def __init__(self):
        self.client = obs.ReqClient(host=OBS_HOST, port=OBS_PORT, password=OBS_PASSWORD, timeout=3)

    def is_recording(self):
        return hasattr(self.client, 'get_record_status') and self.client.get_record_status().output_active

    def start_recording(self):
        self.client.start_record()

    def stop_recording(self):
        self.client.stop_record()


class FileManager:
    """Gerencia operações de arquivos como salvar títulos, renomear gravações e extrair áudio."""

    @staticmethod
    def save_meet_title(meet_title):
        with open(MEET_TITLE_FILE, "w") as f:
            f.write(meet_title)

    @staticmethod
    def get_saved_meet_title():
        return open(MEET_TITLE_FILE).read() if os.path.exists(MEET_TITLE_FILE) else "Reunião"

    @staticmethod
    def get_last_recorded_file():
        files = [f for f in os.listdir(SAVE_DIR) if f.endswith(".mkv")]
        return max(files, key=lambda f: os.path.getctime(os.path.join(SAVE_DIR, f))) if files else None

    @staticmethod
    def rename_recording():
        time.sleep(5)
        last_file = FileManager.get_last_recorded_file()
        if last_file:
            meet_title = FileManager.get_saved_meet_title()
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            new_name = f"{meet_title.replace(' ', '_')}_{timestamp}.mkv"
            old_path = os.path.join(SAVE_DIR, last_file)
            new_path = os.path.join(SAVE_DIR, new_name)
            os.rename(old_path, new_path)
            os.remove(MEET_TITLE_FILE)
            Notifier.send("Gravação renomeada", f"Arquivo renomeado para: {new_name}")
            return new_name
        return None

    @staticmethod
    def extract_audio():
        last_file = FileManager.get_last_recorded_file()
        if last_file:
            input_path = os.path.join(SAVE_DIR, last_file)
            output_path = os.path.join(SAVE_DIR, last_file.replace('.mkv', '.mp3'))
            subprocess.run(["ffmpeg", "-i", input_path, "-q:a", "0", "-map", "a", output_path])
            Notifier.send("Áudio extraído", f"Áudio salvo em: {output_path}")
            return output_path
        return None


class Transcriber:
    """Realiza a transcrição de áudio usando a API da OpenAI."""

    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def transcribe(self):
        last_file = FileManager.get_last_recorded_file()
        if last_file:
            audio_path = os.path.join(SAVE_DIR, last_file.replace('.mkv', '.mp3'))
            transcript_path = os.path.join(SAVE_DIR, last_file.replace('.mkv', '.json'))

            with open(audio_path, "rb") as audio_file:
                response = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="verbose_json",
                    timestamp_granularities=["segment"]
                )

            with open(transcript_path, "w") as f:
                f.write(response.model_dump_json(indent=2))  # Salvar JSON formatado
            
            Notifier.send("Transcrição concluída", f"Transcrição salva em: {transcript_path}")
            return transcript_path
        return None


class Formatter:
    """Organiza a transcrição em tópicos usando a OpenAI."""

    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def format_transcription(self):
        last_file = FileManager.get_last_recorded_file()
        if last_file:
            transcript_path = os.path.join(SAVE_DIR, last_file.replace('.mkv', '.json'))
            formatted_path = os.path.join(SAVE_DIR, last_file.replace('.mkv', '_formatted.txt'))

            with open(transcript_path, "r") as f:
                transcription_data = f.read()

            prompt = f"""
            Organize o seguinte texto em tópicos bem estruturados, destacando os principais pontos discutidos, adicioando a minutagem de cada tópico:

            {transcription_data}

            Retorne apenas o texto formatado, sem explicações adicionais.
            """

            response = self.client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[{"role": "system", "content": "Você é um assistente que organiza transcrições de reuniões."},
                          {"role": "user", "content": prompt}],
                temperature=0.3
            )

            formatted_text = response.choices[0].message.content

            with open(formatted_path, "w") as f:
                f.write(formatted_text)

            subprocess.run(["xdg-open", formatted_path])
            Notifier.send("Transcrição formatada", f"Arquivo salvo em: {formatted_path}")


class MeetMonitor:
    """Gerencia o fluxo de detecção e gravação do Google Meet."""

    def __init__(self):
        self.obs = OBSController()
        self.transcriber = Transcriber()
        self.formatter = Formatter()

    def run(self):
        while True:
            meet_title = MeetDetector.get_meet_title()

            if meet_title and not self.obs.is_recording():
                Notifier.send("Gravação iniciada", f"Gravando: {meet_title}")
                FileManager.save_meet_title(meet_title)
                self.obs.start_recording()

            if not meet_title and self.obs.is_recording():
                Notifier.send("Gravação finalizada", "Processando gravação...")
                self.obs.stop_recording()
                FileManager.rename_recording()
                FileManager.extract_audio()
                self.transcriber.transcribe()
                self.formatter.format_transcription()

            time.sleep(5)


if __name__ == "__main__":
    monitor = MeetMonitor()
    monitor.run()