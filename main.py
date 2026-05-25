import os
import sys
from dotenv import load_dotenv
load_dotenv()

from PySide6.QtWidgets import QApplication

from app.app import ThreatPing

def main():
    os.environ["QT_QUICK_CONTROLS_STYLE"] = "Fusion"

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    threat_ping = ThreatPing(app)

    exit_code = threat_ping.start()

    sys.exit(exit_code)

if __name__ == "__main__":
    main()
