from dataclasses import dataclass

@dataclass
class Location:
    region: str
    country: str
    lat: float
    lon: float
    display_name: str

@dataclass
class Alert:
    source: str      # e.g., 'Weather', 'Earthquake'
    message: str     # Human-readable description
    severity: str    # 'INFO', 'WARNING', 'CRITICAL'
    raw_data: str    # Original text to pass to AI if needed