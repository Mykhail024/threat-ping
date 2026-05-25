import os
import requests
import traceback
from providers.base import BaseProvider, Location


class AlertsInUaProvider(BaseProvider):
    URL_ALERTS = "https://api.alerts.in.ua/v1/alerts/active.json"
    URL_GEO = "https://nominatim.openstreetmap.org/reverse"

    def __init__(self, location: Location):
        super().__init__(location)
        self.api_token = os.getenv("ALERTS_IN_UA_TOKEN")

        # Dynamically fetch local administrative names (in Ukrainian)
        # to match against the API without hardcoding Cyrillic.
        self.local_names = self._fetch_local_names()

    def _fetch_local_names(self) -> set:
        names = set()
        if self.location.lat == 0.0 and self.location.lon == 0.0:
            return names

        try:
            response = requests.get(
                self.URL_GEO,
                params={
                    "lat": self.location.lat,
                    "lon": self.location.lon,
                    "format": "json",
                    "zoom": 10  # Zoom level 10 covers city and county boundaries
                },
                headers={
                    "User-Agent": "threat-ping-app",
                    "Accept-Language": "uk"  # Force API to return Ukrainian localized names
                },
                timeout=5
            )

            if response.status_code == 200:
                address = response.json().get("address", {})

                # Extract all levels of administration (Region, District, City, etc.)
                keys_to_extract = ["state", "county", "city", "town", "municipality", "village"]
                for key in keys_to_extract:
                    val = address.get(key)
                    if val:
                        names.add(val.lower())

        except Exception as e:
            print(f"[System] Reverse geocoding failed: {e}")

        return names

    def fetch(self) -> list[str]:
        if not self.api_token:
            return ["[System WARNING] ALERTS_IN_UA_TOKEN not found in environment variables."]

        if not self.local_names:
            return []

        # [DEBUG] Shows what names the provider is looking for
        print(f"[DEBUG] AlertsInUaProvider active. Searching for matches in: {self.local_names}")

        try:
            response = requests.get(
                self.URL_ALERTS,
                headers={"Authorization": f"Bearer {self.api_token}"},
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            alerts = data.get("alerts", [])
            active_alerts = []

            for alert in alerts:
                loc_title = alert.get("location_title", "").lower()
                alert_type = alert.get("alert_type", "air_raid")

                is_match = any(
                    local_name in loc_title or loc_title in local_name
                    for local_name in self.local_names
                )

                if is_match:
                    # [DEBUG] Shows exactly which alert triggered the match
                    print(f"[DEBUG] MATCH FOUND! Location: '{loc_title}', Type: '{alert_type}'")

                    threat_name = "Air Raid Alert"
                    if alert_type == "artillery_shelling":
                        threat_name = "Artillery Threat"
                    elif alert_type == "chemical":
                        threat_name = "Chemical Hazard"
                    elif alert_type == "nuclear":
                        threat_name = "Nuclear Threat"

                    active_alerts.append(f"[CRITICAL] {threat_name} - {alert.get('location_title')}")

            # [DEBUG] Shows the final list of active alerts being returned to the engine
            if active_alerts:
                print(f"[DEBUG] Returning alerts to engine: {active_alerts}")

            return active_alerts

        except requests.exceptions.RequestException as e:
            return [f"[System] alerts.in.ua API request failed: {e}"]
        except Exception as e:
            import traceback
            traceback.print_exc()
            return [f"[System] Unexpected error occurred: {e}"]