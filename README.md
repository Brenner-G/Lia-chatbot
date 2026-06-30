# 🤖 LIA — Chatbot com Base de Conhecimento

Chatbot que responde **apenas** com base no conteúdo do arquivo `conhecimento.txt`.

## Estrutura
```
chatbot/
├── app.py              # Servidor Flask
├── conhecimento.txt    # Base de conhecimento
├── requirements.txt    # Dependências
├── .gitignore
└── templates/
    └── index.html      # Interface web
```

## Rodando localmente

### 1. Instale as dependências
```bash
pip install -r requirements.txt
```

### 2. Configure sua chave da API Gemini
Nunca coloque a chave direto no código. Use variável de ambiente:

```bash
# Linux / macOS
export GEMINI_API_KEY="sua-chave-aqui"

# Windows (PowerShell)
$env:GEMINI_API_KEY="sua-chave-aqui"
```

> Obtenha sua chave em: https://aistudio.google.com/apikey

### 3. Edite o arquivo de conhecimento
Abra `conhecimento.txt` e ajuste o conteúdo conforme necessário.

### 4. Inicie o servidor
```bash
python app.py
```

Acesse em `http://localhost:5000`

## Deploy no Render (gratuito)

1. Suba este projeto para um repositório no GitHub (veja seção abaixo).
2. Acesse https://render.com e crie uma conta (pode usar login do GitHub).
3. Clique em **New +** → **Web Service**.
4. Conecte sua conta do GitHub e selecione o repositório do chatbot.
5. Configure:
   - **Name**: o que quiser (ex: `chatbot-lia`)
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. Em **Environment Variables**, adicione:
   - `GEMINI_API_KEY` = sua chave da API
7. Clique em **Create Web Service**. O Render vai instalar, buildar e publicar.
8. Depois do deploy, você recebe uma URL pública tipo `https://chatbot-lia.onrender.com`.

> No plano gratuito do Render, o serviço "dorme" depois de um tempo sem uso e demora alguns segundos para acordar na próxima requisição. Isso é normal.

## Publicando no GitHub

```bash
git init
git add .
git commit -m "Primeiro commit do chatbot"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git
git push -u origin main
```

⚠️ **Nunca** faça commit da sua chave de API. Ela deve ficar só como variável de ambiente, tanto local quanto no Render.

## Personalizando

- **Trocar o arquivo de conhecimento:** altere `KNOWLEDGE_FILE` em `app.py`
- **Mudar o comportamento da IA:** edite o `system_prompt` em `app.py`
- **Trocar o modelo:** altere `GEMINI_MODEL` em `app.py`
