from app.services.travel_service import TravelService

class Planner:
    def __init__(self):
        self.travel_service = TravelService()

    def plan_trip(self, city: str) -> str:
        summary = self.travel_service.get_trip_summary(city)
        return f"Planner created: {summary}"
