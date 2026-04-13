# engine.py
import time
import dataclasses
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot
from models import Alert, Location
from providers.usgs import USGSProvider
from providers.om import OMProvider
from services.ai_advisor import ThreatAdvisor


class ThreatEngine(QThread):
    new_alert_signal = pyqtSignal(dict)
    ai_advice_signal = pyqtSignal(str)

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
            OMProvider(self.location)
        ]

    def update_location(self, new_location: Location):
        """Method for GUI to change the scan region."""
        self.location = new_location
        self.seen_alerts.clear()
        self._init_providers()

    @pyqtSlot(dict)
    def request_ai_advice(self, alert_dict: dict):
        advice = self.advisor.generate_advice(
            threat_type=alert_dict["raw_data"],
            location=self.location.display_name,
            severity=alert_dict["severity"]
        )
        self.ai_advice_signal.emit(advice)

    def run(self):
        while self.is_running:
            for provider in self.providers:
                try:
                    raw_alerts = provider.fetch()
                    for text in raw_alerts:
                        if text not in self.seen_alerts:
                            self.seen_alerts.add(text)

                            severity = "INFO"
                            if "CRITICAL" in text:
                                severity = "CRITICAL"
                            elif "WARNING" in text:
                                severity = "WARNING"
                            source = "Weather" if "[Weather" in text else "Earthquake"

                            alert_obj = Alert(
                                source=source,
                                message=text,
                                severity=severity,
                                raw_data=text
                            )

                            self.new_alert_signal.emit(dataclasses.asdict(alert_obj))
                except Exception as e:
                    print(f"Provider error: {e}")

            time.sleep(10)

    def stop(self):
        self.is_running = False
        self.wait()