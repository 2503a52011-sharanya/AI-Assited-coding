import os
from django.conf import settings
from apps.destinations.models import Destination, TouristAttraction
from apps.bookings.models import Booking, Hotel, TransportService, Activity
from apps.weather.services import get_destination_weather

def generate_ai_travel_response(user, session, user_message):
    """
    Handles user chat interactions.
    Injects platform catalog context, user's private bookings (only for authenticated user),
    and utilizes Gemini API with seamless rule-based fallback.
    """
    cleaned_msg = user_message.strip()
    msg_lower = cleaned_msg.lower()

    # 1. Fetch user specific bookings context securely
    user_booking_summary = "None currently active."
    if user and user.is_authenticated:
        recent_bookings = Booking.objects.filter(user=user).order_by('-created_at')[:5]
        if recent_bookings.exists():
            lines = []
            for b in recent_bookings:
                item_name = ""
                if b.hotel:
                    item_name = f"Hotel {b.hotel.name}"
                elif b.transport_service:
                    item_name = f"Transport {b.transport_service.name}"
                elif b.activity:
                    item_name = f"Activity {b.activity.title}"
                lines.append(f"Ref: {b.booking_reference} | Type: {b.get_booking_type_display()} | Item: {item_name} | Status: {b.get_status_display()} | Paid: {'Yes' if b.is_paid else 'No'} | Dates: {b.start_date}")
            user_booking_summary = "\n".join(lines)

    # 2. Fetch platform destination catalog overview
    destinations = Destination.objects.all()[:8]
    dest_overview = ", ".join([f"{d.name} ({d.state_country}, Avg ₹{d.average_budget_per_day}/day)" for d in destinations])

    # 3. Check for specific keywords for direct smart fallback response
    # Weather queries
    for d in destinations:
        if d.name.lower() in msg_lower and ('weather' in msg_lower or 'rain' in msg_lower or 'temp' in msg_lower):
            w = get_destination_weather(d.name, float(d.latitude), float(d.longitude))
            curr = w['current']
            forecast_summary = ", ".join([f"{f['day_name'] if 'day_name' in f else f['date']}: {f['temp']} ({f['condition']})" for f in w['forecast'][:3]])
            return (
                f"🌤️ **Weather Report for {d.name}**:\n\n"
                f"• **Current**: {curr['temperature']}, {curr['condition']} ({curr['description']})\n"
                f"• **Rain Chance**: {curr['rain_prob']}% | **Humidity**: {curr['humidity']} | **Wind**: {curr['wind_speed']}\n"
                f"• **Upcoming 3-Day Forecast**: {forecast_summary}\n\n"
                f"*(Source: {w['source_label']})*\n"
                f"Tip: If rain is forecast during your trip, our smart itinerary revision will automatically suggest indoor cultural attractions & museums!"
            )

    # User booking status query
    if any(k in msg_lower for k in ['my booking', 'booking status', 'confirmed', 'ticket status']):
        if not user or not user.is_authenticated:
            return "Please log in to your traveler account to view your live booking statuses and tickets."
        return (
            f"📋 **Your Active Bookings & Reservations**:\n\n"
            f"{user_booking_summary}\n\n"
            f"You can view complete tickets, vouchers, and cancellation options on the [My Bookings](/my-bookings/) page."
        )

    # Check if Gemini API is available
    api_key = getattr(settings, 'GEMINI_API_KEY', '') or os.getenv('GEMINI_API_KEY', '')
    if api_key and api_key != 'your_gemini_api_key_here':
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            
            # Retrieve recent conversation history
            recent_msgs = session.messages.order_by('-timestamp')[:6]
            history_text = "\n".join([f"{m.sender}: {m.content}" for m in reversed(recent_msgs)])

            system_instruction = f"""
You are the official AI Travel Assistant for 'AI Smart Travel and Tourism Recommendation System' (Tagline: 'Your Journey. Your Interests. Your AI-Powered Trip.').
You are helpful, inspiring, practical, and precise.

Platform Context:
- Available Catalog Destinations: {dest_overview}
- The Authenticated Traveler's Bookings:
{user_booking_summary}

Rules:
1. Always give realistic budgets (in INR ₹), itineraries, and travel time advice.
2. If the user asks about changing activities due to weather, recommend indoor museums, galleries, covered markets, or heritage palaces.
3. If the user asks about their personal bookings, only report the authenticated traveler's bookings provided above. Never hallucinate fake booking references or alter other users' data.
4. Keep answers clean, nicely structured with bullet points and bold highlights.
"""
            model = genai.GenerativeModel(model_name="gemini-1.5-flash")
            prompt = f"{system_instruction}\n\nConversation History:\n{history_text}\nUser: {cleaned_msg}\nAssistant:"
            response = model.generate_content(prompt)
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            print(f"[Gemini AI Notice] Falling back to rule-based engine: {e}")

    # High-quality Intelligent Fallback Engine
    if any(k in msg_lower for k in ['budget', 'cost', '₹', 'rupees', 'price']):
        return (
            f"💰 **Budget Travel Advice**:\n\n"
            f"For popular destinations like Goa, Jaipur, or Kerala, an estimated breakdown per day is:\n"
            f"• **Budget Explorer**: ₹1,500 - ₹2,500/day (Guest houses, local transit, street delicacies)\n"
            f"• **Comfort Family**: ₹4,000 - ₹7,500/day (3-4 Star hotels, private cabs, monument tickets)\n"
            f"• **Luxury Vacation**: ₹12,000+/day (5-Star heritage resorts, guided private tours)\n\n"
            f"You can use our **[Smart AI Trip Planner](/plan-trip/)** to enter your exact budget and let our algorithm optimize day-wise allocations!"
        )

    if any(k in msg_lower for k in ['children', 'kid', 'family']):
        return (
            f"👨‍👩‍👧‍👦 **Family & Kid-Friendly Recommendations**:\n\n"
            f"1. **Jaipur**: Elephant sanctuary visits, Albert Hall Museum, Light & Sound show at Amer Fort.\n"
            f"2. **Goa**: Dolphin-watching boat rides, Naval Aviation Museum, Butterfly Conservatory of Goa.\n"
            f"3. **Kerala**: Eravikulam National Park (Munnar), Periyar Wildlife Sanctuary boat safaris.\n\n"
            f"Our platform highlights safety ratings, minimal walking paths, and child-friendly dining."
        )

    if any(k in msg_lower for k in ['rain', 'bad weather', 'indoor', 'storm']):
        return (
            f"☔ **Weather Protection & Indoor Alternatives**:\n\n"
            f"When bad weather or heavy rain impacts outdoor sightseeing:\n"
            f"• **Goa**: Visit the Museum of Christian Art, Houses of Goa Architecture Museum, or spice plantation sheltered tastings.\n"
            f"• **Jaipur**: Albert Hall Central Museum, City Palace Museum, and covered traditional bazaars like Johari Bazaar.\n"
            f"• Our system automatically runs weather forecasts and flags adverse conditions with side-by-side indoor substitution plans on your itinerary page!"
        )

    # General travel concierge greeting & guide
    return (
        f"👋 Hello! I am your AI Travel Assistant for **AI Smart Travel and Tourism**.\n\n"
        f"I can help you with:\n"
        f"• **Personalized Itineraries**: Multi-day trip plans tailored to your budget and travel style.\n"
        f"• **Weather-Smart Planning**: Real-time forecasts and indoor rain-friendly alternatives.\n"
        f"• **In-Platform Bookings**: Hotels, transport (buses, cabs), and guided activity tickets.\n"
        f"• **Your Bookings**: Checking live status, vouchers, and cancellation rules.\n\n"
        f"How can I assist your journey today? Try asking: *'Plan a 3-day family trip to Jaipur'* or *'What is the weather like in Goa?'*"
    )
