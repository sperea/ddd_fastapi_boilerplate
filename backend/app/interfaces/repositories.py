from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models import Item

class ItemRepository(ABC):
    """
    Repositorio para gestionar las operaciones de dominio relacionadas con Items.
    En DDD, los repositorios representan colecciones de objetos de dominio, no solo operaciones CRUD.
    """
    @abstractmethod
    def get_all(self) -> List[Item]:
        """Obtiene todos los items disponibles en el catálogo."""
        pass
    
    @abstractmethod
    def find_by_id(self, item_id: int) -> Optional[Item]:
        """Busca un item específico por su identificador único."""
        pass
    
    @abstractmethod
    def save(self, item: Item) -> Item:
        """
        Persiste un item en el repositorio.
        En DDD, esta operación podría incluir validaciones de dominio o eventos.
        """
        pass
    
    @abstractmethod
    def remove(self, item_id: int) -> None:
        """Elimina un item del repositorio."""
        pass
    
    @abstractmethod
    def find_by_name(self, name: str) -> List[Item]:
        """Busca items que coincidan con el nombre especificado."""
        pass
