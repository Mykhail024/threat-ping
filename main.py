import os
import sys
from pathlib import Path

from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine, qmlRegisterSingletonType, qmlRegisterType
from PyQt6.QtCore import QUrl

from services.location_model import LocationSearchModel
from services.location_service import LocationService
from engine import ThreatEngine

qml_dir = Path(__file__).parent / "qml"

def main():
    os.environ["QT_QUICK_CONTROLS_STYLE"] = "Fusion"

    app = QGuiApplication(sys.argv)

    loc_service = LocationService()
    current_location = loc_service.get_by_ip()
    
    threat_engine = ThreatEngine(current_location)
    threat_engine.start()
    print(f"Engine started for: {current_location.display_name}")

    engine = QQmlApplicationEngine()

    qmlRegisterSingletonType(QUrl.fromLocalFile(str(qml_dir / "theme/Colors.qml")), "Theme", 1, 0, "Colors")
    qmlRegisterSingletonType(QUrl.fromLocalFile(str(qml_dir / "theme/Typography.qml")), "Theme", 1, 0, "Typography")
    qmlRegisterSingletonType(QUrl.fromLocalFile(str(qml_dir / "theme/Sizes.qml")), "Theme", 1, 0, "Sizes")

    qmlRegisterType(LocationSearchModel, "ThreatPing", 1, 0, "LocationSearchModel")

    engine.load(QUrl("qml/main.qml"))

    if not engine.rootObjects():
        threat_engine.stop()
        sys.exit(1
    exit_code = app.exec()
    
    threat_engine.stop() 
    sys.exit(exit_code)

if __name__ == "__main__":
    main()