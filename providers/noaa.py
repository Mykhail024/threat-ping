import requests
from providers.base import BaseProvider, Location


class SpaceWeatherProvider(BaseProvider):
    """
    Fetches real-time Planetary K-index from NOAA Space Weather Prediction Center.
    """
    URL = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"

    def fetch(self) -> list[str]:
        try:
            response = requests.get(self.URL, headers={"User-Agent": "threat-ping/1.0"}, timeout=10)
            response.raise_for_status()

            data = response.json()
            kp_value = 0.0
            found = False

            for entry in reversed(data):
                try:
                    val = None
                    if isinstance(entry, dict):
                        val = entry.get("Kp") or entry.get("kp")
                    elif isinstance(entry, list):
                        if entry[0] == "time_tag":
                            continue
                        val = entry[1] if len(entry) > 1 else None

                    if val is not None and str(val).strip() != "":
                        kp_value = float(val)
                        found = True
                        break
                except (IndexError, ValueError, KeyError):
                    continue

            if found:
                if kp_value >= 5.0:
                    g_scale = int(kp_value - 4)
                    return [
                        f"[Space Weather CRITICAL] Geomagnetic Storm G{g_scale} detected (Kp={kp_value}). Risk of GPS/Radio disruptions!"]
                else:
                    return [f"[Space Weather] Normal condition (Kp={kp_value}). No solar threats."]
            else:
                return ["[System] Could not parse Kp index from Space Weather data."]

        except requests.exceptions.Timeout:
            return ["[System] NOAA Space Weather API timeout."]
        except Exception as e:
            return [f"[System] Space Weather error: {repr(e)}"]