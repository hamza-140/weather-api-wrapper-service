from flask import Flask, jsonify
import requests
import json
import redis
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

try:
    r = redis.Redis(
        host=os.getenv('host'),
        port=os.getenv('port'),
        password=os.getenv('password')
    )
    r.ping()
    print("Connected to Redis successfully!")
except redis.ConnectionError as e:
    print(f"Could not connect to Redis: {e}")

@app.route('/weather/<location>')
def get_weather(location):
    cache_key = f'{location.lower()}'
    cached_weather = r.get(cache_key)

    if cached_weather:
        status = "Using cached data from Redis"
        print(status)
        response = json.loads(cached_weather)
    else:
        res = requests.get(f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}?unitGroup=us&key={os.getenv('api')}&contentType=json')
        response = json.loads(res.text)
        r.setex(cache_key, 3600, json.dumps(response))
        status = "Fetched from Api and cached new data in Redis"
        print(status)

    current_weather = response['currentConditions']
    weather_info = {
        "status": status,
        "temperature": f"{(current_weather['temp'] - 32) / 1.8:.2f} °C",
        "condition": current_weather['conditions'],
        "wind_speed": f"{current_weather['windspeed']} mph",
        "humidity": f"{current_weather['humidity']}%",
        "location":location
    }

    return app.response_class(
        response=json.dumps(weather_info, ensure_ascii=False),
        mimetype='application/json'
    )
if __name__ == '__main__':
    app.run(debug=True)
