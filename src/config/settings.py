import os
import sys
from dotenv import load_dotenv

def get_env_value(key: str, default: str = None) -> str:
    """
    Busca valor de variável de ambiente na seguinte ordem:
    1. Variáveis do sistema (.bashrc, etc)
    2. Arquivo .env
    3. Valor padrão
    """
    # Primeiro tenta pegar do ambiente do sistema
    value = os.environ.get(key)
    if value is not None:
        return value

    # Se não encontrou, tenta carregar do .env
    if getattr(sys, 'frozen', False):
        # Executando como executável
        env_path = os.path.join(sys._MEIPASS, '.env')
    else:
        # Executando em desenvolvimento
        env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.env')

    if os.path.exists(env_path):
        load_dotenv(env_path)
        value = os.environ.get(key)
        if value is not None:
            return value

    # Se ainda não encontrou, usa o valor padrão
    return default

# Configuração global usando a nova função
OBS_HOST = get_env_value("OBS_HOST", "localhost")
OBS_PORT = int(get_env_value("OBS_PORT", "4455"))
OBS_PASSWORD = get_env_value("OBS_PASSWORD", "")
OPENAI_API_KEY = get_env_value("OPENAI_API_KEY")
SAVE_DIR = os.path.expanduser(get_env_value("SAVE_DIR", "~/Videos/Meet"))
MEET_TITLE_FILE = f"{SAVE_DIR}/meet_title.txt"
BROWSER_API = get_env_value("BROWSER_API", "http://localhost:9222/json")

# Garante que o diretório de gravação existe
os.makedirs(SAVE_DIR, exist_ok=True)

# Imprime as configurações carregadas (útil para debug)
if os.environ.get("DEBUG"):
    print("\n🔧 Configurações carregadas:")
    print(f"OBS_HOST: {OBS_HOST}")
    print(f"OBS_PORT: {OBS_PORT}")
    print(f"OPENAI_API_KEY: {'Configurada' if OPENAI_API_KEY else 'Não configurada'}")
    print(f"SAVE_DIR: {SAVE_DIR}")
    print(f"BROWSER_API: {BROWSER_API}\n")
