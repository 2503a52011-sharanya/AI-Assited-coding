import hashlib
import logging
from typing import Dict, Any, List, Optional
from database.connection import get_db_collection, db_manager
from database.models import (
    create_user_doc, create_trip_doc, create_hotel_doc,
    create_restaurant_doc, create_transport_doc, create_activity_doc,
    create_booking_doc, create_notification_doc, create_review_doc,
    create_favorite_doc, now_iso
)
from config.settings import settings
from config.constants import SEED_DESTINATIONS

logger = logging.getLogger(__name__)

def hash_password(password: str) -> str:
    """Generate SHA-256 hash with salt for secure storage."""
    salt = settings.JWT_SECRET[:12]
    return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password

class Repository:
    """Central repository implementing clean data operations across all 14 collections."""

    @staticmethod
    def initialize_seeds():
        """Ensure default admin, seed destinations, and sample listings exist."""
        # 1. Seed Admin
        users_col = get_db_collection("users")
        admin = users_col.find_one({"email": settings.ADMIN_EMAIL})
        if not admin:
            admin_doc = create_user_doc(
                email=settings.ADMIN_EMAIL,
                password_hash=hash_password(settings.ADMIN_PASSWORD),
                full_name="System Administrator",
                role="Admin"
            )
            users_col.insert_one(admin_doc)

        # 2. Seed Sample Provider
        provider_email = "provider@tajhotels.com"
        provider = users_col.find_one({"email": provider_email})
        if not provider:
            provider_doc = create_user_doc(
                email=provider_email,
                password_hash=hash_password("Provider@123"),
                full_name="Rajesh Sharma (Taj Stays)",
                role="Provider",
                phone="+91 9876543210",
                provider_business_name="Taj Heritage & Luxury Stays",
                provider_type="Hotel"
            )
            provider_doc["provider_approved"] = True
            users_col.insert_one(provider_doc)
            provider_id = provider_doc["_id"]
        else:
            provider_id = provider["_id"]

        # 3. Seed Sample Traveler
        traveler_email = "traveler@example.com"
        traveler = users_col.find_one({"email": traveler_email})
        if not traveler:
            traveler_doc = create_user_doc(
                email=traveler_email,
                password_hash=hash_password("Traveler@123"),
                full_name="Aarav Mehta",
                role="Traveler",
                phone="+91 9123456780"
            )
            users_col.insert_one(traveler_doc)

        # 4. Seed Destinations
        dest_col = get_db_collection("destinations")
        for d in SEED_DESTINATIONS:
            if not dest_col.find_one({"name": d["name"]}):
                dest_col.insert_one(dict(d))

        # 5. Seed Sample Hotels
        hotel_col = get_db_collection("hotels")
        if hotel_col.count_documents({}) == 0:
            sample_hotels = [
                create_hotel_doc(
                    name="Taj Falaknuma Palace",
                    destination="Hyderabad",
                    room_type="Palace Luxury Suite",
                    price_per_night=32000,
                    star_rating=5,
                    guest_rating=4.9,
                    amenities=["Heritage Architecture", "Fine Dining", "Royal Spa", "Free High-Speed WiFi", "Butler Service"],
                    address="Engine Bowli, Fatima Nagar, Falaknuma, Hyderabad",
                    lat=17.3314, lng=78.4674,
                    image_url="https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=800&q=80",
                    description="Perched 2,000 feet above Hyderabad, Falaknuma Palace is the former residence of the Nizam.",
                    provider_id=provider_id
                ),
                create_hotel_doc(
                    name="ITC Kohenur",
                    destination="Hyderabad",
                    room_type="Executive Lake View Room",
                    price_per_night=12500,
                    star_rating=5,
                    guest_rating=4.8,
                    amenities=["Infinity Pool", "Durgam Cheruvu View", "Multi-cuisine", "Fitness Center"],
                    address="HITEC City, Madhapur, Hyderabad",
                    lat=17.4339, lng=78.3842,
                    image_url="https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80",
                    description="Overlooking the freshwater Durgam Cheruvu Lake, offering culinary excellence.",
                    provider_id=provider_id
                ),
                create_hotel_doc(
                    name="The Leela Goa",
                    destination="Goa",
                    room_type="Lagoon Terrace Room",
                    price_per_night=21000,
                    star_rating=5,
                    guest_rating=4.8,
                    amenities=["Private Beach Access", "12-hole Golf Course", "Ayurvedic Spa", "Beach Shack"],
                    address="Mobor Beach, Cavelossim, South Goa",
                    lat=15.1610, lng=73.9450,
                    image_url="https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=800&q=80",
                    description="Spread across 75 lush acres of pristine coastal garden and secluded beach.",
                    provider_id=provider_id
                ),
                create_hotel_doc(
                    name="The Oberoi New Delhi",
                    destination="Delhi",
                    room_type="Premier Golf View Room",
                    price_per_night=19500,
                    star_rating=5,
                    guest_rating=4.9,
                    amenities=["Rooftop Bar", "Delhi Golf Club Views", "Indoor & Outdoor Pools", "Pure Air Filtration"],
                    address="Dr. Zakir Hussain Marg, New Delhi",
                    lat=28.5997, lng=77.2405,
                    image_url="https://images.unsplash.com/photo-1571896349842-33c89424de2d?auto=format&fit=crop&w=800&q=80",
                    description="Iconic luxury landmark in central Delhi overlooking the lush Delhi Golf Club greens.",
                    provider_id=provider_id
                ),
                create_hotel_doc(
                    name="Rambagh Palace",
                    destination="Jaipur",
                    room_type="Royal Palace Suite",
                    price_per_night=38000,
                    star_rating=5,
                    guest_rating=5.0,
                    amenities=["Peacock Garden", "Royal Carriage Rides", "Jiva Grande Spa", "Polo Bar"],
                    address="Bhawani Singh Road, Jaipur",
                    lat=26.8979, lng=75.8078,
                    image_url="https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?auto=format&fit=crop&w=800&q=80",
                    description="Known as the Jewel of Jaipur, former residence of the Maharaja of Jaipur.",
                    provider_id=provider_id
                ),
                create_hotel_doc(
                    name="The Taj Mahal Palace",
                    destination="Mumbai",
                    room_type="Gateway Suite",
                    price_per_night=28000,
                    star_rating=5,
                    guest_rating=4.9,
                    amenities=["Arabian Sea Views", "Harbour View Dining", "Jiva Spa", "Historic Heritage Wing"],
                    address="Apollo Bunder, Colaba, Mumbai",
                    lat=18.9217, lng=72.8332,
                    image_url="https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?auto=format&fit=crop&w=800&q=80",
                    description="Grand 1903 heritage hotel standing proudly opposite the Gateway of India.",
                    provider_id=provider_id
                ),
                create_hotel_doc(
                    name="Kumarakom Lake Resort",
                    destination="Kerala",
                    room_type="Heritage Lake Villa with Private Pool",
                    price_per_night=22000,
                    star_rating=5,
                    guest_rating=4.8,
                    amenities=["Vembanad Lake Cruises", "Traditional Kerala Architecture", "Ayurvedic Spa"],
                    address="Kumarakom, Kottayam, Kerala",
                    lat=9.6175, lng=76.4300,
                    image_url="https://images.unsplash.com/photo-1578683010236-d716f9a3f461?auto=format&fit=crop&w=800&q=80",
                    description="Nestled alongside Lake Vembanad with reconstructed 16th-century traditional manors.",
                    provider_id=provider_id
                )
            ]
            for h in sample_hotels:
                hotel_col.insert_one(h)

        # 6. Seed Sample Restaurants
        rest_col = get_db_collection("restaurants")
        if rest_col.count_documents({}) == 0:
            sample_restaurants = [
                create_restaurant_doc("Paradise Biryani", "Hyderabad", "Hyderabadi / Indian", "$$", 600, 4.7, "11:30 AM - 11:30 PM", "Non-Vegetarian", "Secunderabad, Hyderabad", 17.4411, 78.4983, "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?auto=format&fit=crop&w=800&q=80", "World-renowned Hyderabadi Dum Biryani and tender kebabs."),
                create_restaurant_doc("Bawarchi Restaurant", "Hyderabad", "Mughlai & Biryani", "$$", 550, 4.6, "12:00 PM - 11:00 PM", "Non-Vegetarian", "RTC X Roads, Hyderabad", 17.4062, 78.4985, "https://images.unsplash.com/photo-1633945274405-b6c8069047b0?auto=format&fit=crop&w=800&q=80", "Authentic spicy mutton biryani beloved by Hyderabad locals."),
                create_restaurant_doc("Fisherman's Wharf", "Goa", "Goan & Coastal Seafood", "$$$", 1200, 4.8, "12:30 PM - 11:00 PM", "Non-Vegetarian", "Cavelossim, South Goa", 15.1764, 73.9452, "https://images.unsplash.com/photo-1559339352-11d035aa65de?auto=format&fit=crop&w=800&q=80", "Riverside dining serving Goan fish curry, butter garlic prawns, and crab xec xec."),
                create_restaurant_doc("Karim's Historic Old Delhi", "Delhi", "Mughlai & Kebabs", "$$", 700, 4.7, "11:00 AM - 11:30 PM", "Non-Vegetarian", "Gali Kababian, Jama Masjid, Delhi", 28.6507, 77.2334, "https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=800&q=80", "Legendary royal recipes handed down from the Mughal imperial kitchens."),
                create_restaurant_doc("1135 AD", "Jaipur", "Rajasthani Royal Dining", "$$$$", 2400, 4.9, "12:00 PM - 10:30 PM", "Local Food", "Amer Fort, Jaipur", 26.9855, 75.8513, "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=800&q=80", "Dine inside Amer Fort surrounded by silver furnishings and gold leaf enamel."),
                create_restaurant_doc("Britannia & Co.", "Mumbai", "Parsi & Iranian", "$$", 750, 4.6, "11:30 AM - 04:00 PM", "Local Food", "Ballard Estate, Fort, Mumbai", 18.9351, 72.8402, "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=800&q=80", "Legendary Parsi cafe famed for Berry Pulao, Sali Boti, and caramel custard.")
            ]
            for r in sample_restaurants:
                rest_col.insert_one(r)

        # 7. Seed Sample Transportation
        trans_col = get_db_collection("transportation")
        if trans_col.count_documents({}) == 0:
            sample_trans = [
                create_transport_doc("Flight", "Hyderabad", "Goa", 4500, "1h 15m", "High", "Airbus A320 / Indigo, Air India Express", "Fastest direct connection between Hyderabad and Dabolim/MOPA airport."),
                create_transport_doc("Train", "Hyderabad", "Goa", 1400, "15h 30m", "Medium", "Vasco Express (AC 2-Tier)", "Scenic train journey traversing the Western Ghats and Dudhsagar falls."),
                create_transport_doc("Flight", "Delhi", "Jaipur", 3200, "50m", "High", "ATR 72 / Alliance Air", "Quick aerial hop between the capital and the Pink City."),
                create_transport_doc("Train", "Delhi", "Jaipur", 950, "4h 10m", "High", "Vande Bharat Express (Chair Car)", "Superfast premium train with breakfast service."),
                create_transport_doc("Taxi / Private Cab", "Delhi", "Jaipur", 4500, "5h 00m", "High", "Sedan / SUV with AC", "Door-to-door highway travel via Delhi-Jaipur Expressway.")
            ]
            for t in sample_trans:
                trans_col.insert_one(t)

        # 8. Seed Sample Notifications
        notif_col = get_db_collection("notifications")
        if notif_col.count_documents({}) == 0:
            notif_col.insert_one(create_notification_doc(
                user_id="all",
                title="Welcome to AI Smart Tourism!",
                message="Your intelligent travel companion is ready. Discover customized itineraries and budget optimization.",
                type_="info"
            ))

    # --- User Management ---
    @staticmethod
    def create_user(data: Dict[str, Any]) -> Dict[str, Any]:
        users_col = get_db_collection("users")
        if users_col.find_one({"email": data["email"].strip().lower()}):
            raise ValueError(f"User with email {data['email']} already exists.")
        doc = create_user_doc(
            email=data["email"],
            password_hash=hash_password(data["password"]),
            full_name=data["full_name"],
            role=data.get("role", "Traveler"),
            phone=data.get("phone", ""),
            provider_business_name=data.get("provider_business_name", ""),
            provider_type=data.get("provider_type", "")
        )
        users_col.insert_one(doc)
        return doc

    @staticmethod
    def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
        users_col = get_db_collection("users")
        user = users_col.find_one({"email": email.strip().lower()})
        if user and verify_password(password, user["password_hash"]):
            if not user.get("is_active", True):
                raise ValueError("Your account is currently suspended. Please contact admin.")
            if user.get("role") == "Provider" and not user.get("provider_approved", False):
                raise ValueError("Provider account is pending Admin approval.")
            return user
        return None

    @staticmethod
    def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
        return get_db_collection("users").find_one({"_id": user_id})

    @staticmethod
    def list_users(role: Optional[str] = None) -> List[Dict[str, Any]]:
        query = {"role": role} if role else {}
        return list(get_db_collection("users").find(query))

    @staticmethod
    def update_user_status(user_id: str, is_active: bool) -> bool:
        res = get_db_collection("users").update_one(
            {"_id": user_id},
            {"$set": {"is_active": is_active}}
        )
        return res.modified_count > 0

    @staticmethod
    def approve_provider(user_id: str, approved: bool) -> bool:
        res = get_db_collection("users").update_one(
            {"_id": user_id},
            {"$set": {"provider_approved": approved}}
        )
        return res.modified_count > 0

    @staticmethod
    def delete_user(user_id: str) -> bool:
        res = get_db_collection("users").delete_one({"_id": user_id})
        return res.deleted_count > 0

    # --- Trip Management ---
    @staticmethod
    def save_trip(trip_doc: Dict[str, Any]) -> str:
        trips_col = get_db_collection("trips")
        trips_col.insert_one(trip_doc)
        # Create notification for trip creation
        Repository.create_notification(
            user_id=trip_doc["user_id"],
            title=f"Trip Created: {trip_doc['destination']}",
            message=f"Your {trip_doc['days']}-day trip to {trip_doc['destination']} is saved and ready.",
            type_="success"
        )
        return trip_doc["_id"]

    @staticmethod
    def get_trip(trip_id: str) -> Optional[Dict[str, Any]]:
        return get_db_collection("trips").find_one({"_id": trip_id})

    @staticmethod
    def get_user_trips(user_id: str) -> List[Dict[str, Any]]:
        return list(get_db_collection("trips").find({"user_id": user_id}).sort("created_at", -1))

    @staticmethod
    def delete_trip(trip_id: str, user_id: Optional[str] = None) -> bool:
        query = {"_id": trip_id}
        if user_id:
            query["user_id"] = user_id
        res = get_db_collection("trips").delete_one(query)
        return res.deleted_count > 0

    # --- Destinations ---
    @staticmethod
    def list_destinations(category: Optional[str] = None, search: Optional[str] = None) -> List[Dict[str, Any]]:
        dest_col = get_db_collection("destinations")
        query = {}
        if category and category != "All":
            query["category"] = category
        if search:
            query["name"] = {"$regex": search, "$options": "i"}
        return list(dest_col.find(query))

    @staticmethod
    def get_destination_by_name(name: str) -> Optional[Dict[str, Any]]:
        dest_col = get_db_collection("destinations")
        return dest_col.find_one({"name": {"$regex": f"^{name.strip()}$", "$options": "i"}})

    @staticmethod
    def add_destination(dest_data: Dict[str, Any]) -> str:
        dest_col = get_db_collection("destinations")
        dest_col.insert_one(dest_data)
        return dest_data["_id"]

    # --- Hotels ---
    @staticmethod
    def list_hotels(destination: Optional[str] = None, max_price: Optional[float] = None, min_stars: Optional[int] = None) -> List[Dict[str, Any]]:
        hotels_col = get_db_collection("hotels")
        query = {}
        if destination and destination.strip():
            query["destination"] = {"$regex": destination.strip(), "$options": "i"}
        if max_price:
            query["price_per_night"] = {"$lte": max_price}
        if min_stars:
            query["star_rating"] = {"$gte": min_stars}
        return list(hotels_col.find(query))

    @staticmethod
    def get_hotel_by_id(hotel_id: str) -> Optional[Dict[str, Any]]:
        return get_db_collection("hotels").find_one({"_id": hotel_id})

    @staticmethod
    def add_hotel(hotel_data: Dict[str, Any]) -> str:
        return get_db_collection("hotels").insert_one(hotel_data).inserted_id

    @staticmethod
    def update_hotel(hotel_id: str, updates: Dict[str, Any]) -> bool:
        res = get_db_collection("hotels").update_one({"_id": hotel_id}, {"$set": updates})
        return res.modified_count > 0

    @staticmethod
    def delete_hotel(hotel_id: str, provider_id: Optional[str] = None) -> bool:
        query = {"_id": hotel_id}
        if provider_id and provider_id != "admin":
            query["provider_id"] = provider_id
        res = get_db_collection("hotels").delete_one(query)
        return res.deleted_count > 0

    # --- Restaurants ---
    @staticmethod
    def list_restaurants(destination: Optional[str] = None, cuisine: Optional[str] = None, food_pref: Optional[str] = None) -> List[Dict[str, Any]]:
        rest_col = get_db_collection("restaurants")
        query = {}
        if destination and destination.strip():
            query["destination"] = {"$regex": destination.strip(), "$options": "i"}
        if cuisine and cuisine != "All":
            query["cuisine"] = {"$regex": cuisine, "$options": "i"}
        if food_pref and food_pref != "All":
            query["food_type"] = food_pref
        return list(rest_col.find(query))

    @staticmethod
    def add_restaurant(rest_data: Dict[str, Any]) -> str:
        return get_db_collection("restaurants").insert_one(rest_data).inserted_id

    # --- Transportation ---
    @staticmethod
    def list_transports(from_loc: Optional[str] = None, to_loc: Optional[str] = None) -> List[Dict[str, Any]]:
        trans_col = get_db_collection("transportation")
        query = {}
        if from_loc and from_loc.strip():
            query["from_location"] = {"$regex": from_loc.strip(), "$options": "i"}
        if to_loc and to_loc.strip():
            query["to_location"] = {"$regex": to_loc.strip(), "$options": "i"}
        return list(trans_col.find(query))

    @staticmethod
    def add_transport(trans_data: Dict[str, Any]) -> str:
        return get_db_collection("transportation").insert_one(trans_data).inserted_id

    # --- Bookings & Provider Workflow ---
    @staticmethod
    def create_booking(booking_data: Dict[str, Any]) -> str:
        bkg_col = get_db_collection("bookings")
        bkg_col.insert_one(booking_data)
        
        # Notify provider
        Repository.create_notification(
            user_id=booking_data["provider_id"],
            title="New Booking Request Received",
            message=f"New request for {booking_data['listing_name']} from {booking_data['user_name']}.",
            type_="info"
        )
        # Notify traveler
        Repository.create_notification(
            user_id=booking_data["user_id"],
            title="Booking Request Submitted",
            message=f"Your booking request for {booking_data['listing_name']} is currently Pending confirmation.",
            type_="warning"
        )
        return booking_data["_id"]

    @staticmethod
    def update_booking_status(booking_id: str, new_status: str, provider_id: Optional[str] = None) -> bool:
        bkg_col = get_db_collection("bookings")
        query = {"_id": booking_id}
        if provider_id and provider_id != "admin":
            query["provider_id"] = provider_id
            
        booking = bkg_col.find_one(query)
        if not booking:
            return False

        res = bkg_col.update_one(query, {"$set": {"status": new_status, "updated_at": now_iso()}})
        if res.modified_count > 0:
            # Notify traveler of confirmation or rejection
            type_map = {"Confirmed": "success", "Rejected": "alert", "Cancelled": "warning"}
            Repository.create_notification(
                user_id=booking["user_id"],
                title=f"Booking {new_status}: {booking['listing_name']}",
                message=f"Your booking request for {booking['listing_name']} has been {new_status.lower()}.",
                type_=type_map.get(new_status, "info")
            )
            return True
        return False

    @staticmethod
    def get_user_bookings(user_id: str) -> List[Dict[str, Any]]:
        return list(get_db_collection("bookings").find({"user_id": user_id}).sort("created_at", -1))

    @staticmethod
    def get_provider_bookings(provider_id: str) -> List[Dict[str, Any]]:
        return list(get_db_collection("bookings").find({"provider_id": provider_id}).sort("created_at", -1))

    @staticmethod
    def list_all_bookings() -> List[Dict[str, Any]]:
        return list(get_db_collection("bookings").find({}).sort("created_at", -1))

    # --- Reviews ---
    @staticmethod
    def add_review(review_data: Dict[str, Any]) -> str:
        rev_col = get_db_collection("reviews")
        rev_col.insert_one(review_data)
        return review_data["_id"]

    @staticmethod
    def get_reviews_for_target(target_id: str) -> List[Dict[str, Any]]:
        return list(get_db_collection("reviews").find({"target_id": target_id, "status": "approved"}))

    @staticmethod
    def list_all_reviews() -> List[Dict[str, Any]]:
        return list(get_db_collection("reviews").find({}).sort("created_at", -1))

    @staticmethod
    def moderate_review(review_id: str, new_status: str) -> bool:
        res = get_db_collection("reviews").update_one(
            {"_id": review_id},
            {"$set": {"status": new_status}}
        )
        return res.modified_count > 0

    # --- Favorites ---
    @staticmethod
    def toggle_favorite(user_id: str, item_id: str, item_type: str, title: str, image_url: str = "", destination: str = "", price_info: str = "") -> bool:
        fav_col = get_db_collection("favorites")
        existing = fav_col.find_one({"user_id": user_id, "item_id": item_id})
        if existing:
            fav_col.delete_one({"_id": existing["_id"]})
            return False  # Unfavorited
        else:
            fav_doc = create_favorite_doc(user_id, item_id, item_type, title, image_url, destination, price_info)
            fav_col.insert_one(fav_doc)
            return True  # Favorited

    @staticmethod
    def is_favorite(user_id: str, item_id: str) -> bool:
        return get_db_collection("favorites").find_one({"user_id": user_id, "item_id": item_id}) is not None

    @staticmethod
    def get_user_favorites(user_id: str, item_type: Optional[str] = None) -> List[Dict[str, Any]]:
        query = {"user_id": user_id}
        if item_type and item_type != "All":
            query["item_type"] = item_type
        return list(get_db_collection("favorites").find(query).sort("created_at", -1))

    # --- Notifications ---
    @staticmethod
    def create_notification(user_id: str, title: str, message: str, type_: str = "info") -> str:
        notif_doc = create_notification_doc(user_id, title, message, type_)
        get_db_collection("notifications").insert_one(notif_doc)
        return notif_doc["_id"]

    @staticmethod
    def get_user_notifications(user_id: str) -> List[Dict[str, Any]]:
        query = {"$or": [{"user_id": user_id}, {"user_id": "all"}]}
        return list(get_db_collection("notifications").find(query).sort("created_at", -1))

    @staticmethod
    def mark_notifications_read(user_id: str):
        get_db_collection("notifications").update_one(
            {"user_id": user_id},
            {"$set": {"is_read": True}}
        )

    # --- Dashboard KPI Aggregators ---
    @staticmethod
    def get_admin_kpis() -> Dict[str, Any]:
        return {
            "total_users": get_db_collection("users").count_documents({"role": "Traveler"}),
            "active_providers": get_db_collection("users").count_documents({"role": "Provider", "provider_approved": True}),
            "total_trips": get_db_collection("trips").count_documents({}),
            "total_bookings": get_db_collection("bookings").count_documents({}),
            "confirmed_bookings": get_db_collection("bookings").count_documents({"status": "Confirmed"}),
            "total_revenue": sum(b.get("total_price", 0) for b in get_db_collection("bookings").find({"status": "Confirmed"})),
            "popular_destination": "Hyderabad"
        }

    @staticmethod
    def get_provider_kpis(provider_id: str) -> Dict[str, Any]:
        hotels_count = get_db_collection("hotels").count_documents({"provider_id": provider_id})
        rests_count = get_db_collection("restaurants").count_documents({"provider_id": provider_id})
        trans_count = get_db_collection("transportation").count_documents({"provider_id": provider_id})
        bookings = list(get_db_collection("bookings").find({"provider_id": provider_id}))
        confirmed = [b for b in bookings if b.get("status") == "Confirmed"]
        total_revenue = sum(b.get("total_price", 0) for b in confirmed)

        return {
            "total_listings": hotels_count + rests_count + trans_count,
            "total_bookings": len(bookings),
            "confirmed_bookings": len(confirmed),
            "pending_bookings": sum(1 for b in bookings if b.get("status") == "Pending"),
            "revenue": total_revenue,
            "avg_rating": 4.8
        }

    @staticmethod
    def get_traveler_kpis(user_id: str) -> Dict[str, Any]:
        trips = list(get_db_collection("trips").find({"user_id": user_id}))
        favs_count = get_db_collection("favorites").count_documents({"user_id": user_id})
        upcoming_trips = [t for t in trips if t.get("status") == "Upcoming"]
        bookings = list(get_db_collection("bookings").find({"user_id": user_id}))

        return {
            "trips_planned": len(trips),
            "favorites_count": favs_count,
            "upcoming_trip": upcoming_trips[0]["destination"] if upcoming_trips else "None",
            "total_bookings": len(bookings)
        }

# Trigger seed initialization on module load
Repository.initialize_seeds()
