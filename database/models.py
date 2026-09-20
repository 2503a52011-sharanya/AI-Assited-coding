from datetime import datetime, timezone
import uuid
from typing import Dict, Any, List, Optional

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def generate_id(prefix: str = "id") -> str:
    return f"{prefix}-{uuid.uuid4().hex[:10]}"

def create_user_doc(
    email: str,
    password_hash: str,
    full_name: str,
    role: str = "Traveler",
    phone: str = "",
    provider_business_name: str = "",
    provider_type: str = ""
) -> Dict[str, Any]:
    return {
        "_id": generate_id("usr"),
        "email": email.strip().lower(),
        "password_hash": password_hash,
        "full_name": full_name.strip(),
        "role": role,  # Traveler, Provider, Admin
        "phone": phone.strip(),
        "provider_business_name": provider_business_name.strip(),
        "provider_type": provider_type.strip(),
        "provider_approved": (role != "Provider"),  # Providers need approval by default
        "is_active": True,
        "created_at": now_iso()
    }

def create_trip_doc(
    user_id: str,
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
    food_prefs: List[str],
    transport_prefs: List[str],
    itinerary: List[Dict[str, Any]],
    estimated_costs: Dict[str, Any],
    weather_info: Optional[Dict[str, Any]] = None,
    hotels: Optional[List[Dict[str, Any]]] = None,
    restaurants: Optional[List[Dict[str, Any]]] = None,
    transport_options: Optional[List[Dict[str, Any]]] = None,
    travel_tips: Optional[List[str]] = None,
    ai_mode: str = "gemini"  # "gemini" or "demo_fallback"
) -> Dict[str, Any]:
    return {
        "_id": generate_id("trip"),
        "user_id": user_id,
        "start_location": start_location,
        "destination": destination,
        "start_date": start_date,
        "end_date": end_date,
        "days": days,
        "travelers": travelers,
        "budget": budget,
        "currency": currency,
        "travel_style": travel_style,
        "interests": interests,
        "accommodation_pref": accommodation_pref,
        "food_prefs": food_prefs,
        "transport_prefs": transport_prefs,
        "itinerary": itinerary,
        "estimated_costs": estimated_costs,
        "weather_info": weather_info or {},
        "hotels": hotels or [],
        "restaurants": restaurants or [],
        "transport_options": transport_options or [],
        "travel_tips": travel_tips or [],
        "ai_mode": ai_mode,
        "status": "Upcoming",
        "created_at": now_iso()
    }

def create_hotel_doc(
    name: str,
    destination: str,
    room_type: str,
    price_per_night: float,
    star_rating: int = 4,
    guest_rating: float = 4.5,
    amenities: Optional[List[str]] = None,
    address: str = "",
    lat: Optional[float] = None,
    lng: Optional[float] = None,
    image_url: str = "",
    description: str = "",
    provider_id: str = "system"
) -> Dict[str, Any]:
    return {
        "_id": generate_id("htl"),
        "provider_id": provider_id,
        "name": name,
        "destination": destination,
        "room_type": room_type,
        "price_per_night": price_per_night,
        "star_rating": star_rating,
        "guest_rating": guest_rating,
        "amenities": amenities or ["WiFi", "Breakfast", "Air Conditioning", "Room Service"],
        "address": address or f"Centrally located, {destination}",
        "lat": lat,
        "lng": lng,
        "image_url": image_url or "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80",
        "description": description or f"A delightful stay in {destination} offering comfort and premium hospitality.",
        "is_available": True,
        "created_at": now_iso()
    }

def create_restaurant_doc(
    name: str,
    destination: str,
    cuisine: str,
    price_level: str = "$$",
    avg_cost: float = 800.0,
    rating: float = 4.6,
    opening_hours: str = "11:00 AM - 11:00 PM",
    food_type: str = "Local Food",
    address: str = "",
    lat: Optional[float] = None,
    lng: Optional[float] = None,
    image_url: str = "",
    description: str = "",
    provider_id: str = "system"
) -> Dict[str, Any]:
    return {
        "_id": generate_id("rst"),
        "provider_id": provider_id,
        "name": name,
        "destination": destination,
        "cuisine": cuisine,
        "price_level": price_level,
        "avg_cost_per_person": avg_cost,
        "rating": rating,
        "opening_hours": opening_hours,
        "food_type": food_type,
        "address": address or f"Famous dining street, {destination}",
        "lat": lat,
        "lng": lng,
        "image_url": image_url or "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=800&q=80",
        "description": description or f"Top culinary spot in {destination} serving authentic dishes.",
        "created_at": now_iso()
    }

