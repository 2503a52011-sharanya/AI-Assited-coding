import streamlit as st
import pandas as pd
from services.geocoding_service import geocoding_service
from services.weather_service import weather_service
from ui.components import render_section_header, render_kpi_card, render_demo_badge

def render_weather_view():
    render_section_header("Weather Intelligence Dashboard 🌦️", "Live atmospheric metrics, 7-day forecasts, and AI-adapted travel recommendations")

    c1, c2 = st.columns([2, 1])
    with c1:
        city = st.text_input("Enter Destination City for Weather Inspection", value="Hyderabad").strip()
    with c2:
        st.write("")
        st.write("")
        check_btn = st.button("Check Forecast", type="primary", use_container_width=True)

    coords = geocoding_service.get_coordinates(city)
    if not coords:
        st.warning(f"Coordinates for '{city}' could not be resolved. Please verify the city spelling.")
        return

    weather = weather_service.get_weather(coords[0], coords[1], city)

    if not weather.get("is_live"):
        render_demo_badge("Weather information unavailable in demo mode.")
        st.info("Live weather API could not be reached. Real conditions are not fabricated.")
        return

    # Render Current Conditions
    w1, w2, w3, w4 = st.columns(4)
    with w1:
        render_kpi_card("Temperature", f"{weather.get('temperature')} °C", weather.get("condition", ""))
    with w2:
        render_kpi_card("Humidity", f"{weather.get('humidity')} %", "Relative humidity")
    with w3:
        render_kpi_card("Wind Velocity", f"{weather.get('wind_speed')} km/h", "Surface breezes")
    with w4:
        render_kpi_card("Sunrise / Sunset", f"🌅 {weather.get('sunrise')}", f"🌇 {weather.get('sunset')}")

    st.write("")
    st.markdown(f"""
    <div style="background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 14px; padding: 1.25rem; margin-bottom: 1.5rem;">
        <div style="font-weight: 700; color: #34D399; font-size: 1.05rem;">🤖 Gemini Weather Advisory for {city}:</div>
        <div style="color: #F8FAFC; margin-top: 0.4rem; font-size: 0.95rem;">{weather.get('advice')}</div>
    </div>
    """, unsafe_allow_html=True)

    # 7-Day Forecast
    forecast = weather.get("forecast", [])
    if forecast:
        st.markdown("### 📅 7-Day Outlook & Rainfall Probability")
        df = pd.DataFrame(forecast)
        df.rename(columns={
            "date": "Date",
            "max_temp": "Max Temp (°C)",
            "min_temp": "Min Temp (°C)",
            "rain_prob": "Precipitation Probability (%)"
        }, inplace=True)
        st.dataframe(df, use_container_width=True)
