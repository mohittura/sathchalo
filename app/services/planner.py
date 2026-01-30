"""
Trip Planner Service
Creates complete trip plans with itineraries and recommendations.
"""
from app.tools.itenary import create_itinerary
from app.tools.trip_info import get_trip_info
from app.tools.budget import calculate_budget


class Planner:
    """
    Service to create comprehensive trip plans.
    """
    
    def plan_trip(self, destination: str, days: int = 3) -> str:
        """
        Create a complete trip plan.
        
        Args:
            destination: Where to travel
            days: Number of days
            
        Returns:
            Complete trip plan with itinerary, info, and budget
        """
        destination_info = get_trip_info(destination)
        itinerary = create_itinerary(f"{days} days {destination}")
        budget = calculate_budget(f"{destination} {days} days")
        
        return (
            f"✈️ Your {days}-Day Trip to {destination.title()}\n\n"
            f"{destination_info}\n\n"
            f"{'━'*40}\n\n"
            f"{itinerary}\n\n"
            f"{'━'*40}\n\n"
            f"{budget}"
        )
