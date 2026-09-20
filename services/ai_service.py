import json
import logging
import re
from typing import Dict, Any, List, Optional
from config.settings import settings
from services.recommendation_engine import recommendation_engine

logger = logging.getLogger(__name__)

class AIService:
    """
    Google Gemini AI service wrapper.
    Responsible for:
    - Structured itinerary generation
    - Budget analysis and alternative suggestions
    - Weather-aware adjustments
    - Travel Assistant chatbot
    - Mood-based trip planning
    - Fallback protection (NEVER crashes if Gemini is offline)
    """

    def __init__(self):
        self.client = None
        self._init_gemini()

    def _init_gemini(self):
        if settings.has_gemini_key():
            try:
                import google.generativeai as genai
                genai.configure(api_key=settings.GEMINI_API_KEY)
                # Use gemini-1.5-flash or gemini-pro
                self.model = genai.GenerativeModel("gemini-1.5-flash")
                self.chat_model = genai.GenerativeModel("gemini-1.5-flash")
                self.is_configured = True
                logger.info("Google Gemini AI client configured successfully.")
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini client: {e}")
                self.is_configured = False
        else:
            self.is_configured = False

    def generate_trip_plan(
        self,
        start_location: str,
        destination: str,
        start_date: str,
        end_date: str,
        days: int,
        travelers: int,
        budget: float,
        currency: str,
        travel_style: str,
        interests: List[str],
        accommodation_pref: str,
        food_preferences: List[str],
        transport_preferences: List[str],
        weather_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generates personalized trip plan using Gemini if available,
        otherwise seamlessly executes the algorithmic recommendation engine.
        """
        # Always prepare the reliable fallback result first
        fallback_plan = recommendation_engine.generate_recommendation(
            start_location=start_location,
            destination=destination,
            start_date=start_date,
            end_date=end_date,
            days=days,
            travelers=travelers,
            budget=budget,
            currency=currency,
            travel_style=travel_style,
            interests=interests,
            accommodation_pref=accommodation_pref,
            food_preferences=food_preferences,
            transport_preferences=transport_preferences,
            weather_info=weather_info
        )

        if not self.is_configured:
            fallback_plan["is_ai_mode"] = False
            fallback_plan["ai_notice"] = "AI service unavailable — using demo recommendation mode."
            return fallback_plan

        # Attempt Gemini Generation
        try:
            prompt = self._build_itinerary_prompt(
                start_location=start_location,
                destination=destination,
                start_date=start_date,
                end_date=end_date,
                days=days,
                travelers=travelers,
                budget=budget,
                currency=currency,
                travel_style=travel_style,
                interests=interests,
                accommodation_pref=accommodation_pref,
                food_preferences=food_preferences,
                transport_preferences=transport_preferences,
                weather_info=weather_info
            )

            response = self.model.generate_content(
                prompt,
                generation_config={"temperature": 0.3}
            )

            raw_text = response.text if response and hasattr(response, "text") else ""
            parsed = self._extract_and_validate_json(raw_text)

            if parsed and "itinerary" in parsed and "estimated_costs" in parsed:
                # Merge curated real hotel and transport candidates into AI result for consistency
                if not parsed.get("hotels"):
                    parsed["hotels"] = fallback_plan["hotels"]
                if not parsed.get("restaurants"):
                    parsed["restaurants"] = fallback_plan["restaurants"]
                if not parsed.get("transport_options"):
                    parsed["transport_options"] = fallback_plan["transport_options"]
                
                parsed["is_ai_mode"] = True
                parsed["ai_notice"] = "Generated live with Google Gemini AI."
                return parsed
            else:
                logger.warning("Gemini JSON validation failed, using resilient fallback plan.")
        except Exception as e:
            logger.warning(f"Gemini API request failed: {e}. Activating fallback.")

        fallback_plan["is_ai_mode"] = False
        fallback_plan["ai_notice"] = "AI service unavailable — using demo recommendation mode."
        return fallback_plan

    def ask_travel_assistant(
        self,
        question: str,
        context: Optional[Dict[str, Any]] = None,
        chat_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """Interactive AI Travel Assistant chat with trip context memory."""
        if not self.is_configured:
            return self._fallback_assistant_response(question, context)

        try:
            ctx_prompt = ""
            if context:
                ctx_prompt = (
                    f"Current Trip Context:\n"
                    f"- Destination: {context.get('destination', 'N/A')}\n"
                    f"- Travelers: {context.get('travelers', 1)}\n"
                    f"- Duration: {context.get('days', 3)} days\n"
                    f"- Budget: {context.get('currency', 'INR')} {context.get('budget', 20000)}\n"
                    f"- Travel Style: {context.get('travel_style', 'Standard')}\n\n"
                )

            system_instruction = (
                "You are an expert AI Travel Concierge for the AI Smart Tourism Platform. "
                "Provide polite, concise, practical, and highly specific travel advice. "
                "Suggest exact spots, realistic budget tips, transit hacks, and local food items."
            )

            full_prompt = f"{system_instruction}\n\n{ctx_prompt}User Question: {question}"
            response = self.chat_model.generate_content(full_prompt)
            return response.text.strip()
        except Exception as e:
            logger.warning(f"Gemini chat failed: {e}")
            return self._fallback_assistant_response(question, context)

    def generate_mood_trip(self, mood: str, destination: str, days: int, budget: float, currency: str) -> Dict[str, Any]:
        """Generate mood-specific recommendations."""
        mood_themes = {
            "Relaxing": {"focus": "Spas, wellness, tranquil lakes, quiet cafes, sunset viewpoints", "pacing": "Slow and restorative"},
            "Adventurous": {"focus": "Trekking, water sports, rugged trails, outdoor thrills", "pacing": "High energy & active"},
            "Romantic": {"focus": "Candlelit fine dining, scenic promenades, private boat rides, rooftop sunsets", "pacing": "Intimate and unhurried"},
            "Spiritual": {"focus": "Ancient temples, meditation sanctuaries, historic heritage shrines, ashrams", "pacing": "Serene and reflective"},
            "Cultural": {"focus": "Heritage monuments, museums, local craft workshops, classical performances", "pacing": "In-depth discovery"},
            "Foodie": {"focus": "Famous street food stalls, heritage eateries, artisanal cafes, cooking masterclasses", "pacing": "Culinary trail"},
            "Nature": {"focus": "Botanical gardens, wildlife reserves, national parks, waterfalls", "pacing": "Scenic immersion"},
            "Photography": {"focus": "Golden hour spots, architectural symmetry, iconic viewpoints, colorful markets", "pacing": "Visual and creative"}
        }
        theme = mood_themes.get(mood, mood_themes["Relaxing"])
        return {
            "mood": mood,
            "theme_focus": theme["focus"],
            "pacing": theme["pacing"],
            "summary": f"A specialized {mood} experience tailored for {destination} emphasizing {theme['focus']}."
        }

    def _build_itinerary_prompt(
        self,
        start_location: str,
        destination: str,
        start_date: str,
        end_date: str,
        days: int,
        travelers: int,
        budget: float,
        currency: str,
        travel_style: str,
        interests: List[str],
        accommodation_pref: str,
        food_preferences: List[str],
        transport_preferences: List[str],
        weather_info: Dict[str, Any]
    ) -> str:
        weather_summary = f"{weather_info.get('condition', 'Normal')}, Temp: {weather_info.get('temperature', 26)}°C"
        return f"""
You are the AI engine for a smart tourism platform.
Create a structured JSON travel plan based on these user specifications:

Input:
- Start Location: {start_location}
- Destination: {destination}
- Dates: {start_date} to {end_date} ({days} days)
- Travelers: {travelers}
- Budget: {currency} {budget}
- Travel Style: {travel_style}
- Interests: {", ".join(interests)}
- Accommodation Preference: {accommodation_pref}
- Food Preferences: {", ".join(food_preferences)}
- Transport Preferences: {", ".join(transport_preferences)}
- Weather Forecast: {weather_summary}

Requirements:
1. Return strictly valid JSON with no markdown wrapping or preamble.
2. JSON must follow this exact schema:
{{
  "destination_summary": "string",
  "attractions": ["string", "string", ...],
  "weather_advice": "string",
  "itinerary": [
    {{
      "day": 1,
      "date": "YYYY-MM-DD",
      "theme": "string",
      "morning": {{
        "time": "09:00 AM - 12:30 PM",
        "activity": "string",
        "location": "string",
        "duration": "string",
        "travel_time": "string",
        "estimated_cost": 0,
        "meal_recommendation": "string"
      }},
      "afternoon": {{
        "time": "01:30 PM - 05:00 PM",
        "activity": "string",
        "location": "string",
        "duration": "string",
        "travel_time": "string",
        "estimated_cost": 0,
        "meal_recommendation": "string"
      }},
      "evening": {{
        "time": "06:00 PM - 09:30 PM",
        "activity": "string",
        "location": "string",
        "duration": "string",
        "travel_time": "string",
        "estimated_cost": 0,
        "meal_recommendation": "string"
      }}
    }}
  ],
  "estimated_costs": {{
    "transportation": 0,
    "accommodation": 0,
    "food": 0,
    "activities": 0,
    "local_travel": 0,
    "miscellaneous": 0,
    "total_estimated": 0,
    "currency": "{currency}"
  }},
  "budget_analysis": {{
    "total_budget": {budget},
    "estimated_cost": 0,
    "remaining_budget": 0,
    "utilization_percentage": 0.0,
    "status": "string",
    "is_over_budget": false,
    "alternatives": []
  }},
  "travel_tips": ["string", "string", ...]
}}
"""

    def _extract_and_validate_json(self, raw_text: str) -> Optional[Dict[str, Any]]:
        """Cleans, repairs, and parses JSON output from LLM."""
        if not raw_text:
            return None
        # Remove Markdown fences
        cleaned = re.sub(r"^```(?:json)?", "", raw_text.strip(), flags=re.MULTILINE)
        cleaned = re.sub(r"```$", "", cleaned.strip(), flags=re.MULTILINE).strip()

        # Find first { and last }
        start_idx = cleaned.find("{")
        end_idx = cleaned.rfind("}")
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            candidate = cleaned[start_idx:end_idx + 1]
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                # Attempt light sanitization (trailing commas)
                sanitized = re.sub(r",\s*([\]}])", r"\1", candidate)
                try:
                    return json.loads(sanitized)
                except Exception:
                    pass
        return None

    def _fallback_assistant_response(self, question: str, context: Optional[Dict[str, Any]]) -> str:
        """Intelligent offline rule-based response generator for travel queries."""
        q_lower = question.lower()
        dest = context.get("destination", "your destination") if context else "your destination"

        if "tomorrow" in q_lower or "what can i do" in q_lower:
            return f"For tomorrow in {dest}, start early with a visit to the top historic monument before peak heat and crowds. Head to an authentic local bistro for lunch, and spend your afternoon exploring the central artisan market or museums, followed by a scenic sunset promenade."
        elif "hotel" in q_lower or "cheaper" in q_lower or "stay" in q_lower:
            return f"To save on accommodation in {dest}, look for certified boutique homestays or 3-star business hotels near public transit hubs. Booking rooms with complimentary breakfast can save up to 15% on daily food costs."
        elif "rain" in q_lower or "weather" in q_lower:
            return f"If rain is forecast in {dest}, shift your plan toward indoor cultural attractions such as museums, art galleries, palace interiors, and historic covered bazaars. Carry an umbrella and slip-resistant footwear."
        elif "cost" in q_lower or "budget" in q_lower or "reduce" in q_lower:
            return f"To reduce trip expenses in {dest}: 1) Use express rail or metro instead of private taxis, 2) Explore street food markets and local eateries for lunch, 3) Book attraction passes online in advance for combo discounts."
        else:
            return f"Great question about {dest}! Based on your trip preferences, prioritizing central locations, taking advantage of city transit cards, and scheduling major sightseeing early in the day will give you the best experience while staying within budget."

ai_service = AIService()
