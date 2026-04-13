import sys
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine, qmlRegisterSingletonType
from PyQt6.QtCore import QUrl
from pathlib import Path

qml_dir = Path(__file__).parent / "qml"

def main():
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    qmlRegisterSingletonType(QUrl.fromLocalFile(str(qml_dir / "theme/Colors.qml")), "Theme", 1, 0, "Colors")
    qmlRegisterSingletonType(QUrl.fromLocalFile(str(qml_dir / "theme/Typography.qml")), "Theme", 1, 0, "Typography")
    qmlRegisterSingletonType(QUrl.fromLocalFile(str(qml_dir / "theme/Sizes.qml")), "Theme", 1, 0, "Sizes")

    engine.load(QUrl("qml/main.qml"))

    if not engine.rootObjects():
        sys.exit(1)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
