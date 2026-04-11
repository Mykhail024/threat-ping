from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class Location:
    region: str
    country: str
    lat: float
    lon: float
    display_name: str


class BaseProvider(ABC):
    def __init__(self, location: Location):
        self.location = location

    @abstractmethod
    def fetch(self) -> list[str]:
        pass
