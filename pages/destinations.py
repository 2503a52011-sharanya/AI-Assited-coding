import streamlit as st
from services.destination_service import DestinationService
from services.weather_service import WeatherService
from services.map_service import MapService
from utils.helpers import format_currency


def render_destinations_page():
    st.title("📍 Destination Detailed Spotlight")

    dest_id = st.session_state.get("selected_dest_id")
    destinations = DestinationService.get_all(limit=100)
    
    # Destination selector
    dest_names = [d["name"] for d in destinations]
    current_index = 0
    if dest_id:
        for idx, d in enumerate(destinations):
            if d["id"] == dest_id:
                current_index = idx
                break

    selected_name = st.selectbox("Select Destination to Inspect", dest_names, index=current_index)
    selected_dest = next((d for d in destinations if d["name"] == selected_name), destinations[0])
    
    # Hero Details
    col_img, col_desc = st.columns([1.2, 2])
    with col_img:
        st.image(selected_dest.get("image_url") or "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=800", width="stretch")
    with col_desc:
        st.header(selected_dest["name"])
        st.markdown(f"**State / Region:** {selected_dest['state']} | **Country:** {selected_dest.get('country', 'India')}")
        st.markdown(f"**Best Season to Visit:** `{selected_dest.get('best_season', 'October to March')}`")
        st.markdown(f"**Ideal Duration:** `{selected_dest.get('ideal_duration_days', 3)} Days`")
        st.markdown(f"**Estimated Daily Budget:** `{format_currency(selected_dest.get('avg_daily_budget', 3000.0))}`")
        st.write(selected_dest.get("description", ""))
        
        if st.button(f"🎯 Plan Trip to {selected_dest['name']}", type="primary"):
            st.session_state["selected_destination_name"] = selected_dest["name"]
            st.switch_page("pages/planner.py")

    # Weather Widget
    st.markdown("---")
    st.subheader("🌤️ Live Weather & 5-Day Forecast")
    lat = float(selected_dest["latitude"])
    lon = float(selected_dest["longitude"])
    weather = WeatherService.get_weather(lat, lon, selected_dest["name"])
    
    w_cols = st.columns(4)
    with w_cols[0]:
        st.metric("Temperature", f"{weather['temperature']}°C", weather['condition'])
    with w_cols[1]:
        st.metric("Humidity", f"{weather['humidity']}%")
    with w_cols[2]:
        st.metric("Wind Speed", f"{weather['wind_speed']} km/h")
    with w_cols[3]:
        st.metric("Rain Chance", f"{weather.get('forecast', [{}])[0].get('rain_probability', 5)}%")

    # Forecast mini-cards
    if weather.get("forecast"):
        st.markdown("##### 5-Day Outlook")
        f_cols = st.columns(len(weather["forecast"]))
        for idx, f in enumerate(weather["forecast"]):
            with f_cols[idx]:
                st.markdown(f"""
                <div style="background: #f1f5f9; padding: 10px; border-radius: 8px; text-align: center;">
                    <div style="font-weight: 600; font-size: 0.85rem;">{f['date']}</div>
                    <div style="font-size: 1.5rem; margin: 4px 0;">{f['icon']}</div>
                    <div style="font-size: 0.9rem;"><b>{f['max_temp']}°C</b> / {f['min_temp']}°C</div>
                    <div style="font-size: 0.8rem; color: #475569;">🌧️ {f['rain_probability']}%</div>
                </div>
                """, unsafe_allow_html=True)

    # Details: Attractions, Hotels, Activities, Restaurants, Map
    details = DestinationService.get_details(selected_dest["id"])
    tab_attr, tab_hotel, tab_act, tab_rest, tab_map = st.tabs([
        "🏛️ Attractions", "🏨 Accommodations", "🧗 Activities", "🍲 Dining", "🗺️ Map"
    ])

    with tab_attr:
        attractions = details["attractions"]
        if attractions:
            a_cols = st.columns(2)
            for idx, a in enumerate(attractions):
                with a_cols[idx % 2]:
                    with st.container(border=True):
                        st.markdown(f"#### {a['name']}")
                        st.markdown(f"🏷️ **{a['category']}** | ⭐ `{a['rating']}/5.0`")
                        st.markdown(f"🎟️ Entry: **{format_currency(a['entry_fee'])}** | ⏱️ Hours: `{a['opening_time']} - {a['closing_time']}`")
                        st.write(a.get("description", ""))
        else:
            st.info("No curated attractions listed yet.")

    with tab_hotel:
        hotels = details["hotels"]
        if hotels:
            h_cols = st.columns(2)
            for idx, h in enumerate(hotels):
                with h_cols[idx % 2]:
                    with st.container(border=True):
                        st.markdown(f"#### {h['name']}")
                        st.markdown(f"⭐ **{h['star_rating']}-Star {h['hotel_type']}** | Rating: `{h['rating']}/5.0`")
                        st.markdown(f"💰 Nightly Rate: **{format_currency(h['price_per_night'])}**")
                        st.caption(f"📍 {h['address']}")
                        if h.get("amenities"):
                            st.write(f"✨ Amenities: *{h['amenities']}*")
        else:
            st.info("No curated hotels listed yet.")

    with tab_act:
        activities = details["activities"]
        if activities:
            for act in activities:
                with st.container(border=True):
                    st.markdown(f"#### {act['title']}")
                    st.markdown(f"🏷️ `{act['category']}` | ⏱️ `{act['duration_hours']} Hours` | ⭐ `{act['rating']}/5.0`")
                    st.markdown(f"💰 Price: **{format_currency(act['price_per_person'])}** per person")
                    st.write(act["description"])
        else:
            st.info("No activities registered yet.")

    with tab_rest:
        restaurants = details["restaurants"]
        if restaurants:
            r_cols = st.columns(2)
            for idx, r in enumerate(restaurants):
                with r_cols[idx % 2]:
                    with st.container(border=True):
                        veg_badge = "🟢 Pure Veg" if r.get("is_vegetarian") else "🔴 Non-Veg & Veg"
                        st.markdown(f"#### {r['name']}")
                        st.markdown(f"🍽️ **{r['cuisine_type']}** ({veg_badge})")
                        st.markdown(f"💰 Avg Meal: **{format_currency(r['avg_meal_cost'])}** | ⭐ `{r['rating']}/5.0`")
                        st.caption(f"📍 {r.get('address', '')}")
        else:
            st.info("No restaurants registered yet.")

    with tab_map:
        st.subheader(f"Geographical Map: {selected_dest['name']}")
        map_df = MapService.generate_map_dataframe(selected_dest["name"], lat, lon, details["attractions"])
        st.map(map_df, latitude="latitude", longitude="longitude", size="size")


render_destinations_page()

