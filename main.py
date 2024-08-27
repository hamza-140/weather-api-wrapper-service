import requests
import json

res = requests.get('https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/lahore?unitGroup=us&key=5WYDX6XPDCZPZ932JKG2CMYRU&contentType=json')

response = json.loads(res.text)
current_weather = response['currentConditions']
print(f"Temperature: {(current_weather['temp']-32)/1.8:.2f}°C")
print(f"Condition: {current_weather['conditions']}")
print(f"Wind Speed: {current_weather['windspeed']} mph")
print(f"Humidity: {current_weather['humidity']}%")

import redis

r = redis.Redis(
  host='redis-10759.c83.us-east-1-2.ec2.redns.redis-cloud.com',
  port=10759,
  password='aQkubnh5LVaQtwdeSQBDzC79EcI8V9zc')
