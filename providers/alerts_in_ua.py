import os
import requests
import traceback

from providers.base import BaseProvider, Location


class AlertsInUaProvider(BaseProvider):
    URL_ALERTS = "https://api.alerts.in.ua/v1/alerts/active.json"
    URL_GEO = "https://nominatim.openstreetmap.org/reverse"

    _geo_cache: dict = {}

    def __init__(self, location: Location):
        super().__init__(location)

        self.api_token = os.getenv("ALERTS_IN_UA_TOKEN")

        self.local_names = self._fetch_local_names()

    @staticmethod
    def _normalize(text: str) -> str:

        if not text:
            return ""

        text = text.lower().strip()

        replacements = [
            "область",
            "район",
            "місто",
            "м.",
            "громада",
            "територіальна",
        ]

        for item in replacements:
            text = text.replace(item, "")

        return " ".join(text.split()).strip()

    @staticmethod
    def _stem(text: str) -> str:


        text = AlertsInUaProvider._normalize(text)

        suffixes = [
            "ська",
            "ський",
            "ські",
            "ське",
            "ської",
            "ському",
            "ський",
            "ських",
        ]

        for suffix in suffixes:
            if text.endswith(suffix):
                text = text[:-len(suffix)]
                break

        if text.endswith("и"):
            text = text[:-1]

        return text.strip()

    def _fetch_local_names(self) -> set[str]:

        names = set()

        if self.location.lat == 0.0 and self.location.lon == 0.0:
            return names

        cache_key = (
            round(self.location.lat, 3),
            round(self.location.lon, 3)
        )

        cached = self._geo_cache.get(cache_key)

        if cached:
            return cached

        try:
            response = requests.get(
                self.URL_GEO,
                params={
                    "lat": self.location.lat,
                    "lon": self.location.lon,
                    "format": "json",
                    "zoom": 10,
                },
                headers={
                    "User-Agent": "threat-ping-app",
                    "Accept-Language": "uk",
                },
                timeout=(3, 10)
            )

            response.raise_for_status()

            data = response.json()
            address = data.get("address", {})

            keys_to_extract = [
                "state",
                "county",
                "city",
                "town",
                "municipality",
                "village",
            ]

            for key in keys_to_extract:
                value = address.get(key)

                if value:
                    names.add(value.lower())

            self._geo_cache[cache_key] = names

            print(f"[DEBUG] Geo names resolved: {names}")

        except requests.exceptions.RequestException as e:
            print(f"[System] Reverse geocoding failed: {e}")

        except Exception:
            traceback.print_exc()

        return names

    def _map_alert_type(self, alert_type: str) -> str:

        mapping = {
            "air_raid": "Air Raid Alert",
            "artillery_shelling": "Artillery Threat",
            "urban_fights": "Urban Combat Threat",
            "chemical": "Chemical Hazard",
            "nuclear": "Nuclear Threat",
        }

        return mapping.get(
            alert_type,
            f"Unknown Threat ({alert_type})"
        )

    def fetch(self) -> list[str]:

        if not self.api_token:
            return [
                "[System WARNING] ALERTS_IN_UA_TOKEN not found."
            ]

        if not self.local_names:
            print("[DEBUG] No local names resolved.")
            return []

        print(
            f"[DEBUG] Searching alerts for locations: "
            f"{self.local_names}"
        )

        try:
            response = requests.get(
                self.URL_ALERTS,
                headers={
                    "Authorization": f"Bearer {self.api_token}"
                },
                timeout=(3, 10)
            )

            response.raise_for_status()

            data = response.json()

            alerts = data.get("alerts")

            if not isinstance(alerts, list):
                return [
                    "[System] Invalid alerts format received."
                ]

            active_alerts = []

            for alert in alerts:
                location_title = alert.get(
                    "location_title",
                    ""
                )

                location_oblast = alert.get(
                    "location_oblast",
                    ""
                )

                alert_type = alert.get(
                    "alert_type",
                    "air_raid"
                )

                alert_stems = {
                    self._stem(location_title),
                    self._stem(location_oblast),
                }

                local_stems = {
                    self._stem(name)
                    for name in self.local_names
                }

                is_match = any(
                    stem in local_stems
                    for stem in alert_stems
                    if stem
                )

                if not is_match:
                    continue

                threat_name = self._map_alert_type(
                    alert_type
                )

                print(
                    f"[DEBUG] MATCH FOUND -> "
                    f"{location_title} ({alert_type})"
                )

                active_alerts.append(
                    f"[CRITICAL] "
                    f"{threat_name} — "
                    f"{location_title}"
                )

            if active_alerts:
                print(
                    f"[DEBUG] Returning alerts: "
                    f"{active_alerts}"
                )

            return active_alerts

        except requests.exceptions.Timeout:
            return [
                "[System] alerts.in.ua API timeout."
            ]

        except requests.exceptions.RequestException as e:
            return [
                f"[System] alerts.in.ua API request failed: {e}"
            ]

        except Exception:
            traceback.print_exc()

            return [
                "[System] Unexpected error occurred "
                "inside AlertsInUaProvider."
            ]