import os
import requests
from datetime import datetime, timedelta
from django.conf import settings
from .models import WeatherCache

def get_destination_weather(city_name, lat=None, lon=None, force_refresh=False):
    """
    Fetches real-time weather and 5-day forecast.
    Uses OpenWeather API if OPENWEATHER_API_KEY is present and functional.
    Falls back gracefully to realistic climate-modeled demo data, clearly flagged.
    """
    api_key = getattr(settings, 'OPENWEATHER_API_KEY', '') or os.getenv('OPENWEATHER_API_KEY', '')
    
    # Check cache (30 mins TTL)
    cached = WeatherCache.objects.filter(city__iexact=city_name).first()
    if cached and not force_refresh:
        age = datetime.now(cached.updated_at.tzinfo) - cached.updated_at
        if age < timedelta(minutes=30):
            return {
                'city': cached.city,
                'current': cached.current_data,
                'forecast': cached.forecast_data,
                'is_live': cached.is_live_api,
                'source_label': 'Live Satellite Feed (OpenWeather)' if cached.is_live_api else 'Simulation / Demo Mode (Set OPENWEATHER_API_KEY in .env to activate live API)',
                'updated_at': cached.updated_at.strftime('%b %d, %Y %I:%M %p')
            }

    # Attempt live API call if key configured
    if api_key and api_key != 'your_openweather_api_key_here':
        try:
            current_url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid={api_key}"
            if lat and lon:
                current_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"
            
            c_res = requests.get(current_url, timeout=5)
            if c_res.status_code == 200:
                c_json = c_res.json()
                
                # Fetch 5-day forecast
                forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&units=metric&appid={api_key}"
                if lat and lon:
                    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={api_key}"
                f_res = requests.get(forecast_url, timeout=5)
                forecast_list = []
                if f_res.status_code == 200:
                    f_json = f_res.json()
                    # Group by day
                    seen_dates = set()
                    for item in f_json.get('list', []):
                        dt = item.get('dt_txt', '').split(' ')[0]
                        if dt not in seen_dates and len(seen_dates) < 5:
                            seen_dates.add(dt)
                            forecast_list.append({
                                'date': dt,
                                'temp': f"{round(item['main']['temp'])}°C",
                                'condition': item['weather'][0]['main'],
                                'description': item['weather'][0]['description'].title(),
                                'icon': item['weather'][0]['icon'],
                                'rain_chance': round(item.get('pop', 0) * 100),
                                'humidity': item['main']['humidity'],
                                'wind_speed': f"{item['wind']['speed']} m/s"
                            })

                current_data = {
                    'temperature': f"{round(c_json['main']['temp'])}°C",
                    'temp_num': c_json['main']['temp'],
                    'feels_like': f"{round(c_json['main']['feels_like'])}°C",
                    'condition': c_json['weather'][0]['main'],
                    'description': c_json['weather'][0]['description'].title(),
                    'humidity': f"{c_json['main']['humidity']}%",
                    'wind_speed': f"{c_json['wind']['speed']} m/s",
                    'rain_prob': 85 if 'rain' in c_json['weather'][0]['main'].lower() else 15,
                    'icon': c_json['weather'][0]['icon'],
                }

                cache_obj, _ = WeatherCache.objects.update_or_create(
                    city=city_name,
                    defaults={
                        'latitude': lat or 0,
                        'longitude': lon or 0,
                        'current_data': current_data,
                        'forecast_data': forecast_list,
                        'is_live_api': True
                    }
                )
                return {
                    'city': city_name,
                    'current': current_data,
                    'forecast': forecast_list,
                    'is_live': True,
                    'source_label': 'Live Satellite Feed (OpenWeather API)',
                    'updated_at': datetime.now().strftime('%b %d, %Y %I:%M %p')
                }
        except Exception as e:
            print(f"[Weather API Warning] Falling back to climate simulation: {e}")

    # Realistic climate-aware Demo Mode Fallback
    # Tailored per destination types
    is_rainy_sim = 'goa' in city_name.lower() or 'kerala' in city_name.lower()
    demo_current = {
        'temperature': '29°C',
        'temp_num': 29,
        'feels_like': '31°C',
        'condition': 'Scattered Showers' if is_rainy_sim else 'Sunny & Pleasant',
        'description': 'Intermittent monsoon showers expected' if is_rainy_sim else 'Clear blue skies with light breeze',
        'humidity': '78%' if is_rainy_sim else '54%',
        'wind_speed': '14 km/h',
        'rain_prob': 80 if is_rainy_sim else 10,
        'icon': '10d' if is_rainy_sim else '01d',
    }

    base_date = datetime.now()
    demo_forecast = [
        {
            'date': (base_date + timedelta(days=i)).strftime('%Y-%m-%d'),
            'day_name': (base_date + timedelta(days=i)).strftime('%A'),
            'temp': f"{28 + (i % 3)}°C",
            'condition': 'Heavy Rain' if (is_rainy_sim and i in (1, 2)) else ('Partly Cloudy' if i == 3 else 'Sunny'),
            'description': 'Adverse thunderstorm and heavy rainfall' if (is_rainy_sim and i in (1, 2)) else 'Ideal sightseeing climate',
            'icon': '11d' if (is_rainy_sim and i in (1, 2)) else '02d',
            'rain_chance': 85 if (is_rainy_sim and i in (1, 2)) else 15,
            'humidity': 85 if (is_rainy_sim and i in (1, 2)) else 50,
            'wind_speed': '22 km/h' if (is_rainy_sim and i in (1, 2)) else '10 km/h',
            'is_adverse': True if (is_rainy_sim and i in (1, 2)) else False,
        }
        for i in range(1, 6)
    ]

    cache_obj, _ = WeatherCache.objects.update_or_create(
        city=city_name,
        defaults={
            'latitude': lat or 0,
            'longitude': lon or 0,
            'current_data': demo_current,
            'forecast_data': demo_forecast,
            'is_live_api': False
        }
    )

    return {
        'city': city_name,
        'current': demo_current,
        'forecast': demo_forecast,
        'is_live': False,
        'source_label': 'Simulation / Demo Mode (Set OPENWEATHER_API_KEY in .env for live API)',
        'updated_at': datetime.now().strftime('%b %d, %Y %I:%M %p')
    }
