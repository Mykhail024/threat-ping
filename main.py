import time

from providers.base import Location
from utils import resolve_location
from providers.usgs import USGSProvider

LOCATION: Location = resolve_location("Ternopil")
POLL_INTERVAL = 5

PROVIDERS = [
    USGSProvider(LOCATION, radius_km=1500, min_magnitude=3.0) #radius is debatable and yet to be changed
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
