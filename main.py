import time
import os
from dotenv import load_dotenv

from providers.base import Location
from utils import resolve_location

from providers.usgs import USGSProvider
from providers.om import OMProvider

from services.ai_advisor import ThreatAdvisor

load_dotenv()

LOCATION: Location = resolve_location("Osaka")
POLL_INTERVAL = 30

PROVIDERS = [
    USGSProvider(LOCATION),
    OMProvider(LOCATION)
]


def main():
    print(f"threat-ping started — {LOCATION.display_name}")

    advisor = ThreatAdvisor()
    seen_alerts = set()

    while True:
        for provider in PROVIDERS:
            alerts = provider.fetch()
            for alert_text in alerts:
                if alert_text not in seen_alerts:
                    print(alert_text)
                    seen_alerts.add(alert_text)

                    # addressing AI only if it's important WARNING/CRITICAL
                    is_threat = any(keyword in alert_text for keyword in ["Earthquake", "WARNING", "CRITICAL"])

                    if is_threat:
                        print("  [AI is analyzing the threat...]")
                        advice = advisor.generate_advice(
                            threat_type=alert_text,
                            location=LOCATION.display_name,
                            severity="High"
                        )
                        print(f"  {advice}\n")

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()