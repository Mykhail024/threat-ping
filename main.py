import time

from providers.base import Location
from utils import resolve_location

from providers.usgs import USGSProvider
from providers.weather import WeatherProvider

LOCATION: Location = resolve_location("Ternopil")
POLL_INTERVAL = 5

PROVIDERS = [
    USGSProvider(LOCATION),
    WeatherProvider(LOCATION)
]


def main():
    print(f"threat-ping started — {LOCATION.display_name}")

    while True:
        for provider in PROVIDERS:
            alerts = provider.fetch()
            for alert in alerts:
                print(alert)  # TODO: replace with real notification!!!
        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
