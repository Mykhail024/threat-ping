from pathlib import Path
import sys
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu

from models import AlertType


BASE_DIR = Path(__file__).resolve().parent.parent
ICONS_DIR = BASE_DIR / "qml" / "assets" / "icons"

class TrayIcon(QSystemTrayIcon):
    def __init__(self, on_quit, parent=None):
        self.on_quit = on_quit
        self.icons = {
            AlertType.SAFE: QIcon(str(ICONS_DIR / "lucide--map-pin-check.svg")),
            AlertType.DANGER: QIcon(str(ICONS_DIR / "lucide--map-pin-x.svg")),
            AlertType.UNKNOWN: QIcon(str(ICONS_DIR / "lucide--map-pin.svg")),
        }

        super().__init__(self.icons[AlertType.UNKNOWN], parent)

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
        print("Quit...")
        self.hide()
        self.on_quit()

    def on_settings_click(self):
        print("Settings...")
            
    def set_state(self, state: AlertType):
        icon = self.icons.get(state, self.icons[AlertType.UNKNOWN])
        self.setIcon(icon)

        tooltips = {
            AlertType.SAFE: "ThreatPing: Safe",
            AlertType.DANGER: "ThreatPing: Critical threat",
            AlertType.UNKNOWN: "ThreatPing: Updating...",
        }
        self.setToolTip(tooltips.get(state, "ThreatPing"))

