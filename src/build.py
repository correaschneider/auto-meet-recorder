import PyInstaller.__main__
import os
import shutil

def build_executable():
    # Limpa diretório dist se existir
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    
    # Define os argumentos para o PyInstaller
    args = [
        'src/main.py',  # Script principal
        '--onefile',    # Gera um único arquivo executável
        '--name=meet-recorder',  # Nome do executável
        '--add-data=src/config:config',  # Inclui arquivos de configuração
        '--hidden-import=obsws_python',
        '--hidden-import=openai',
        '--hidden-import=requests',
        '--hidden-import=pydub',
        '--hidden-import=python-dotenv',
        '--noconsole',  # Sem janela de console
        '--icon=src/assets/icon.ico',  # Ícone do executável (você precisará criar este ícone)
    ]
    
    # Executa o PyInstaller
    PyInstaller.__main__.run(args)
    
    print("✅ Executável criado com sucesso!")
    print(f"📁 Localização: {os.path.abspath('dist/meet-recorder')}")

if __name__ == "__main__":
    build_executable() 