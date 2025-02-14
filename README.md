# 📌 Guia de Instalação e Execução do Script

Este guia descreve como configurar e executar o script para **gravação automática de reuniões do Google Meet com OBS Studio, extração de áudio, transcrição e formatação da transcrição em tópicos**.

----------

## ✅ 1. Requisitos

Antes de executar o script, certifique-se de que seu sistema tem os seguintes pacotes instalados:

### 📌 Dependências do Sistema

Execute o seguinte comando no terminal:

```bash
sudo apt update && sudo apt install ffmpeg xdg-utils -y

```

- **`ffmpeg`** → Extrai o áudio do vídeo.
- **`xdg-utils`** → Abre automaticamente arquivos formatados.

### 📌 Instalar o Google Chrome ou Brave

Se estiver usando **Chrome**:

```bash
sudo apt install google-chrome-stable -y

```

Se estiver usando **Brave**:

```bash
sudo apt install brave-browser -y

```

----------

## ✅ 2. Configurar o Navegador

Alterando o `.desktop` do navegador para sempre iniciar com `--remote-debugging-port`  
O script precisa acessar as abas do navegador via Remote Debugging.

Se quiser garantir que o navegador sempre inicie com a opção de depuração ativada:

1. Edite o arquivo `.desktop` do navegador:

    ```bash
    code /usr/share/applications/brave-browser.desktop
    
    ```

    ou, para Chrome:

    ```bash
    code /usr/share/applications/google-chrome.desktop
    
    ```

2. Dentro do arquivo, adicione `--remote-debugging-port=9222` a todas as linhas que começam com `Exec=`.
3. Salve o arquivo e reinicie o navegador.

----------

## ✅ 3. Instalar Dependências do Python

O script usa bibliotecas específicas. Para instalá-las, execute:

```bash
pip install obsws-python openai requests

```

----------

## ✅ 4. Configurar o OBS Studio

### 📌 Instalar o OBS Studio

Execute o seguinte comando para instalar o OBS Studio no Ubuntu:

```bash
sudo add-apt-repository ppa:obsproject/obs-studio -y
sudo apt update && sudo apt install obs-studio -y

```

1. **Ative o WebSocket no OBS**

    - Vá em `Tools` → `Servidor WebSocket`.
    - **Ative** a opção **"Enable WebSocket server"** e mantenha a porta `4455`.
    - Desative `Enable Authentication`.
    - Clique em `Apply` e `Ok`.
2. **Crie uma cena chamada "Meet"**

    - Vá em `Cenas` e clique no `+`.
    - Nomeie como **"Meet"**.
3. **Adicione os Sources**

    - Vá em `Sources` → `Add source`.
    - Selecione `Screen Capture (PipeWire)`.
    - Selecione também `Audio Output Capture (PulseAudio)`.
4. **Configure o caminho do Output do vídeo**

    - Vá em `Controls` → `Settings` e submenu `Output`.
    - Na seção de `Recording` no campo `Recording Path` adicione o `~/Videos/Meet`.
    - Clique em `Apply` e `Ok`.

----------

## ✅ 5. Configurar a API da OpenAI

O script usa a **API Whisper da OpenAI** para transcrição.

1. **Crie uma conta na OpenAI**: [https://openai.com/](https://openai.com/)
2. **Pegue sua API Key**: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
3. **Edite o script** e substitua `OPENAI_API_KEY` pela sua chave:

    ```python
    OPENAI_API_KEY = "SUA_CHAVE_AQUI"
    
    ```

----------

## ✅ 6. Executar o Script

Agora que tudo está configurado, basta rodar:

```bash
python3 meet_and_obs.py

```

O script irá: ✅ Detectar reuniões do Google Meet  
✅ Iniciar a gravação no OBS  
✅ Parar a gravação ao final  
✅ Extrair o áudio  
✅ Transcrever automaticamente  
✅ Formatar a transcrição em tópicos

----------

## ✅ 7. Rodar Automaticamente no Boot

Para que o script inicie com o sistema:

### 📌 Criando um Link Simbólico para /bin

O Ubuntu requer que scripts executáveis estejam em diretórios do sistema para iniciar automaticamente. Para isso, criamos um **link simbólico** para `/bin`:

1. Torne o script executável:

    ```bash
    chmod +x /caminho/para/meet_and_obs.py
    
    ```

2. Crie um link simbólico em `/bin`:

    ```bash
    sudo ln -s /caminho/para/meet_and_obs.py /bin/meet_and_obs.py
    
    ```

3. Agora o script pode ser executado apenas com:

    ```bash
    python3 /bin/meet_and_obs.py
    
    ```

### 📌 Usando o Crontab

1. Edite o `crontab`:

    ```bash
    crontab -e
    
    ```

2. Adicione a linha:

    ```bash
    @reboot python3 /bin/meet_and_obs.py &
    
    ```

### 📌 Usando o Startup Applications (Aplicativos de Inicialização)

1. Abra o `Startup Applications` no Ubuntu.
2. Clique em `Add`.
3. No campo `Name`, insira um nome como `Meet OBS Recorder`.
4. No campo `Command`, insira:

    ```bash
    python3 meet_and_obs.py
    ```

5. No campo `Comment`, insira uma descrição, como `Inicia a gravação automática do Google Meet`.
6. Clique em `Save`.

Isso garantirá que o script seja iniciado automaticamente ao ligar o sistema.

----------

Agora o **Google Meet será gravado e transcrito automaticamente**, sem precisar de ações manuais! 🚀

Se precisar de ajustes, me avise! 😃
