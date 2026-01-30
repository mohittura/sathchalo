"""
Trip Info Tool
Provides destination information and travel tips.
"""


# Destination database
DESTINATIONS = {
    "paris": {
        "name": "Paris, France",
        "best_time": "April to June, September to November",
        "language": "French",
        "currency": "Euro (€)",
        "attractions": ["Eiffel Tower", "Louvre Museum", "Notre-Dame", "Champs-Élysées", "Montmartre"],
        "tips": "Learn basic French phrases. Metro is the best way to get around."
    },
    "tokyo": {
        "name": "Tokyo, Japan",
        "best_time": "March to May (cherry blossoms), September to November",
        "language": "Japanese",
        "currency": "Japanese Yen (¥)",
        "attractions": ["Shibuya Crossing", "Senso-ji Temple", "Tokyo Tower", "Akihabara", "Meiji Shrine"],
        "tips": "Get a Suica card for transport. Many places are cash-only."
    },
    "bali": {
        "name": "Bali, Indonesia",
        "best_time": "April to October (dry season)",
        "language": "Indonesian, Balinese",
        "currency": "Indonesian Rupiah (IDR)",
        "attractions": ["Ubud Rice Terraces", "Uluwatu Temple", "Seminyak Beach", "Tanah Lot", "Mount Batur"],
        "tips": "Rent a scooter for flexibility. Respect temple dress codes."
    },
    "dubai": {
        "name": "Dubai, UAE",
        "best_time": "November to March (cooler months)",
        "language": "Arabic, English widely spoken",
        "currency": "UAE Dirham (AED)",
        "attractions": ["Burj Khalifa", "Dubai Mall", "Palm Jumeirah", "Desert Safari", "Dubai Marina"],
        "tips": "Dress modestly in public. Friday is the weekend."
    },
    "goa": {
        "name": "Goa, India",
        "best_time": "November to February",
        "language": "Konkani, English, Hindi",
        "currency": "Indian Rupee (₹)",
        "attractions": ["Baga Beach", "Basilica of Bom Jesus", "Dudhsagar Falls", "Fort Aguada", "Anjuna Flea Market"],
        "tips": "Rent a two-wheeler. North Goa is lively, South Goa is serene."
    }
}


def get_trip_info(destination: str) -> str:
    """
    Get information about a travel destination.
    
    Args:
        destination: City or destination name
    
    Returns:
        Destination information as formatted string
    """
    destination_lower = destination.lower().strip()
    
    # Find matching destination
    info = None
    for key, value in DESTINATIONS.items():
        if key in destination_lower or destination_lower in key:
            info = value
            break
    
    if not info:
        return (
            f"📍 {destination.title()}\n\n"
            f"I don't have detailed information about this destination yet.\n"
            f"But I can still help you with weather, flights, and budget estimates!\n\n"
            f"Try asking about popular destinations like Paris, Tokyo, Bali, Dubai, or Goa."
        )
    
    attractions_list = ", ".join(info["attractions"])
    
    return (
        f"📍 {info['name']}\n\n"
        f"🗓️ Best Time to Visit: {info['best_time']}\n"
        f"🗣️ Language: {info['language']}\n"
        f"💵 Currency: {info['currency']}\n\n"
        f"🏛️ Top Attractions:\n{attractions_list}\n\n"
        f"💡 Travel Tip: {info['tips']}"
    )
