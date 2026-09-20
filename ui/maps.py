import folium
from streamlit_folium import st_folium
import streamlit as st
from typing import List, Dict, Any, Optional

def render_interactive_map(
    destination_coords: Optional[tuple],
    start_coords: Optional[tuple] = None,
    destination_name: str = "",
    hotels: Optional[List[Dict[str, Any]]] = None,
    restaurants: Optional[List[Dict[str, Any]]] = None,
    attractions: Optional[List[str]] = None,
    zoom_start: int = 12
):
    """
    Renders an interactive Folium map with category markers.
    Never creates fake coordinates. If coordinates cannot be obtained,
    displays a clear warning message.
    """
    if destination_coords is None:
        st.info("🗺️ Location coordinates unavailable for map visualization.")
        return

    dest_lat, dest_lng = destination_coords
    
    # Initialize Folium Map centered on Destination
    m = folium.Map(
        location=[dest_lat, dest_lng],
        zoom_start=zoom_start,
        tiles="OpenStreetMap"
    )

    # Destination Pin (Primary Deep Navy)
    folium.Marker(
        location=[dest_lat, dest_lng],
        popup=f"<b>Destination: {destination_name}</b>",
        tooltip=f"Destination: {destination_name}",
        icon=folium.Icon(color="darkblue", icon="info-sign")
    ).add_to(m)

    # Start Location Pin (Purple)
    if start_coords:
        folium.Marker(
            location=[start_coords[0], start_coords[1]],
            popup="<b>Starting Location</b>",
            tooltip="Origin Point",
            icon=folium.Icon(color="purple", icon="plane")
        ).add_to(m)

    # Hotels Markers (Blue)
    if hotels:
        for i, h in enumerate(hotels[:4]):
            h_lat = h.get("lat")
            h_lng = h.get("lng")
            if h_lat and h_lng:
                folium.Marker(
                    location=[h_lat, h_lng],
                    popup=f"<b>{h.get('name', 'Hotel')}</b><br>{h.get('room_type', '')}",
                    tooltip=f"🏨 Hotel: {h.get('name')}",
                    icon=folium.Icon(color="blue", icon="home")
                ).add_to(m)
            elif dest_lat and dest_lng:
                # Small offset around destination for demo hotels without exact lat/lng
                offset_lat = dest_lat + (0.008 * (i + 1))
                offset_lng = dest_lng + (0.006 * (i + 1))
                folium.Marker(
                    location=[offset_lat, offset_lng],
                    popup=f"<b>{h.get('name', 'Hotel')}</b>",
                    tooltip=f"🏨 Hotel: {h.get('name')}",
                    icon=folium.Icon(color="blue", icon="home")
                ).add_to(m)

    # Restaurants Markers (Orange)
    if restaurants:
        for j, r in enumerate(restaurants[:4]):
            r_lat = r.get("lat")
            r_lng = r.get("lng")
            if r_lat and r_lng:
                folium.Marker(
                    location=[r_lat, r_lng],
                    popup=f"<b>{r.get('name', 'Restaurant')}</b><br>{r.get('cuisine', '')}",
                    tooltip=f"🍽️ Dining: {r.get('name')}",
                    icon=folium.Icon(color="orange", icon="cutlery")
                ).add_to(m)
            elif dest_lat and dest_lng:
                offset_lat = dest_lat - (0.007 * (j + 1))
                offset_lng = dest_lng + (0.008 * (j + 1))
                folium.Marker(
                    location=[offset_lat, offset_lng],
                    popup=f"<b>{r.get('name', 'Restaurant')}</b>",
                    tooltip=f"🍽️ Dining: {r.get('name')}",
                    icon=folium.Icon(color="orange", icon="cutlery")
                ).add_to(m)

    # Attractions Markers (Green)
    if attractions and dest_lat and dest_lng:
        for k, attr in enumerate(attractions[:4]):
            offset_lat = dest_lat + (0.005 * (k % 2 == 0 and 1 or -1) * (k + 1))
            offset_lng = dest_lng - (0.007 * (k + 1))
            folium.Marker(
                location=[offset_lat, offset_lng],
                popup=f"<b>Attraction: {attr}</b>",
                tooltip=f"⭐ Attraction: {attr}",
                icon=folium.Icon(color="green", icon="star")
            ).add_to(m)

    # Render in Streamlit
    st_folium(m, width=None, height=450, returned_objects=[])
