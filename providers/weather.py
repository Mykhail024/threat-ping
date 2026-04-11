import requests
from providers.base import BaseProvider, Location

class WeatherProvider(BaseProvider):
    """
    Fetches current weather data from Open-Meteo API.
    Uses full WMO code mapping and severity classification.
    """
    URL = "https://api.open-meteo.com/v1/forecast"

    # Complete WMO Weather interpretation codes (WW)
    # https://open-meteo.com/en/docs
    WEATHER_CODES = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Light freezing drizzle",
        57: "Dense freezing drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Light freezing rain",
        67: "Heavy freezing rain",
        71: "Slight snow fall",
        73: "Moderate snow fall",
        75: "Heavy snow fall",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm (slight or moderate)",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail",
    }

    # Severity thresholds based on code ranges
    SEVERITY_CRITICAL = {95, 96, 99}          # Thunderstorms with/without hail
    SEVERITY_WARNING = {56, 57, 66, 67, 71, 73, 75, 77, 82, 85, 86}  # Freezing rain, heavy snow, violent showers

    def _get_condition(self, code: int) -> str:
        """Return human-readable condition for a given weather code."""
        return self.WEATHER_CODES.get(code, f"Unknown (code {code})")

    def _get_severity(self, code: int) -> str:
        """Return severity level: INFO, WARNING, or CRITICAL."""
        if code in self.SEVERITY_CRITICAL:
            return "CRITICAL"
        if code in self.SEVERITY_WARNING:
            return "WARNING"
        return "INFO"

    def fetch(self) -> list[str]:
        """
        Fetch current weather for the stored location.
        Returns a list with one string containing weather info and alerts.
        """
        try:
            response = requests.get(
                self.URL,
                params={
                    "latitude": self.location.lat,
                    "longitude": self.location.lon,
                    "current_weather": "true",
                    # Additional fields can be added here (e.g., "hourly": ""),
                    # but current_weather already gives temperature, wind, weathercode.
                },
                headers={"User-Agent": "threat-ping/1.0"},
                timeout=5
            )
            response.raise_for_status()

            data = response.json()
            current = data.get("current_weather", {})

            if not current:
                return ["[Weather] No current weather data available"]

            code = current.get("weathercode", 0)
            temp = current.get("temperature")
            wind_speed = current.get("windspeed")
            wind_dir = current.get("winddirection")

            condition = self._get_condition(code)
            severity = self._get_severity(code)

            # Build base weather string
            weather_str = (f"{condition}, {temp:.1f}°C" if temp is not None else f"{condition}, temperature N/A")
            if wind_speed is not None:
                weather_str += f", wind {wind_speed:.1f} km/h"
                if wind_dir is not None:
                    weather_str += f" (from {wind_dir:.0f}°)"

            # Add severity prefix
            if severity == "CRITICAL":
                prefix = "[Weather CRITICAL]"
            elif severity == "WARNING":
                prefix = "[Weather WARNING]"
            else:
                prefix = "[Weather]"

            return [f"{prefix} {weather_str} - {self.location.display_name}"]

        except requests.exceptions.Timeout:
            return ["[System] Weather API timeout. The service may be slow. Consider increasing timeout or retrying later."]
        except requests.exceptions.RequestException as e:
            return [f"[System] Weather API request failed: {e}"]
        except Exception as e:
            return [f"[System] Unexpected weather error: {e}"]