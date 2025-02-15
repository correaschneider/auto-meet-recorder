import os
import requests
from typing import Tuple, List
from config.settings import BROWSER_API, OPENAI_API_KEY, SAVE_DIR, OBS_HOST, OBS_PORT
from obsws_python import ReqClient
from obsws_python.error import OBSSDKError

class SystemValidator:
    """Valida os requisitos do sistema antes de iniciar o script."""

    @staticmethod
    def validate_all() -> Tuple[bool, List[str]]:
        """
        Executa todas as validações necessárias.
        Retorna uma tupla com (sucesso, lista_de_erros).
        """
        errors = []

        # Valida diretório de salvamento
        if not os.path.exists(SAVE_DIR):
            try:
                os.makedirs(SAVE_DIR)
            except Exception as e:
                errors.append(f"❌ Não foi possível criar o diretório {SAVE_DIR}: {str(e)}")

        # Valida API Key da OpenAI
        if not OPENAI_API_KEY:
            errors.append("❌ OPENAI_API_KEY não configurada")

        # Valida conexão com o navegador
        try:
            response = requests.get(BROWSER_API)
            if response.status_code != 200:
                errors.append("❌ Não foi possível conectar ao navegador. Verifique se está rodando com --remote-debugging-port=9222")
        except requests.exceptions.RequestException:
            errors.append(f"❌ Navegador não está acessível na url {BROWSER_API}")

        # Valida conexão com OBS
        try:
            client = ReqClient(host=OBS_HOST, port=OBS_PORT)
            client.get_version()
        except OBSSDKError as e:
            errors.append(f"❌ Não foi possível conectar ao OBS: {str(e)}")
        except Exception as e:
            errors.append(f"❌ Erro ao tentar conectar com OBS: {str(e)}")

        # Valida FFmpeg
        try:
            result = os.system("ffmpeg -version > /dev/null 2>&1")
            if result != 0:
                errors.append("❌ FFmpeg não está instalado")
        except Exception:
            errors.append("❌ Não foi possível verificar a instalação do FFmpeg")

        return (len(errors) == 0, errors) 