import pandas as pd
from utils.helpers import haversine_distance


class MapService:
    @staticmethod
    def calculate_distance_and_time(origin_lat: float, origin_lon: float, dest_lat: float, dest_lon: float):
        """Calculates distance in km and estimates transit times for different modes."""
        distance_km = haversine_distance(origin_lat, origin_lon, dest_lat, dest_lon)
        
        # Approximate average transit speeds (accounting for terrain, stops, transfers)
        transit_times = {
            "Flight": round(max(1.0, distance_km / 500.0) + 1.5, 1), # flight + airport formalities
            "Train": round(max(1.5, distance_km / 55.0), 1),
            "Bus": round(max(2.0, distance_km / 45.0), 1),
            "Cab": round(max(1.5, distance_km / 50.0), 1)
        }
        
        return {
            "distance_km": distance_km,
            "transit_times": transit_times
        }

    @staticmethod
    def generate_map_dataframe(destination_name: str, dest_lat: float, dest_lon: float, attractions: list = None):
        """Builds a pandas DataFrame formatted for st.map or pydeck layer."""
        data = [{
            "name": f"📍 Destination: {destination_name}",
            "latitude": dest_lat,
            "longitude": dest_lon,
            "type": "Destination",
            "size": 120
        }]
        
        if attractions:
            for a in attractions:
                lat = a.get("latitude")
                lon = a.get("longitude")
                if lat and lon:
                    data.append({
                        "name": f"⭐ {a.get('name', 'Attraction')}",
                        "latitude": lat,
                        "longitude": lon,
                        "type": "Attraction",
                        "size": 70
                    })
                    
        return pd.DataFrame(data)
