# Constants for AI Smart Tourism & Travel Recommendation System

CURRENCIES = {
    "INR": {"symbol": "₹", "rate_to_inr": 1.0, "name": "Indian Rupee"},
    "USD": {"symbol": "$", "rate_to_inr": 83.5, "name": "US Dollar"},
    "EUR": {"symbol": "€", "rate_to_inr": 90.5, "name": "Euro"},
    "GBP": {"symbol": "£", "rate_to_inr": 106.0, "name": "British Pound"}
}

TRAVEL_STYLES = [
    "Budget",
    "Standard",
    "Luxury",
    "Backpacker",
    "Family",
    "Solo",
    "Couple"
]

INTERESTS = [
    "Historical Places",
    "Nature",
    "Beaches",
    "Adventure",
    "Food",
    "Shopping",
    "Culture",
    "Museums",
    "Religious Places",
    "Photography",
    "Nightlife",
    "Wildlife",
    "Architecture"
]

ACCOMMODATION_TYPES = [
    "Budget Hotel",
    "3 Star",
    "4 Star",
    "5 Star",
    "Hostel",
    "Homestay"
]

FOOD_PREFERENCES = [
    "Local Food",
    "Vegetarian",
    "Non-Vegetarian",
    "Vegan",
    "Fine Dining",
    "Street Food"
]

TRANSPORT_PREFERENCES = [
    "Public Transport",
    "Bus",
    "Train",
    "Taxi",
    "Rental Car",
    "Flight",
    "Mixed"
]

MOOD_OPTIONS = [
    "Relaxing",
    "Adventurous",
    "Romantic",
    "Spiritual",
    "Cultural",
    "Foodie",
    "Nature",
    "Photography"
]

PROVIDER_TYPES = [
    "Hotel",
    "Restaurant",
    "Transport",
    "Tour/Activity"
]

BOOKING_STATUSES = [
    "Pending",
    "Confirmed",
    "Rejected",
    "Cancelled"
]

USER_ROLES = [
    "Traveler",
    "Provider",
    "Admin"
]

