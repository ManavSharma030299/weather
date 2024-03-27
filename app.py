from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)
openweathermap_api_key = os.environ.get('29f6bb5012ba4119260829540477d3b8')

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    city = req.get("result", {}).get("parameters", {}).get("geo-city")

    if city:
        weather_data = get_weather_data(city)
        if weather_data:
            speech = format_weather_response(weather_data)
        else:
            speech = "Weather data not available for the specified city."

        return jsonify({
            "speech": speech,
            "displayText": speech,
            "source": "dialogflow-weather-by-satheshrgs"
        })
    else:
        return jsonify({
            "speech": "Unable to determine the city.",
            "displayText": "Unable to determine the city.",
            "source": "dialogflow-weather-by-satheshrgs"
        })

def get_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={openweathermap_api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def format_weather_response(weather_data):
    temperature = weather_data["main"]["temp"]
    humidity = weather_data["main"]["humidity"]
    wind_speed = weather_data["wind"]["speed"]
    latitude = weather_data["coord"]["lat"]
    longitude = weather_data["coord"]["lon"]

    speech = (f"Today's weather:\n"
              f"Temperature: {temperature}°C\n"
              f"Humidity: {humidity}%\n"
              f"Wind Speed: {wind_speed} m/s\n"
              f"Latitude: {latitude}\n"
              f"Longitude: {longitude}")

    return speech

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
