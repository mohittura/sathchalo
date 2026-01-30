"""
Itinerary Tool
Generates day-by-day travel itineraries.
"""


def create_itinerary(query: str) -> str:
    """
    Create a travel itinerary for a destination.
    
    Args:
        query: Query like "3 day itinerary for Paris" or "Tokyo 5 days"
    
    Returns:
        Day-by-day itinerary as formatted string
    """
    query_lower = query.lower()
    
    # Extract number of days
    days = 3  # default
    for word in query_lower.split():
        if word.isdigit():
            days = int(word)
            break
    
    # Cap at reasonable limit
    days = min(days, 7)
    
    # Determine destination
    destination = "your destination"
    common_destinations = ["paris", "tokyo", "bali", "dubai", "goa", "london", "singapore", "bangkok"]
    
    for dest in common_destinations:
        if dest in query_lower:
            destination = dest.title()
            break
    
    # Generate itinerary based on destination
    itineraries = {
        "Paris": [
            "🗼 Eiffel Tower & Trocadéro Gardens\n   - Morning: Climb the tower for city views\n   - Lunch: Café near Champ de Mars",
            "🎨 Louvre Museum & Tuileries\n   - Spend 4-5 hours exploring art\n   - Evening: Seine River walk",
            "⛪ Notre-Dame & Latin Quarter\n   - Morning: Cathedral visit\n   - Afternoon: Explore Saint-Germain-des-Prés",
            "🏰 Versailles Day Trip\n   - Full day at the palace and gardens\n   - Evening: Return for Montmartre sunset",
            "🛍️ Champs-Élysées & Arc de Triomphe\n   - Shopping and sightseeing\n   - Evening: Moulin Rouge area",
            "🍷 Montmartre & Sacré-Cœur\n   - Artist square, panoramic views\n   - Lunch: French bistro experience",
            "🌸 Hidden Paris\n   - Le Marais district, vintage shops\n   - Farewell dinner cruise on Seine"
        ],
        "Tokyo": [
            "🏮 Senso-ji Temple & Asakusa\n   - Morning: Temple visit, Nakamise shopping\n   - Afternoon: Tokyo Skytree",
            "🚶 Shibuya & Harajuku\n   - Famous crossing, Takeshita Street\n   - Evening: Shibuya nightlife",
            "🎌 Meiji Shrine & Shinjuku\n   - Morning: Peaceful shrine walk\n   - Night: Golden Gai tiny bars",
            "🗼 Tokyo Tower & Roppongi\n   - City views, art museums\n   - Evening: Upscale dining",
            "🎮 Akihabara & Ueno\n   - Anime/tech paradise, Ueno Park\n   - Evening: Ramen hunting",
            "🌊 Day Trip to Kamakura\n   - Giant Buddha, temples\n   - Beach time if weather permits",
            "🍣 Tsukiji & Ginza\n   - Fresh sushi breakfast\n   - Luxury shopping, tea ceremony"
        ]
    }
    
    # Get or create generic itinerary
    activities = itineraries.get(destination, None)
    
    if not activities:
        activities = [
            "🌅 Arrival & Orientation\n   - Check in, explore neighborhood\n   - Local dinner to sample cuisine",
            "🏛️ Major Attractions\n   - Visit top landmarks\n   - Cultural experiences",
            "🚶 Local Exploration\n   - Walking tour of historic areas\n   - Shopping at local markets",
            "🌿 Nature & Relaxation\n   - Parks, gardens, or beach\n   - Spa or wellness activity",
            "🎭 Cultural Immersion\n   - Museums, shows, or workshops\n   - Traditional dining experience",
            "🛍️ Shopping & Souvenirs\n   - Local crafts and gifts\n   - Farewell dinner",
            "✈️ Departure Day\n   - Last-minute sightseeing\n   - Airport transfer"
        ]
    
    # Build itinerary
    result = f"📅 {days}-Day Itinerary for {destination}\n\n"
    
    for i in range(days):
        result += f"━━━ Day {i + 1} ━━━\n"
        result += activities[i % len(activities)] + "\n\n"
    
    result += "💡 Tip: Be flexible and leave room for spontaneous discoveries!"
    
    return result
