from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
import requests
from openai import OpenAI

# Cargar variables del entorno
load_dotenv()
BITRIX = os.getenv("BITRIX_WEBHOOK")
OPENAI_KEY = os.getenv("OPENAI_KEY")

# Inicializar app Flask
app = Flask(__name__, template_folder="templates", static_folder="static")

# Cliente OpenAI
client = OpenAI(api_key=OPENAI_KEY)

@app.route('/')
def index():
    return render_template('chatbot.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    mensaje = data.get('message', '')
    user_id = data.get('user_id', 1)

    if "tareas" in mensaje.lower():
        tareas = consultar_tareas(user_id)
        return jsonify({"respuesta": f"Tus tareas: {', '.join(tareas)}"})

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": mensaje}]
    )
    respuesta_ia = response.choices[0].message.content
    return jsonify({"respuesta": respuesta_ia})

def consultar_tareas(user_id):
    url = f"{BITRIX}tasks.task.list.json?filter[RESPONSIBLE_ID]={user_id}"
    r = requests.get(url)
    tareas = r.json().get('result', {}).get('tasks', [])
    return [t['task']['title'] for t in tareas]

if __name__ == '__main__':
    app.run()
