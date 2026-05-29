import os
from flask import Flask, request, jsonify, render_template
from azure.ai.projects import AIProjectClient
from azure.identity import AzureCliCredential
from openai import AzureOpenAI

app = Flask(__name__)

API_KEY  = os.environ.get("AZURE_API_KEY")
endpoint = "https://1515427-7907-resource.openai.azure.com/"

client = AzureOpenAI(
    api_key=API_KEY,
    azure_endpoint=endpoint,
    api_version="2024-05-01-preview"
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")

    if not user_input:
        return jsonify({"response": "Por favor escribe algo."})

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Eres InnoBot, asistente virtual de InnovVentas, tienda de productos tecnológicos. Solo responde preguntas sobre productos, pagos, pedidos, devoluciones y envíos. Si preguntan otra cosa responde: Lo siento, solo puedo ayudarte con consultas de InnovVentas."},
                {"role": "user", "content": user_input}
            ]
        )
        return jsonify({"response": response.choices[0].message.content})

    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)