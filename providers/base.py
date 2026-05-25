from abc import ABC, abstractmethod
from dataclasses import dataclass

from models import Location

class BaseProvider(ABC):
    def __init__(self, location: Location):
        self.location = location

    @abstractmethod
    def fetch(self) -> list[str]:
        pass
