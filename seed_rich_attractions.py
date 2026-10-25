import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_tourism.settings')
django.setup()

from decimal import Decimal
from apps.destinations.models import Destination, TouristAttraction

def seed_rich_attractions():
    print("[Seed] Populating rich catalog of unique attractions for Goa, Jaipur, and Kerala...")

    # Fetch Destinations
    dest_goa = Destination.objects.filter(name='Goa').first()
    dest_jaipur = Destination.objects.filter(name='Jaipur').first()
    dest_kerala = Destination.objects.filter(name__icontains='Kerala').first()

    # --- GOA ATTRACTIONS (12 Distinct Places) ---
    goa_attractions = [
        ('Aguada Fort & Lighthouse', 'Heritage', '17th-century Portuguese fortress with sweeping Arabian Sea views.', 'https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80', 15.4920, 73.7738, 50.00, 2.0, False, False, 4.6),
        ('Calangute & Baga Beachfront', 'Nature', 'Iconic coastline for watersports, beach shacks, and tropical ocean waves.', 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80', 15.5440, 73.7554, 0.00, 3.0, False, False, 4.4),
        ('Museum of Christian Art & Convent', 'Museum', 'Sheltered indoor gallery showcasing Indo-Portuguese sacred relics and silver art.', 'https://images.unsplash.com/photo-1544644181-1484b3fdfc62?auto=format&fit=crop&w=800&q=80', 15.5034, 73.9118, 150.00, 2.5, True, True, 4.7),
        ('Basilica of Bom Jesus', 'Religious', 'UNESCO World Heritage baroque church holding the sacred relics of St. Francis Xavier.', 'https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=800&q=80', 15.5009, 73.9116, 0.00, 1.5, True, True, 4.8),
        ('Chapora Fort (Dil Chahta Hai Point)', 'Heritage', 'Promontory fort perched high above the Vagator coastline offering panoramic sunset views.', 'https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=800&q=80', 15.6058, 73.7371, 0.00, 2.0, False, False, 4.5),
        ('Houses of Goa Architecture Museum', 'Museum', 'Unique multi-level triangular museum celebrating Portuguese-Goan domestic architecture.', 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=800&q=80', 15.5262, 73.8449, 100.00, 2.0, True, True, 4.6),
        ('Dudhsagar Cascading Waterfalls', 'Adventure', 'Magnificent four-tiered white waterfall flowing through Bhagwan Mahavir Wildlife Sanctuary.', 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80', 15.3144, 74.3143, 400.00, 4.0, False, False, 4.9),
        ('Fontainhas Latin Quarter', 'Heritage', 'Quaint heritage quarter featuring vibrant pastel Portuguese villas and artisan cafes.', 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80', 15.4989, 73.8278, 0.00, 2.5, False, True, 4.7),
        ('Sahakari Spice Farm & Botanical Plantation', 'Nature', 'Guided plantation tour through cardamoms, vanilla, and peri-peri with indoor Goan lunch.', 'https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=800&q=80', 15.4184, 74.0202, 500.00, 3.0, True, True, 4.5),
        ('Anjuna Wednesday Flea Market', 'Shopping', 'Lively beachside bazaar with handcrafted jewelry, bohemian clothes, and music.', 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=800&q=80', 15.5786, 73.7431, 0.00, 2.0, False, False, 4.3),
        ('Reis Magos Fort on Mandovi River', 'Heritage', 'Restored 16th-century fortress and cultural center with high ramparts overlooking Panaji.', 'https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80', 15.5036, 73.8094, 50.00, 1.5, True, True, 4.6),
        ('Mandovi River Sunset Catamaran Cruise', 'Relaxation', 'Gentle evening river cruise with traditional Goan folk performances and susegad vibes.', 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?auto=format&fit=crop&w=800&q=80', 15.5015, 73.8252, 600.00, 2.0, False, False, 4.7),
    ]

    for name, cat, desc, img, lat, lng, fee, hours, indoor, rain, rating in goa_attractions:
        TouristAttraction.objects.update_or_create(
            destination=dest_goa,
            name=name,
            defaults={
                'category': cat,
                'description': desc,
                'image_url': img,
                'latitude': Decimal(str(lat)),
                'longitude': Decimal(str(lng)),
                'entry_fee': Decimal(str(fee)),
                'typical_time_spent_hours': Decimal(str(hours)),
                'is_indoor': indoor,
                'rain_friendly': rain,
                'rating': Decimal(str(rating))
            }
        )

    # --- JAIPUR ATTRACTIONS (12 Distinct Places) ---
    jaipur_attractions = [
        ('Amer Fort & Palace Grounds', 'Heritage', 'Red sandstone and marble hill fort featuring the ornate Mirror Palace (Sheesh Mahal).', 'https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=800&q=80', 26.9855, 75.8513, 200.00, 3.0, False, False, 4.9),
        ('Albert Hall Central Museum', 'Museum', 'Indo-Saracenic museum housing royal miniatures, carpets, and ancient Egyptian artifacts.', 'https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80', 26.9115, 75.8194, 150.00, 2.5, True, True, 4.8),
        ('City Palace & Chandra Mahal', 'Heritage', 'Sprawling palace complex with covered royal textile galleries and the Peacock Gate.', 'https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=800&q=80', 26.9258, 75.8237, 300.00, 2.0, True, True, 4.7),
        ('Hawa Mahal (Palace of Winds)', 'Heritage', 'Iconic five-story pink sandstone facade with 953 ornate latticed jharokhas.', 'https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80', 26.9239, 75.8267, 50.00, 1.5, False, True, 4.6),
        ('Jantar Mantar Astronomical Observatory', 'Heritage', 'UNESCO-listed collection of nineteen architectural astronomical instruments.', 'https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=800&q=80', 26.9248, 75.8246, 100.00, 2.0, False, False, 4.7),
        ('Nahargarh Fort Sunset Viewpoint', 'Adventure', 'Hilltop fortress perched on the Aravalli hills with a breathtaking panorama of Jaipur.', 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80', 26.9378, 75.8156, 100.00, 2.5, False, False, 4.8),
        ('Jal Mahal (Water Palace Promenade)', 'Nature', 'Serene water palace appearing to float in the center of Man Sagar Lake.', 'https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80', 26.9535, 75.8462, 0.00, 1.5, False, False, 4.5),
        ('Johari & Bapu Covered Bazaars', 'Shopping', 'Vibrant traditional pink arcade selling silver jewelry, jaipuri quilts, and bandhani.', 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=800&q=80', 26.9197, 75.8236, 0.00, 2.0, True, True, 4.4),
        ('Chokhi Dhani Ethnic Village Resort', 'Food', 'Immersive Rajasthani village fair with folk dancers, camel rides, and royal thali feast.', 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80', 26.7663, 75.8364, 850.00, 3.5, True, True, 4.7),
        ('Jaigarh Fort & Jaivana Cannon', 'Heritage', 'Massive fortress housing the world\'s largest cannon on wheels and subterranean armory.', 'https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=800&q=80', 26.9850, 75.8456, 150.00, 2.0, False, False, 4.6),
        ('Galtaji Temple (Monkey Valley Shrine)', 'Religious', 'Historic Hindu pilgrimage complex set in a mountain pass with natural sacred water kunds.', 'https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=800&q=80', 26.9161, 75.8582, 0.00, 2.0, False, False, 4.5),
        ('Birla Mandir at Moti Dungri', 'Religious', 'Pure white marble temple dedicated to Lakshmi Narayan, glowing spectacularly at dusk.', 'https://images.unsplash.com/photo-1544644181-1484b3fdfc62?auto=format&fit=crop&w=800&q=80', 26.8923, 75.8153, 0.00, 1.5, True, True, 4.7),
    ]

    for name, cat, desc, img, lat, lng, fee, hours, indoor, rain, rating in jaipur_attractions:
        TouristAttraction.objects.update_or_create(
            destination=dest_jaipur,
            name=name,
            defaults={
                'category': cat,
                'description': desc,
                'image_url': img,
                'latitude': Decimal(str(lat)),
                'longitude': Decimal(str(lng)),
                'entry_fee': Decimal(str(fee)),
                'typical_time_spent_hours': Decimal(str(hours)),
                'is_indoor': indoor,
                'rain_friendly': rain,
                'rating': Decimal(str(rating))
            }
        )

    # --- KERALA BACKWATERS (12 Distinct Places) ---
    kerala_attractions = [
        ('Alleppey Punnamada Houseboat Pier', 'Nature', 'Departure terminal for serene backwater cruises on traditional kettuvallam boats.', 'https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=800&q=80', 9.5085, 76.3533, 500.00, 3.5, False, False, 4.9),
        ('Kerala Folklore Museum (Kochi)', 'Museum', 'Architectural marvel combining Malabar, Cochin, and Travancore woodwork with thousands of masks.', 'https://images.unsplash.com/photo-1544644181-1484b3fdfc62?auto=format&fit=crop&w=800&q=80', 9.9298, 76.3117, 200.00, 2.5, True, True, 4.8),
        ('Mattancherry Dutch Palace', 'Heritage', 'Historic palace renowned for vivid Hindu mythological murals depicting the Ramayana.', 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=800&q=80', 9.9583, 76.2592, 50.00, 1.5, True, True, 4.6),
        ('Marari Palm Beach & Fisher Village', 'Nature', 'Quiet white sand beach lined with coconut groves and organic ayurvedic retreat shacks.', 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80', 9.6015, 76.2995, 0.00, 2.5, False, False, 4.7),
        ('Kumarakom Bird Sanctuary Trail', 'Nature', 'Lush wetland sanctuary on Vembanad Lake, home to migratory Siberian storks and herons.', 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80', 9.6267, 76.4307, 100.00, 2.5, False, False, 4.6),
        ('Pathiramanal Island Sanctuary', 'Nature', 'Picturesque birding island in Vembanad Lake accessible only by traditional motorboat.', 'https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=800&q=80', 9.6192, 76.3881, 150.00, 2.0, False, False, 4.5),
        ('Fort Kochi Chinese Fishing Nets', 'Heritage', 'Cantilevered mechanical fishing structures dating back to 14th-century trade routes.', 'https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=800&q=80', 9.9674, 76.2427, 0.00, 1.5, False, True, 4.7),
        ('Krishnapuram Palace Museum', 'Heritage', '18th-century Travancore residence housing the famous Gajendra Moksham mural painting.', 'https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80', 9.1558, 76.4950, 50.00, 2.0, True, True, 4.5),
        ('Alappuzha Lighthouse & Maritime Museum', 'Museum', 'Climbable striped lighthouse offering 360-degree views of the Arabian Sea and canals.', 'https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80', 9.4975, 76.3197, 40.00, 1.5, True, True, 4.4),
        ('Coir & Spice Heritage Village', 'Shopping', 'Demonstration of coconut fiber weaving, aromatic spices, and traditional Kerala handicrafts.', 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=800&q=80', 9.5340, 76.3280, 50.00, 2.0, True, True, 4.3),
        ('St. Mary\'s Forane Church (Champakulam)', 'Religious', 'Ancient Christian church established in 427 AD with carved altar and wooden statues.', 'https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=800&q=80', 9.4075, 76.4172, 0.00, 1.5, True, True, 4.6),
        ('Vembanad Lake Shikara Sunset Cruise', 'Relaxation', 'Small covered shikara boat gliding through narrow palm canals at golden hour.', 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?auto=format&fit=crop&w=800&q=80', 9.5850, 76.4100, 450.00, 2.0, True, True, 4.8),
    ]

    for name, cat, desc, img, lat, lng, fee, hours, indoor, rain, rating in kerala_attractions:
        TouristAttraction.objects.update_or_create(
            destination=dest_kerala,
            name=name,
            defaults={
                'category': cat,
                'description': desc,
                'image_url': img,
                'latitude': Decimal(str(lat)),
                'longitude': Decimal(str(lng)),
                'entry_fee': Decimal(str(fee)),
                'typical_time_spent_hours': Decimal(str(hours)),
                'is_indoor': indoor,
                'rain_friendly': rain,
                'rating': Decimal(str(rating))
            }
        )

    print("[Done] Successfully seeded over 36 distinct attractions across all destinations!")

if __name__ == '__main__':
    seed_rich_attractions()
