# services/location_service.py
import requests
from utils import resolve_location
from models import Location

class LocationService:
    @staticmethod
    def get_by_query(query: str) -> Location:
        """Uses Nominatim from utils.py to find location by string."""
        return resolve_location(query)

    @staticmethod
    def get_by_ip() -> Location:
        """Detects location using IP-API (free service)."""
        try:
            response = requests.get("http://ip-api.com/json/", timeout=5)
            data = response.json()
            #map IP-API fields to our Location model
            return Location(
                region=data.get("city", "Unknown"),
                country=data.get("countryCode", "UA"),
                lat=data.get("lat", 0.0),
                lon=data.get("lon", 0.0),
                display_name=f"{data.get('city')}, {data.get('country')}"
            )
        except Exception:
            # Fallback to default location if IP detection fails
            return Location("Kyiv", "UA", 50.45, 30.52, "Kyiv, Ukraine (Fallback)")