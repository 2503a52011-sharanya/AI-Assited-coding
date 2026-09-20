import logging
import requests
from typing import Dict, Any, Optional
from config.settings import settings

logger = logging.getLogger(__name__)

class WeatherService:
    """
    Retrieves weather data using Open-Meteo (open public API) or OpenWeatherMap.
    Provides weather-aware guidance for itinerary adjustments.
    Never fabricates live weather data when APIs are unreachable.
    """

    @staticmethod
    def get_weather(lat: Optional[float], lng: Optional[float], location_name: str = "") -> Dict[str, Any]:
        if lat is None or lng is None:
            return {
                "is_live": False,
                "location": location_name,
                "message": "Weather information unavailable in demo mode.",
                "advice": "General advice: Carry seasonal layers and check local forecasts before venturing out."
            }

        try:
            # Open-Meteo API query (Free, reliable, no API key required)
            url = (
                f"https://api.open-meteo.com/v1/forecast?"
                f"latitude={lat}&longitude={lng}&"
                f"current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m&"
                f"daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,sunrise,sunset&"
                f"timezone=auto"
            )
            res = requests.get(url, timeout=3.0)
            if res.status_code == 200:
                data = res.json()
                current = data.get("current", {})
                daily = data.get("daily", {})

                # Weather code translation (WMO standard)
                w_code = current.get("weather_code", 0)
                condition, is_rainy = WeatherService._translate_weather_code(w_code)

                # Daily forecast
                forecast = []
                times = daily.get("time", [])
                max_temps = daily.get("temperature_2m_max", [])
                min_temps = daily.get("temperature_2m_min", [])
                rain_probs = daily.get("precipitation_probability_max", [])

                for i in range(min(len(times), 7)):
                    forecast.append({
                        "date": times[i],
                        "max_temp": max_temps[i] if i < len(max_temps) else None,
                        "min_temp": min_temps[i] if i < len(min_temps) else None,
                        "rain_prob": rain_probs[i] if i < len(rain_probs) else 0
                    })

                sunrises = daily.get("sunrise", ["06:00"])
                sunsets = daily.get("sunset", ["18:30"])
                sunrise = sunrises[0].split("T")[-1] if sunrises else "06:00"
                sunset = sunsets[0].split("T")[-1] if sunsets else "18:30"

                advice = WeatherService._generate_weather_advice(condition, is_rainy, current.get("temperature_2m", 25))

                return {
                    "is_live": True,
                    "location": location_name,
                    "temperature": current.get("temperature_2m"),
                    "apparent_temperature": current.get("apparent_temperature"),
                    "humidity": current.get("relative_humidity_2m"),
                    "wind_speed": current.get("wind_speed_10m"),
                    "precipitation": current.get("precipitation", 0),
                    "condition": condition,
                    "is_rainy": is_rainy,
                    "sunrise": sunrise,
                    "sunset": sunset,
                    "forecast": forecast,
                    "advice": advice
                }
        except Exception as e:
            logger.debug(f"Live weather API query failed: {e}")

        return {
            "is_live": False,
            "location": location_name,
            "message": "Weather information unavailable in demo mode.",
            "advice": "Pack comfortably for variable conditions and verify regional alerts before departure."
        }

    @staticmethod
    def _translate_weather_code(code: int) -> Tuple[str, bool]:
        """Translates WMO weather interpretation code."""
        if code == 0:
            return "Clear Sky", False
        elif code in [1, 2, 3]:
            return "Partly Cloudy", False
        elif code in [45, 48]:
            return "Foggy", False
        elif code in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
            return "Rain Showers", True
        elif code in [71, 73, 75, 85, 86]:
            return "Snow", False
        elif code in [95, 96, 99]:
            return "Thunderstorm", True
        return "Scattered Clouds", False

    @staticmethod
    def _generate_weather_advice(condition: str, is_rainy: bool, temp: float) -> str:
        if is_rainy:
            return "Rain is expected in the area. Focus on museums, art galleries, historic indoor monuments, and cozy regional restaurants during shower spells."
        elif temp > 33:
            return "High temperatures anticipated. Schedule outdoor excursions and walking tours for early morning or post-sunset hours, and keep well hydrated."
        elif temp < 10:
            return "Chilly conditions expected. Layer warm woolens and windbreakers, especially for early morning viewpoints and evening cultural strolls."
        else:
            return "Pleasant weather predicted! Ideal conditions for sightseeing, parks, coastal promenades, and outdoor adventure tours."

from typing import Tuple
weather_service = WeatherService()
