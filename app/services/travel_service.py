"""
Travel Service Module
Orchestrates travel tools for comprehensive trip information.
"""
from app.tools.weather import get_weather
from app.tools.trip_info import get_trip_info
from app.tools.budget import calculate_budget


class TravelService:
    """
    Service to combine multiple travel tools for a complete trip summary.
    """
    
    def get_trip_summary(self, city: str, days: int = 3) -> str:
        """
        Get a comprehensive trip summary for a destination.
        
        Args:
            city: Destination city name
            days: Number of days for the trip
            
        Returns:
            Combined summary with weather, destination info, and budget
        """
        weather = get_weather(city)
        destination_info = get_trip_info(city)
        budget = calculate_budget(f"{city} {days} days")
        
        return (
            f"🌍 Trip Summary for {city.title()}\n\n"
            f"{'='*40}\n\n"
            f"{weather}\n\n"
            f"{'='*40}\n\n"
            f"{destination_info}\n\n"
            f"{'='*40}\n\n"
            f"{budget}"
        )
