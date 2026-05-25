from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtQml import QQmlApplicationEngine, qmlRegisterType
from models import Alert
from services.location_model import LocationSearchModel
from services.location_service import LocationService
from engine import ThreatEngine
from app.tray_icon import TrayIcon

from qml import resources_rc

class ThreatPing:
    def __init__(self, app) -> None:
        self.app = app

        self.loc_service = LocationService()
        self.current_location = None

        self.threat_engine = None
        self.qml_engine = None
        self.tray = None

        self._is_shutting_down = False

        self.app.aboutToQuit.connect(self.shutdown)

    def start(self) -> int:
        self.current_location = self.loc_service.get_by_ip()

        self.threat_engine = ThreatEngine(self.current_location)
        self.threat_engine.start()
        print(f"Engine started for: {self.current_location.display_name}")

        self.qml_engine = QQmlApplicationEngine()
        self.qml_engine.addImportPath(":/")
        self._register_qml_types()
        self.qml_engine.load("qrc:/main.qml")

        if not self.qml_engine.rootObjects():
            self.stop()
            return 1

        self.tray = TrayIcon(on_quit=self.quit, parent= None)
        self.tray.show()

        self.threat_engine.new_alert_signal.connect(self.on_alert)

        try:
            return self.app.exec()
        finally:
            self.stop()

    def on_alert(self, alert : Alert):
        if self.tray is not None:
            self.tray.set_state(alert.type)

            print("Alert: ", alert.type.name)

    def stop(self):
        if self.threat_engine is not None:
            self.threat_engine.stop()

    def shutdown(self):
        if self._is_shutting_down:
            return
        self._is_shutting_down = True

        if self.tray is not None:
            self.tray.hide()

        if self.threat_engine is not None:
            self.threat_engine.stop()

    def quit(self):
        self.shutdown()
        self.app.quit()

    def _register_qml_types(self):
        qmlRegisterType(LocationSearchModel, "ThreatPing", 1, 0, "LocationSearchModel")
