# engine.py
import time
from PySide6.QtCore import QThread, Signal
from models import Alert, AlertType, Location
from providers.usgs import USGSProvider
from providers.om import OMProvider
from services.ai_advisor import ThreatAdvisor


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
        """Initializes or restarts providers for current location."""
        self.providers = [
            USGSProvider(self.location),
            OMProvider(self.location)
        ]

    def update_location(self, new_location: Location):
        """Method for GUI to change the scan region."""
        self.location = new_location
        self.seen_alerts.clear()  # Optional: clear history on location change
        self._init_providers()

    def request_ai_advice(self, alert: Alert):
        """Method for GUI to trigger AI advice manually."""
        advice = self.advisor.generate_advice(
            threat_type=alert.raw_data,
            location=self.location.display_name,
            type=alert.type
        )
        self.ai_advice_signal.emit(advice)

    def run(self):
        """Main background loop."""
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

                            source = "Weather" if "[Weather" in text else "Earthquake"

                            # Create Alert object and send to GUI
                            alert_obj = Alert(
                                source=source,
                                message=text,
                                type=AlertType.DANGER if "WARNING" in text or "CRITICAL" in text else AlertType.SAFE,
                                raw_data=text
                            )
                            self.new_alert_signal.emit(alert_obj)
                except Exception as e:
                    self.new_alert_signal.emit(Alert(source="System", message="Provider error", type=AlertType.UNKNOWN, raw_data="Provider error"))
                    print(f"Provider error: {e}")

            time.sleep(10)  # 10s interval to save API limits

    def stop(self):
        self.is_running = False
        self.wait()
