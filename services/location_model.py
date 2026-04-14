import requests
import dataclasses

from PyQt6.QtCore import QAbstractListModel, QByteArray, QModelIndex, QVariant, Qt, pyqtSlot, QThread, pyqtSignal

from providers.base import Location


class SearchWorker(QThread):
    results_ready = pyqtSignal(int, list)
    error_occurred = pyqtSignal(int, str)

    def __init__(self, query_id, query):
        super().__init__()
        self.query_id = query_id
        self.query = query

    def run(self):
        try:
            response = requests.get(
                "https://nominatim.openstreetmap.org/search",
                params={"q": self.query, "format": "json", "limit": 5, "addressdetails": 1},
                headers={"User-Agent": "threat-ping-app-v1"},
                timeout=5
            )
            if self.isInterruptionRequested():
                return
            data = response.json()
            results = []
            for item in data:
                addr = item.get("address", {})
                results.append(Location(
                    region=item.get("display_name", "").split(',')[0],
                    country=addr.get("country_code", "").upper(),
                    lat=float(item["lat"]),
                    lon=float(item["lon"]),
                    display_name=item["display_name"]
                ))
            if not self.isInterruptionRequested():
                print(f"Nominatim returned: {len(results)} results")
                self.results_ready.emit(self.query_id, results)
        except Exception as e:
            if not self.isInterruptionRequested():
                self.error_occurred.emit(self.query_id, str(e))
                self.results_ready.emit(self.query_id, [])

class LocationSearchModel(QAbstractListModel):
    NameRole = Qt.ItemDataRole.UserRole + 1
    LatRole = NameRole + 1
    LonRole = LatRole + 1
    RegionRole = LonRole + 1
    CountryRole = RegionRole + 1

    def __init__(self, parent=None):
        super().__init__(parent)
        self._results = []
        self._worker = None
        self._last_query_id = 0
        print("LocationSearchModel created")

    def rowCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        return len(self._results)

    def roleNames(self):
        return {Qt.ItemDataRole.DisplayRole: QByteArray(b"display"),
                self.NameRole: QByteArray(b"cityName"),
                self.LatRole: QByteArray(b"lat"),
                self.LonRole: QByteArray(b"lon"),
                self.RegionRole: QByteArray(b"region"),
                self.CountryRole: QByteArray(b"country")}

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or index.row() >= len(self._results):
            return None
        loc = self._results[index.row()]

        if role == Qt.ItemDataRole.DisplayRole or role == self.NameRole:
            return loc.display_name
        if role == self.LatRole:
            return loc.lat
        if role == self.LonRole:
            return loc.lon
        if role == self.RegionRole:
            return loc.region
        if role == self.CountryRole:
            return loc.country
        return None

    @pyqtSlot(str)
    def search(self, query):
        print(f"Searching: '{query}'")
        if len(query) < 3:
            self.handle_results(self._last_query_id, [])
            return
        self._last_query_id += 1
        current_id = self._last_query_id
        if self._worker and self._worker.isRunning():
            self._worker.requestInterruption()
            self._worker.wait(1000)
            if self._worker.isRunning():
                self._worker.terminate()
                self._worker.wait()
        self._worker = SearchWorker(current_id, query)
        self._worker.results_ready.connect(self.handle_results)
        self._worker.error_occurred.connect(self.handle_error)
        self._worker.start()

    @pyqtSlot(int, list)
    def handle_results(self, query_id, new_results):
        if query_id == self._last_query_id:
            print(f"Updating model: {len(new_results)} items")
            self.beginResetModel()
            self._results = new_results
            self.endResetModel()

    @pyqtSlot(int, str)
    def handle_error(self, query_id, error_msg):
        if query_id == self._last_query_id:
            print(f"Search error: {error_msg}")

    @pyqtSlot(int, result='QVariant')
    def get_location(self, index):
        if 0 <= index < len(self._results):
            return dataclasses.asdict(self._results[index])
        return {}