def create_transport_doc(
    transport_type: str,
    from_loc: str,
    to_loc: str,
    estimated_cost: float,
    duration: str,
    convenience: str = "High",
    vehicle_details: str = "",
    description: str = "",
    provider_id: str = "system"
) -> Dict[str, Any]:
    return {
        "_id": generate_id("trn"),
        "provider_id": provider_id,
        "type": transport_type,
        "from_location": from_loc,
        "to_location": to_loc,
        "cost": estimated_cost,
        "duration": duration,
        "convenience": convenience,
        "vehicle_details": vehicle_details,
        "description": description or f"Reliable {transport_type} transfer between {from_loc} and {to_loc}.",
        "created_at": now_iso()
    }

def create_activity_doc(
    name: str,
    destination: str,
    category: str,
    price: float,
    duration: str,
    image_url: str = "",
    description: str = "",
    lat: Optional[float] = None,
    lng: Optional[float] = None,
    provider_id: str = "system"
) -> Dict[str, Any]:
    return {
        "_id": generate_id("act"),
        "provider_id": provider_id,
        "name": name,
        "destination": destination,
        "category": category,
        "price": price,
        "duration": duration,
        "image_url": image_url or "https://images.unsplash.com/photo-1533105079780-92b9be482077?auto=format&fit=crop&w=800&q=80",
        "description": description or f"Exciting {category} experience in {destination}.",
        "lat": lat,
        "lng": lng,
        "created_at": now_iso()
    }

def create_booking_doc(
    user_id: str,
    user_name: str,
    user_email: str,
    provider_id: str,
    listing_id: str,
    listing_type: str,
    listing_name: str,
    trip_id: str = "",
    dates: str = "",
    guests: int = 1,
    total_price: float = 0.0,
    currency: str = "INR",
    status: str = "Pending",
    notes: str = ""
) -> Dict[str, Any]:
    return {
        "_id": generate_id("bkg"),
        "user_id": user_id,
        "user_name": user_name,
        "user_email": user_email,
        "provider_id": provider_id,
        "listing_id": listing_id,
        "listing_type": listing_type,
        "listing_name": listing_name,
        "trip_id": trip_id,
        "dates": dates,
        "guests": guests,
        "total_price": total_price,
        "currency": currency,
        "status": status,  # Pending, Confirmed, Rejected, Cancelled
        "notes": notes,
        "created_at": now_iso()
    }

def create_notification_doc(
    user_id: str,
    title: str,
    message: str,
    type_: str = "info"  # info, success, warning, alert
) -> Dict[str, Any]:
    return {
        "_id": generate_id("notif"),
        "user_id": user_id,
        "title": title,
        "message": message,
        "type": type_,
        "is_read": False,
        "created_at": now_iso()
    }

def create_review_doc(
    user_id: str,
    user_name: str,
    target_id: str,
    target_type: str,  # hotel, restaurant, activity, provider
    rating: int,
    comment: str
) -> Dict[str, Any]:
    return {
        "_id": generate_id("rev"),
        "user_id": user_id,
        "user_name": user_name,
        "target_id": target_id,
        "target_type": target_type,
        "rating": max(1, min(5, rating)),
        "comment": comment,
        "status": "approved",  # approved, flagged, removed
        "created_at": now_iso()
    }

def create_favorite_doc(
    user_id: str,
    item_id: str,
    item_type: str,  # hotel, restaurant, activity, destination
    title: str,
    image_url: str = "",
    destination: str = "",
    price_info: str = ""
) -> Dict[str, Any]:
    return {
        "_id": generate_id("fav"),
        "user_id": user_id,
        "item_id": item_id,
        "item_type": item_type,
        "title": title,
        "image_url": image_url,
        "destination": destination,
        "price_info": price_info,
        "created_at": now_iso()
    }
