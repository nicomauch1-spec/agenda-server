from flask import Flask, jsonify
import requests
import os
from datetime import datetime, timedelta, timezone

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY")

LEAGUES = [128,131,13,11,2,39,140,135,78,61]
SAN_LORENZO_ID = 515

@app.route("/")
def home():
    return "Agenda API funcionando"

@app.route("/agenda")
def agenda():
    # Ajuste de zona horaria para Argentina (UTC-3)
    tz_arg = timezone(timedelta(hours=-3))
    today = datetime.now(tz_arg).strftime("%Y-%m-%d")

    url = "https://v3.football.api-sports.io/fixtures"
    headers = {
        "x-apisports-key": API_KEY
    }

    params = {
        "date": today,
        "timezone": "America/Argentina/Buenos_Aires"
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    partidos = []

    for fixture in data.get("response", []):

        if fixture["league"]["id"] in LEAGUES:

            home_id = fixture["teams"]["home"]["id"]
            away_id = fixture["teams"]["away"]["id"]

            partidos.append({
                "priority": home_id == SAN_LORENZO_ID or away_id == SAN_LORENZO_ID,
                "league": fixture["league"]["name"],
                "time": fixture["fixture"]["date"][11:16],
                "home": fixture["teams"]["home"]["name"],
                "away": fixture["teams"]["away"]["name"]
            })

    # Ordena primero por prioridad (los de San Lorenzo) y luego por horario
    partidos.sort(key=lambda x: (not x["priority"], x["time"]))

    return jsonify(partidos)


if __name__ == "__main__":
    # Render asigna dinámicamente el puerto, si falla usa el 10000 localmente
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
