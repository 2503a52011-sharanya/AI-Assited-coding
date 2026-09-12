import logging
import requests
from config.settings import OPENMETEO_BASE_URL
from utils.caching import get_cached_api_response, set_cached_api_response

logger = logging.getLogger(__name__)

# WMO Weather interpretation codes
WMO_CODES = {
    0: ("Clear sky", "☀️"),
    1: ("Mainly clear", "🌤️"),
    2: ("Partly cloudy", "⛅"),
    3: ("Overcast", "☁️"),
    45: ("Foggy", "🌫️"),
    48: ("Depositing rime fog", "🌫️"),
    51: ("Light drizzle", "🌦️"),
    53: ("Moderate drizzle", "🌦️"),
    55: ("Dense drizzle", "🌧️"),
    61: ("Slight rain", "🌧️"),
    63: ("Moderate rain", "🌧️"),
    65: ("Heavy rain", "⛈️"),
    80: ("Slight rain showers", "🌦️"),
    81: ("Moderate rain showers", "🌧️"),
    82: ("Violent rain showers", "⛈️"),
    95: ("Thunderstorm", "⚡"),
    96: ("Thunderstorm with hail", "⛈️")
}


class WeatherService:
    @staticmethod
    def get_weather(lat: float, lon: float, destination_name: str = "") -> dict:
        """Fetches live weather from Open-Meteo with caching and fallback."""
        cache_key = f"weather_{round(lat, 2)}_{round(lon, 2)}"
        cached = get_cached_api_response(cache_key)
        if cached:
            return cached

        try:
            url = f"{OPENMETEO_BASE_URL}/forecast"
            params = {
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,relative_humidity_2m,weather_code,precipitation,wind_speed_10m",
                "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max",
                "timezone": "auto"
            }
            resp = requests.get(url, params=params, timeout=4)
            if resp.status_code == 200:
                data = resp.json()
                current = data.get("current", {})
                daily = data.get("daily", {})

                code = current.get("weather_code", 0)
                condition, icon = WMO_CODES.get(code, ("Pleasant", "☀️"))

                forecast = []
                times = daily.get("time", [])
                max_temps = daily.get("temperature_2m_max", [])
                min_temps = daily.get("temperature_2m_min", [])
                rain_probs = daily.get("precipitation_probability_max", [])
                daily_codes = daily.get("weather_code", [])

                for i in range(min(5, len(times))):
                    d_code = daily_codes[i] if i < len(daily_codes) else 0
                    d_cond, d_icon = WMO_CODES.get(d_code, ("Clear", "☀️"))
                    forecast.append({
                        "date": times[i],
                        "max_temp": max_temps[i] if i < len(max_temps) else 28.0,
                        "min_temp": min_temps[i] if i < len(min_temps) else 18.0,
                        "rain_probability": rain_probs[i] if i < len(rain_probs) else 10,
                        "condition": d_cond,
                        "icon": d_icon
                    })

                weather_res = {
                    "temperature": current.get("temperature_2m", 25.0),
                    "humidity": current.get("relative_humidity_2m", 55),
                    "wind_speed": current.get("wind_speed_10m", 12.0),
                    "condition": condition,
                    "icon": icon,
                    "precipitation": current.get("precipitation", 0.0),
                    "forecast": forecast,
                    "is_live": True
                }
                set_cached_api_response(cache_key, weather_res, ttl_seconds=7200)
                return weather_res
        except Exception as e:
            logger.warning(f"Open-Meteo live API request failed: {e}. Using intelligent fallback.")

        # Realistic climate fallback
        return {
            "temperature": 24.5,
            "humidity": 58,
            "wind_speed": 10.5,
            "condition": "Pleasant & Clear",
            "icon": "🌤️",
            "precipitation": 0.0,
            "forecast": [
                {"date": "Day 1", "max_temp": 26.0, "min_temp": 17.0, "rain_probability": 15, "condition": "Partly Cloudy", "icon": "⛅"},
                {"date": "Day 2", "max_temp": 25.5, "min_temp": 16.5, "rain_probability": 20, "condition": "Sunny Intervals", "icon": "🌤️"},
                {"date": "Day 3", "max_temp": 27.0, "min_temp": 18.0, "rain_probability": 10, "condition": "Clear Sky", "icon": "☀️"}
            ],
            "is_live": False
        }

    @staticmethod
    def get_itinerary_weather_advisory(weather_data: dict) -> list[str]:
        """Analyzes forecast to generate actionable smart warnings for itinerary planning."""
        advisories = []
        forecast = weather_data.get("forecast", [])
        for idx, day in enumerate(forecast, start=1):
            rain_prob = day.get("rain_probability", 0)
            if rain_prob >= 50:
                advisories.append(
                    f"⚠️ **Rain Alert on Day {idx}** ({rain_prob}% chance): Consider prioritizing indoor attractions "
                    f"(museums, caves, cultural centers) during the afternoon hours."
                )
            elif day.get("max_temp", 25) > 36:
                advisories.append(
                    f"☀️ **High Heat Alert on Day {idx}** ({day['max_temp']}°C): Schedule outdoor exploration early morning or post 4:00 PM."
                )
        return advisories
