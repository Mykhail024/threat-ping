import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtQml import QQmlApplicationEngine, qmlRegisterSingletonType
from PyQt6.QtCore import QUrl
from pathlib import Path
from engine import ThreatEngine
from services.location_service import LocationService
from services.location_model import LocationSearchModel


qml_dir = Path(__file__).parent / "qml"


def main():
    os.environ["QT_QUICK_CONTROLS_STYLE"] = "Fusion"

    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()

    engine.warnings.connect(lambda warnings: [print(f" QML ERROR: {w.toString()}") for w in warnings])


    loc_service = LocationService()
    current_loc = loc_service.get_by_ip()
    threat_engine = ThreatEngine(current_loc)

    search_model = LocationSearchModel()

    context = engine.rootContext()
    context.setContextProperty("threatEngine", threat_engine)
    context.setContextProperty("searchModel", search_model)

    qmlRegisterSingletonType(QUrl.fromLocalFile(str(qml_dir / "theme/Colors.qml")), "Theme", 1, 0, "Colors")
    qmlRegisterSingletonType(QUrl.fromLocalFile(str(qml_dir / "theme/Typography.qml")), "Theme", 1, 0, "Typography")
    qmlRegisterSingletonType(QUrl.fromLocalFile(str(qml_dir / "theme/Sizes.qml")), "Theme", 1, 0, "Sizes")

    qml_path = str(qml_dir / "main.qml")
    engine.load(QUrl.fromLocalFile(qml_path))

    if not engine.rootObjects():
        print(f"crit error: {qml_path}")
        sys.exit(1)

    threat_engine.start()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()