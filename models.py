from dataclasses import dataclass
from enum import Enum, auto

class AlertType(Enum):
    SAFE = auto()
    DANGER = auto()
    UNKNOWN = auto()

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
    type: AlertType
    raw_data: str    # Original text to pass to AI if needed
