import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração global
OBS_HOST = os.getenv("OBS_HOST", "localhost")
OBS_PORT = int(os.getenv("OBS_PORT", "4455"))
OBS_PASSWORD = os.getenv("OBS_PASSWORD", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SAVE_DIR = os.path.expanduser(os.getenv("SAVE_DIR", "~/Videos/Meet"))
MEET_TITLE_FILE = f"{SAVE_DIR}/meet_title.txt"
BROWSER_API = os.getenv("BROWSER_API", "http://localhost:9222/json")

# Garante que o diretório de gravação existe
os.makedirs(SAVE_DIR, exist_ok=True)
