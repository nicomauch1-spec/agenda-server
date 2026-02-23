from flask import Flask, jsonify
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/agenda')
def agenda():
    # DATOS DE PRUEBA (Para que tu app de Android funcione mientras destrabas la API)
    # Estos partidos se verán hoy en tu app sin importar el bloqueo de API-Football
    partidos_mock = [
        {
            "home": "Fiorentina",
            "away": "Pisa",
            "league": "Serie A",
            "time": "14:30",
            "priority": False
        },
        {
            "home": "Manchester Utd",
            "away": "Leicester",
            "league": "Premier League",
            "time": "11:00",
            "priority": False
        },
        {
            "home": "San Lorenzo",
            "away": "Velez",
            "league": "Liga Profesional",
            "time": "19:15",
            "priority": True
        },
        {
            "home": "Barcelona",
            "away": "Getafe",
            "league": "La Liga",
            "time": "17:00",
            "priority": False
        }
    ]
    
    return jsonify(partidos_mock)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
