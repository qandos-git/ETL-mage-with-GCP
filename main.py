import pandas as pd
from flask import Flask, render_template, request, jsonify
import requests
from pydantic import BaseModel
import pickle

class Example(BaseModel):
    temp: float
    min_temp: float
    max_temp: float
    temp_range: float
    
    
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

def get_outfit_recommendation(feels_like):
    if feels_like < 10:
        return "It's really cold! Wear a heavy jacket, scarf, and gloves."
    elif 10 <= feels_like < 20:
        return "Cool weather! A light jacket or hoodie is a good choice."
    elif 20 <= feels_like < 30:
        return "Warm but comfortable. T-shirt and jeans work well."
    else:
        return "Hot weather! Wear light, breathable clothes and stay hydrated."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["GET"])
def get_weather_prediction():
    response = requests.get(WEATHER_API_URL, params=LOCATION_PARAMS)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch weather data"}), 500
    
    data = response.json()
    current_temp = data["current"]["temperature_2m"]
    min_temp = data["daily"]["temperature_2m_min"][0]
    max_temp = data["daily"]["temperature_2m_max"][0]
    temp_range = max_temp - min_temp

    # Predict feels_like temperature
    model_input = [[current_temp, min_temp, max_temp, temp_range]]
    feels_like_pred = model.predict(model_input)[0]

    return jsonify({
        "current_temp": current_temp,
        "predicted_feels_like": feels_like_pred,
        "recommendation": get_outfit_recommendation(feels_like_pred)
    })

if __name__ == "__main__":
    app.run(debug=True)
