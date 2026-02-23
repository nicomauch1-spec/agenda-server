from flask import Flask, jsonify
import requests
import os
from datetime import datetime
import pytz # Recomendado para manejar zonas horarias

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY")
LEAGUES = [128, 131, 13, 11, 2, 39, 140, 135, 78, 61]
SAN_LORENZO_ID = 515

@app.route("/")
def home():
    return {"status": "online", "message": "Agenda API funcionando"}

@app.route("/agenda")
def agenda():
    # Forzamos la zona horaria de Argentina sin importar dónde esté el servidor
    tz = pytz.timezone('America/Argentina/Buenos_Aires')
    today = datetime.now(tz).strftime("%Y-%m-%d")

    url = "https://v3.football.api-sports.io/fixtures"
    headers = {"x-apisports-key": API_KEY}
    params = {
        "date": today,
        "timezone": "America/Argentina/Buenos_Aires"
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status() # Lanza error si la API responde mal
        data = response.json()

        partidos = []
        for fixture in data.get("response", []):
            if fixture["league"]["id"] in LEAGUES:
                home_team = fixture["teams"]["home"]
                away_team = fixture["teams"]["away"]
                
                # Check de San Lorenzo (Prioridad)
                is_priority = home_team["id"] == SAN_LORENZO_ID or away_team["id"] == SAN_LORENZO_ID

                partidos.append({
                    "priority": is_priority,
                    "league": fixture["league"]["name"],
                    "time": fixture["fixture"]["date"][11:16], # HH:mm
                    "home": home_team["name"],
                    "away": away_team["name"],
                    "status": fixture["fixture"]["status"]["short"] # Agregado: para saber si ya empezó o terminó
                })

        # Ordenar: Primero San Lorenzo, luego por horario
        partidos.sort(key=lambda x: (not x["priority"], x["time"]))
        return jsonify(partidos)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Render usa la variable de entorno PORT, si no existe usa 10000
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
