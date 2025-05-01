from abc import ABC, abstractmethod
from typing import List
from app.domain.models import Item

class ItemRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Item]:
        pass
