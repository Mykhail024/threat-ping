import os
import requests
from providers.base import BaseProvider, Location


class AlertsInUaProvider(BaseProvider):
    URL = "https://api.alerts.in.ua/v1/alerts/active.json"

    def __init__(self, location: Location):
        super().__init__(location)
        # TOKEEEEEEEEEEEEEEEEEEEEEEN
        self.api_token = os.getenv("ALERTS_IN_UA_TOKEN")

    def fetch(self) -> list[str]:
        if not self.api_token:
            return ["[System] ALERTS_IN_UA_TOKEN не знайдено у файлі .env"]

        try:
            response = requests.get(
                self.URL,
                headers={"Authorization": f"Bearer {self.api_token}"},
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            alerts = data.get("alerts", [])
            active_alerts = []

            for alert in alerts:
                loc_title = alert.get("location_title", "")
                if self.location.region.lower() in loc_title.lower() or loc_title.lower() in self.location.region.lower():
                    alert_type = alert.get("alert_type", "air_raid")
                    threat_name = "Air raid alert"
                    if alert_type == "artillery_shelling":
                        threat_name = "Artillery shells"
                    elif alert_type == "chemical":
                        threat_name = "Chemical threat"
                    elif alert_type == "nuclear":
                        threat_name = "Radiation alert"

                    active_alerts.append(f"[Air Raid CRITICAL] {threat_name} — {loc_title}")

            return active_alerts

        except requests.exceptions.RequestException as e:
            return [f"[System] alerts.in.ua API timeout/error: {e}"]
        except Exception as e:
            return [f"[System] Unexpected error occurred in alerts.in.ua: {e}"]
