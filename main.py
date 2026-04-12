import time
import os
import sys
from dotenv import load_dotenv

from providers.base import Location
from utils import resolve_location

from providers.usgs import USGSProvider
from providers.om import OMProvider
from providers.noaa import SpaceWeatherProvider

from services.ai_advisor import ThreatAdvisor

from PyQt6.QtWidgets import QApplication
from engine import ThreatEngine
from services.location_service import LocationService


def main():
    app = QApplication(sys.argv)

    # Example logic: Get location by IP first
    loc_service = LocationService()
    current_location = loc_service.get_by_ip()

    # Initialize engine
    engine = ThreatEngine(current_location)

    # Connect signals 
    # window = MainWindow()
    # engine.new_alert_signal.connect(window.add_alert_to_list)
    # engine.ai_advice_signal.connect(window.show_ai_popup)

    engine.start()

    # sys.exit(app.exec()) # This starts the UI event loop
    print(f"Engine started for: {current_location.display_name}")
    print("Wait for GUI to be integrated...")


if __name__ == "__main__":
    main()