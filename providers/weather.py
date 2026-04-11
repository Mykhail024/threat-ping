import requests
from providers.base import BaseProvider, Location


class WeatherProvider(BaseProvider):
    URL = "https://api.open-meteo.com/v1/forecast"

    def __init__(self, location: Location):
        super().__init__(location)

    def fetch(self) -> list[str]:
        try:
            response = requests.get(self.URL, params={
                "latitude": self.location.lat,
                "longitude": self.location.lon,
                "current_weather": "true"
            })
            response.raise_for_status()

            data = response.json()
            current = data.get("current_weather", {})
            weather_code = current.get("weathercode")

            # WMO extreme codes
            # full list (maybe in the future): https://open-meteo.com/en/docs
            severe_weather_codes = {
                71: "Heavy snowfall",
                73: "Snowstorm",
                75: "Extreme snowfall",
                95: "Severe thunderstorm",
                96: "Thunderstorm with hail",
                99: "Thunderstorm with large hail (Storm warning)"
            }

            alerts = []
            # checking in the list
            if weather_code in severe_weather_codes:
                threat_name = severe_weather_codes[weather_code]
                alerts.append(f"[Weather Warning] {threat_name} - {self.location.display_name}")

            return alerts

        except Exception as e:
            print(f"Connection error Weather: {e}")
            return []