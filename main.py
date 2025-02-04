from flask import Flask, render_template, request, jsonify
import requests
import pickle
import json
from apscheduler.schedulers.background import BackgroundScheduler

    
with open('models/model_v0.pkl', 'rb') as m:
    model = pickle.load(m)

app = Flask(__name__)

# Weather API details
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"
LOCATION_PARAMS = {
    "latitude": 26.3333,  # Buraidah, Saudi Arabia
    "longitude": 43.9667,
    "current": "temperature_2m",
    "daily": ["temperature_2m_max", "temperature_2m_min"],
    "timezone": "Asia/Riyadh"
}

DATA_FILE = "weather_data.json"

def fetch_and_store_weather():
    """Fetches daily weather data from API and saves it to a file."""
    response = requests.get(WEATHER_API_URL, params=LOCATION_PARAMS)
    if response.status_code == 200:
        with open(DATA_FILE, "w") as f:
            json.dump(response.json(), f)

# Run fetch function every day
scheduler = BackgroundScheduler()
scheduler.add_job(fetch_and_store_weather, "cron", hour=0, minute=0)
scheduler.start()

def get_stored_weather():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def get_outfit_recommendation(feels_like):
    if feels_like < 10:
        return "الجو بارد جدًا، تدحمل"
    elif 10 <= feels_like < 20:
        return "الجو بارد قليلًا ومناسب للكشتات"
    elif 20 <= feels_like < 30:
        return "جو لطيف مناسب للحدائق."
    else:
        return "🔥"

@app.route("/")
def home():
    """Reads stored weather data and predicts feels_like."""
    data = get_stored_weather()
    if not data:
        return jsonify({"error": "No weather data available"}), 500

    current_temp = data["current"]["temperature_2m"]
    min_temp = data["daily"]["temperature_2m_min"][0]
    max_temp = data["daily"]["temperature_2m_max"][0]
    temp_range = max_temp - min_temp

    # Predict feels_like temperature
    model_input = [[current_temp, min_temp, max_temp, temp_range]]
    feels_like_pred = round(model.predict(model_input)[0])

    return render_template(
        "index.html",
        current_temp= current_temp,
        feels_like =feels_like_pred,
        recommendation=get_outfit_recommendation(feels_like_pred)
    )

@app.route("/test_model", methods=["POST"])
def test_model():
    """Allows users to test the model with their own inputs."""
    data = request.json
    try:
        temp = float(data["temp"])
        temp_min = float(data["temp_min"])
        temp_max = float(data["temp_max"])
        temp_range = float(data["temp_range"])

        model_input = [[temp, temp_min, temp_max, temp_range]]
        feels_like_pred = round(model.predict(model_input)[0])

        return jsonify({
            "feels_like": feels_like_pred,
            "recommendation": get_outfit_recommendation(feels_like_pred)
        })
    except (KeyError, ValueError):
        return jsonify({"error": "⚠️ مدخلات غير صحيحة، تأكد من القيم المدخلة!"}), 400


if __name__ == "__main__":
    fetch_and_store_weather()  # Fetch data initially
    app.run(debug=True)
