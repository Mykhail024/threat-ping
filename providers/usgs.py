import requests
from providers.base import BaseProvider, Location


class USGSProvider(BaseProvider):
    URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

    def __init__(self, location: Location, radius_km: int = 500, min_magnitude: float = 4.0):
        super().__init__(location)
        self.radius_km = radius_km
        self.min_magnitude = min_magnitude

    def fetch(self) -> list[str]:
        try:
            response = requests.get(self.URL, params={
                "format": "geojson",
                "latitude": self.location.lat,
                "longitude": self.location.lon,
                "maxradiuskm": self.radius_km,
                "minmagnitude": self.min_magnitude,
                "orderby": "time",
                "limit": 5,
            })
            response.raise_for_status()

            features = response.json().get("features", [])
            alerts = []
            for event in features:
                props = event["properties"]
                alerts.append(f"[Earthquake] M{props['mag']} - {props['place']}")
            return alerts

        except Exception as e:
            print(f"Помилка з'єднання з USGS: {e}")
            return []