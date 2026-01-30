from app.tools.weather import get_weather

class TravelService:
    def get_trip_summary(self, city: str) -> str:
        weather = get_weather(city)
        return f"Trip summary for {city}: {weather}"
