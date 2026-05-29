from flask import Flask, request, jsonify, render_template
from azure.identity import InteractiveBrowserCredential
from azure.ai.projects import AIProjectClient
import os

app = Flask(__name__)

endpoint   = "https://1515427-7907-resource.services.ai.azure.com/api/projects/1515427-7907"
my_agent   = "iatrabajomartes"
my_version = "4"

print("Iniciando autenticación con Azure...")

credential     = InteractiveBrowserCredential()
project_client = AIProjectClient(
    endpoint=endpoint,
    credential=credential
)

openai_client = project_client.get_openai_client()

print("✅ Autenticación exitosa. Servidor listo.")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    user_input = data.get("message", "")

    if not user_input:
        return jsonify({
            "response": "Por favor escribe algo."
        })

    try:

        response = openai_client.responses.create(

            input=[
                {
                    "role": "user",
                    "content": user_input
                }
            ],

            extra_body={
                "agent_reference": {
                    "name": my_agent,
                    "version": my_version,
                    "type": "agent_reference"
                }
            },
        )

        return jsonify({
            "response": response.output_text
        })

    except Exception as e:

        return jsonify({
            "response": f"Error: {str(e)}"
        })

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )