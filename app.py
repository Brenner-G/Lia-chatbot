import os
from flask import Flask, request, jsonify, render_template
from google import genai
from google.genai import types

app = Flask(__name__)

# A chave é lida da variável de ambiente GEMINI_API_KEY (configurada no Render)
API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

KNOWLEDGE_FILE = "conhecimento.txt"

GEMINI_MODEL = "gemini-2.0-flash"  # modelo estável; troque se quiser usar outro

def carregar_conhecimento():
    """Carrega o conteúdo do arquivo de conhecimento."""
    try:
        with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    if not API_KEY:
        return jsonify({"error": "Chave da API não configurada no servidor."}), 500

    data = request.json
    pergunta = data.get("message", "").strip()
    historico = data.get("history", [])

    if not pergunta:
        return jsonify({"error": "Mensagem vazia"}), 400

    conhecimento = carregar_conhecimento()
    if not conhecimento:
        return jsonify({"error": f"Arquivo '{KNOWLEDGE_FILE}' não encontrado."}), 500

    system_prompt = f"""Você é uma assistente virtual prestativa, Lia. Responda às perguntas do usuário EXCLUSIVAMENTE com base nas informações fornecidas abaixo, seja clara direta e concisa, resumindo a resposta, não use markdown e separe os parágrafos.

REGRAS IMPORTANTES:
1. Responda APENAS com informações presentes no texto abaixo.
2. Se a pergunta não puder ser respondida com base nessas informações, diga educadamente que não tem essa informação disponível e que a pessoa deve procurar o consultorio da UFF.
3. Não invente, suponha ou complemente com conhecimento externo.
4. Responda em português, de forma clara, amigável e facilitada para a gestante.
5. Não mencione que está consultando um arquivo ou base de dados.

BASE DE CONHECIMENTO:
---
{conhecimento}
---"""

    historico_recente = historico[-6:] if len(historico) > 6 else historico

    while historico_recente and historico_recente[0]["role"] != "user":
        historico_recente = historico_recente[1:]

    gemini_history = []
    for msg in historico_recente:
        role = "user" if msg["role"] == "user" else "model"
        gemini_history.append(
            types.Content(role=role, parts=[types.Part(text=msg["content"])])
        )

    try:
        chat_session = client.chats.create(
            model=GEMINI_MODEL,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                max_output_tokens=1000,
                temperature=0.2,
            ),
            history=gemini_history,
        )

        response = chat_session.send_message(pergunta)
        resposta = response.text
        return jsonify({"response": resposta})

    except Exception as e:
        erro = str(e)
        if "token" in erro.lower() or "quota" in erro.lower() or "limit" in erro.lower():
            return jsonify({"error": "Limite de tokens atingido. Tente iniciar uma nova conversa."}), 429
        return jsonify({"error": erro}), 500

if __name__ == "__main__":
    if not API_KEY:
        print("⚠️  ATENÇÃO: Variável GEMINI_API_KEY não definida!")
        print("   Obtenha sua chave em: https://aistudio.google.com/apikey")
    port = int(os.environ.get("PORT", 5000))
    print(f"🤖 Chatbot iniciado em http://localhost:{port}")
    app.run(debug=False, host="0.0.0.0", port=port)