# Initial Seed Destinations with High Quality Tourism Imagery & Genuine Coordinates
SEED_DESTINATIONS = [
    {
        "id": "dest-hyderabad",
        "name": "Hyderabad",
        "country": "India",
        "category": "Historical",
        "description": "The City of Pearls, famous for its grand Nizam heritage, iconic Charminar, historic Golconda Fort, and world-renowned Hyderabadi Biryani.",
        "image_url": "https://images.unsplash.com/photo-1605007493699-ce65834f8a00?auto=format&fit=crop&w=1000&q=80",
        "lat": 17.3850,
        "lng": 78.4867,
        "best_season": "October to March",
        "avg_budget_inr": 15000,
        "popularity_score": 4.8,
        "top_attractions": ["Charminar", "Golconda Fort", "Hussain Sagar Lake", "Ramoji Film City", "Salar Jung Museum", "Chowmahalla Palace"]
    },
    {
        "id": "dest-goa",
        "name": "Goa",
        "country": "India",
        "category": "Beach",
        "description": "India's premier coastal paradise, celebrated for sun-kissed golden beaches, Portuguese colonial architecture, vibrant water sports, and beachside shacks.",
        "image_url": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=1000&q=80",
        "lat": 15.2993,
        "lng": 74.1240,
        "best_season": "November to February",
        "avg_budget_inr": 22000,
        "popularity_score": 4.9,
        "top_attractions": ["Baga Beach", "Aguada Fort", "Basilica of Bom Jesus", "Dudhsagar Falls", "Anjuna Flea Market", "Palolem Beach"]
    },
    {
        "id": "dest-delhi",
        "name": "Delhi",
        "country": "India",
        "category": "Culture",
        "description": "India's pulsing historic capital blending ancient monuments like the Red Fort and Qutub Minar with bustling street food lanes of Chandni Chowk.",
        "image_url": "https://images.unsplash.com/photo-1587474260584-136574528ed5?auto=format&fit=crop&w=1000&q=80",
        "lat": 28.6139,
        "lng": 77.2090,
        "best_season": "October to March",
        "avg_budget_inr": 18000,
        "popularity_score": 4.7,
        "top_attractions": ["India Gate", "Red Fort", "Qutub Minar", "Humayun's Tomb", "Lotus Temple", "Chandni Chowk"]
    },
    {
        "id": "dest-jaipur",
        "name": "Jaipur",
        "country": "India",
        "category": "Historical",
        "description": "The regal Pink City of Rajasthan, steeped in royal splendor with majestic hilltop forts, ornate palaces like Hawa Mahal, and bustling craft bazaars.",
        "image_url": "https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=1000&q=80",
        "lat": 26.9124,
        "lng": 75.7873,
        "best_season": "October to March",
        "avg_budget_inr": 16000,
        "popularity_score": 4.8,
        "top_attractions": ["Hawa Mahal", "Amer Fort", "City Palace", "Jantar Mantar", "Nahargarh Fort", "Albert Hall Museum"]
    },
    {
        "id": "dest-mumbai",
        "name": "Mumbai",
        "country": "India",
        "category": "Culture",
        "description": "The City of Dreams, featuring colonial landmarks like Gateway of India, scenic Marine Drive, Bollywood culture, and delicious coastal street snacks.",
        "image_url": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?auto=format&fit=crop&w=1000&q=80",
        "lat": 18.9220,
        "lng": 72.8347,
        "best_season": "November to February",
        "avg_budget_inr": 25000,
        "popularity_score": 4.8,
        "top_attractions": ["Gateway of India", "Marine Drive", "Elephanta Caves", "Colaba Causeway", "Chhatrapati Shivaji Terminus", "Juhu Beach"]
    },
    {
        "id": "dest-kerala",
        "name": "Kerala",
        "country": "India",
        "category": "Nature",
        "description": "God's Own Country, globally renowned for serene backwaters in Alleppey, lush tea estates of Munnar, Ayurvedic sanctuaries, and tranquil coastline.",
        "image_url": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=1000&q=80",
        "lat": 9.9312,
        "lng": 76.2673,
        "best_season": "September to March",
        "avg_budget_inr": 24000,
        "popularity_score": 4.9,
        "top_attractions": ["Alleppey Backwaters", "Munnar Tea Gardens", "Periyar National Park", "Fort Kochi", "Varkala Cliff Beach", "Athirappilly Waterfalls"]
    },
    {
        "id": "dest-paris",
        "name": "Paris",
        "country": "France",
        "category": "Architecture",
        "description": "The City of Light, world capital of art, fashion, gastronomy and culture, home to the Eiffel Tower, the Louvre, and romantic Seine riverbanks.",
        "image_url": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&w=1000&q=80",
        "lat": 48.8566,
        "lng": 2.3522,
        "best_season": "April to October",
        "avg_budget_inr": 120000,
        "popularity_score": 4.9,
        "top_attractions": ["Eiffel Tower", "Louvre Museum", "Notre-Dame Cathedral", "Arc de Triomphe", "Montmartre", "Seine River Cruise"]
    },
    {
        "id": "dest-tokyo",
        "name": "Tokyo",
        "country": "Japan",
        "category": "Culture",
        "description": "A dazzling fusion of ultramodern neon skyscrapers and historic temples, cutting-edge anime culture, and the world's most Michelin-starred dining.",
        "image_url": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?auto=format&fit=crop&w=1000&q=80",
        "lat": 35.6762,
        "lng": 139.6503,
        "best_season": "March to May, September to November",
        "avg_budget_inr": 140000,
        "popularity_score": 4.9,
        "top_attractions": ["Sensō-ji Temple", "Shibuya Crossing", "Tokyo Skytree", "Meiji Shrine", "Akihabara", "Shinjuku Gyoen"]
    },
    {
        "id": "dest-dubai",
        "name": "Dubai",
        "country": "UAE",
        "category": "Adventure",
        "description": "Futuristic desert metropolis known for luxury shopping, ultramodern architecture including Burj Khalifa, desert safaris, and lively nightlife.",
        "image_url": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=1000&q=80",
        "lat": 25.2048,
        "lng": 55.2708,
        "best_season": "November to March",
        "avg_budget_inr": 85000,
        "popularity_score": 4.8,
        "top_attractions": ["Burj Khalifa", "The Dubai Mall", "Palm Jumeirah", "Desert Safari Dunes", "Dubai Marina", "Museum of the Future"]
    },
    {
        "id": "dest-london",
        "name": "London",
        "country": "UK",
        "category": "Historical",
        "description": "Timeless global capital on the River Thames, steeped in two millennia of history alongside royal palaces, world-class museums, and West End theater.",
        "image_url": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?auto=format&fit=crop&w=1000&q=80",
        "lat": 51.5074,
        "lng": -0.1278,
        "best_season": "May to September",
        "avg_budget_inr": 130000,
        "popularity_score": 4.8,
        "top_attractions": ["Big Ben & Parliament", "Tower of London", "British Museum", "London Eye", "Buckingham Palace", "Trafalgar Square"]
    }
]
