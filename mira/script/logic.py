from weather import WeatherAware
from predict import MiraPredictor

class MiraLogic:
    def __init__(self):
        self.weather_module = WeatherAware()
        self.predictor = MiraPredictor()

    def analyze_classroom(self, classroom_data):
        # 1. Get Environment Context
        weather = self.weather_module.get_current_weather()
        weather_impact = self.weather_module.analyze_weather_impact(weather['condition'])
        
        # 2. Inject Weather into classroom data for prediction
        classroom_data['weather_condition'] = weather['condition']
        
        # 3. Predict Engagement (0 or 1)
        engagement_status, confidence = self.predictor.predict_engagement(classroom_data)
        
        # 4. Generate Strategic Advice (The "Logic")
        report = {
            "status": "OPTIMAL" if engagement_status == 1 else "CRITICAL",
            "confidence": f"{confidence*100:.1f}%",
            "weather_context": f"It is {weather['condition']}. {weather_impact}",
            "recommendation": ""
        }

        if engagement_status == 1:
            report['recommendation'] = "Current teaching method is effective. Continue monitoring."
        else:
            # DETERIORATING LOGIC
            if weather['condition'] == 'rainy' or weather['condition'] == 'cloudy':
                report['recommendation'] = "Engagement is dropping. Weather is lethargic. SUGGESTION: Switch to an active Group Discussion or Physical Ice-breaker."
            elif classroom_data['method_of_teaching'] == 'lecture':
                report['recommendation'] = "Lecture format is failing. SUGGESTION: Switch to Project-Based Learning immediately."
            else:
                report['recommendation'] = "General fatigue detected. SUGGESTION: Take a 5-minute break or introduce a visual aid."

        return report