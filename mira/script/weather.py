import requests
import random

# API Configuration (You would replace this with a real API key from OpenWeatherMap)
API_KEY = "YOUR_API_KEY"
CITY = "Nairobi" # Default, can be dynamic

class WeatherAware:
    def __init__(self):
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    def get_current_weather(self):
        """Fetches real weather or simulates it if no API key is present."""
        try:
            # Simulate for now to ensure code runs without API Key
            # In production, uncomment the requests logic
            weather_conditions = ['sunny', 'rainy', 'cloudy', 'stormy']
            condition = random.choice(weather_conditions)
            temp = random.randint(18, 30)
            
            # Real API Logic (Commented out for safety)
            # params = {'q': CITY, 'appid': API_KEY, 'units': 'metric'}
            # response = requests.get(self.base_url, params=params)
            # data = response.json()
            # condition = data['weather'][0]['main'].lower()
            # temp = data['main']['temp']
            
            return {"condition": condition, "temperature": temp}
        except Exception as e:
            return {"condition": "sunny", "temperature": 25}

    def analyze_weather_impact(self, condition):
        """Returns the likely physiological effect on students."""
        impacts = {
            "sunny": "High energy, potentially distracted if too hot.",
            "rainy": "Lethargic, cozy, lower concentration levels.",
            "cloudy": "Stable, good for focus.",
            "stormy": "Anxious, distracted by noise."
        }
        return impacts.get(condition, "Normal")