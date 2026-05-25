# engine.py
import time
from PySide6.QtCore import QThread, Signal, Slot
from models import Alert, AlertType, Location
from providers.usgs import USGSProvider
from providers.om import OMProvider
from services.ai_advisor import ThreatAdvisor
from providers.alerts_in_ua import AlertsInUaProvider


class ThreatEngine(QThread):
    # This signal sends new alerts to the GUI
    new_alert_signal = Signal(Alert)
    # This signal sends AI advice back to the GUI
    ai_advice_signal = Signal(str)

    def __init__(self, location: Location):
        super().__init__()
        self.location = location
        self.advisor = ThreatAdvisor()
        self.seen_alerts = set()
        self.is_running = True
        self._init_providers()

    def _init_providers(self):
        self.providers = [
            USGSProvider(self.location),
            OMProvider(self.location),
            AlertsInUaProvider(self.location)
        ]

    def update_location(self, new_location: Location):
        self.location = new_location
        self.seen_alerts.clear()
        self._init_providers()
        print("Location changed to: ", self.location.country)

    @Slot(str, str, float, float, str)
    def update_location_from_qml(self, region : str, display_name: str, lat: float, lon: float, country: str):
        new_location = Location(
                region=region,
                display_name=display_name,
                lat=lat,
                lon=lon,
                country=country
                )
        self.update_location(new_location)

    def request_ai_advice(self, alert: Alert):
        advice = self.advisor.generate_advice(
            threat_type=alert.raw_data,
            location=self.location.display_name,
            type=alert.type
        )
        self.ai_advice_signal.emit(advice)

    def run(self):
        while self.is_running:
            if self.isInterruptionRequested():
                self.is_running = False
                return

            for provider in self.providers:
                try:
                    raw_alerts = provider.fetch()
                    for text in raw_alerts:
                        if text not in self.seen_alerts:
                            self.seen_alerts.add(text)
                            if "[Weather" in text:
                                source = "Weather"
                            elif "[Earthquake" in text:
                                source = "Earthquake"
                            elif "[Air Raid" in text:
                                source = "Air Raid"
                            else:
                                source = "System"

                            alert_type = AlertType.DANGER if "WARNING" in text or "CRITICAL" in text else AlertType.SAFE
                            alert_obj = Alert(
                                source=source,
                                message=text,
                                type=alert_type,
                                raw_data=text
                            )
                            self.new_alert_signal.emit(alert_obj)
                except Exception as e:
                    self.new_alert_signal.emit(Alert(source="System", message="Provider error", type=AlertType.UNKNOWN, raw_data="Provider error"))
                    print(f"Provider error: {e}")

            time.sleep(10)

    def stop(self):
        self.is_running = False
        self.wait()
