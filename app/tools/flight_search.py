"""
Flight Search Tool
Mock flight search for demo purposes.
"""


def search_flights(query: str) -> str:
    """
    Search for flights between cities.
    
    Args:
        query: Search query like "Delhi to Paris" or "flights from Mumbai to London"
    
    Returns:
        Flight options as a formatted string
    """
    # Parse origin and destination from query
    query_lower = query.lower()
    
    # Try to extract cities
    origin = "Your City"
    destination = "Destination"
    
    if " to " in query_lower:
        parts = query_lower.split(" to ")
        origin = parts[0].replace("flights from", "").replace("flight from", "").strip().title()
        destination = parts[1].strip().title()
    elif " from " in query_lower and " " in query_lower:
        # Handle "flights from X"
        parts = query_lower.split(" from ")
        if len(parts) > 1:
            origin = parts[1].split()[0].title()
    
    # Mock flight data
    flights = [
        {
            "airline": "Air India",
            "departure": "06:00",
            "arrival": "12:30",
            "price": "₹15,500",
            "stops": "Non-stop"
        },
        {
            "airline": "IndiGo",
            "departure": "09:45",
            "arrival": "16:15",
            "price": "₹12,800",
            "stops": "1 stop"
        },
        {
            "airline": "Emirates",
            "departure": "14:30",
            "arrival": "22:00",
            "price": "₹28,000",
            "stops": "Non-stop"
        }
    ]
    
    result = f"✈️ Flights from {origin} to {destination}:\n\n"
    
    for i, flight in enumerate(flights, 1):
        result += (
            f"{i}. {flight['airline']}\n"
            f"   Departure: {flight['departure']} → Arrival: {flight['arrival']}\n"
            f"   Price: {flight['price']} | {flight['stops']}\n\n"
        )
    
    result += "💡 Tip: Book early for better prices!"
    
    return result
