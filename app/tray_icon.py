from pathlib import Path
import sys
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu


BASE_DIR = Path(__file__).resolve().parent.parent
ICONS_DIR = BASE_DIR / "qml" / "assets" / "icons"

class TrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None):
        self.icons = {
            "normal": QIcon(str(ICONS_DIR / "lucide--map-pin-check.svg")),
            "danger": QIcon(str(ICONS_DIR / "lucide--map-pin-x.svg")),
            "loading": QIcon(str(ICONS_DIR / "lucide--map-pin.svg")),
        }

        super().__init__(self.icons["loading"], parent)

        self.menu = QMenu()

        self.settings_action = QAction("Settings", self.menu)
        self.quit_action = QAction("Quit", self.menu)

        self.menu.addAction(self.settings_action)
        self.menu.addAction(self.quit_action)

        self.quit_action.triggered.connect(self.on_quit_click)
        self.settings_action.triggered.connect(self.on_settings_click)

        self.setContextMenu(self.menu)

    def on_click(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            print("Left clicked!")

    def on_quit_click(self):
        app = QApplication.instance()
        if app is not None:
            app.quit()
            print("Exit...")

    def on_settings_click(self):
        print("Settings...")
            
    def set_state(self, state: str):
        icon = self.icons.get(state, self.icons["loading"])
        self.setIcon(icon)

        tooltips = {
            "normal": "ThreatPing: Safe",
            "danger": "ThreatPing: Critical threat",
            "loading": "ThreatPing: Updating...",
        }
        self.setToolTip(tooltips.get(state, "ThreatPing"))

