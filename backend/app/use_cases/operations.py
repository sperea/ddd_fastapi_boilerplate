from typing import List, Optional
from app.interfaces.repositories import ItemRepository
from app.domain.models import Item, ItemDomain, DomainException, InvalidItemOperation

class ItemService:
    """
    Servicio de aplicación para gestionar las operaciones relacionadas con los Items.
    En DDD, los servicios de aplicación coordinan entre la capa de infraestructura y el dominio.
    """
    def __init__(self, repository: ItemRepository):
        self.repository = repository
    
    def get_all_items(self) -> List[Item]:
        """Obtiene todos los items disponibles"""
        return self.repository.get_all()
    
    def get_item_by_id(self, item_id: int) -> Optional[Item]:
        """Obtiene un item por su ID"""
        return self.repository.find_by_id(item_id)
    
    def create_item(self, name: str, description: Optional[str] = None) -> Item:
        """
        Crea un nuevo item con validaciones de dominio
        """
        # Crear primero como entidad de dominio para validar reglas de negocio
        domain_item = ItemDomain(id=None, name=name, description=description)
        # Si llegamos aquí, las validaciones han pasado
        new_item = Item(name=domain_item.name, description=domain_item.description)
        return self.repository.save(new_item)
    
    def update_item_description(self, item_id: int, new_description: str) -> Optional[Item]:
        """
        Actualiza la descripción de un item aplicando reglas de dominio
        """
        item = self.repository.find_by_id(item_id)
        if not item:
            return None
        
        # Convertir a modelo de dominio para aplicar reglas de negocio
        domain_item = ItemDomain(
            id=item.id, 
            name=item.name,
            description=item.description,
            status=getattr(item, 'status', 'available')
        )
        
        domain_item.update_description(new_description)
        
        # Actualizar el modelo de repositorio
        item.description = domain_item.description
        item.updated_at = domain_item.updated_at
        
        return self.repository.save(item)
    
    def reserve_item(self, item_id: int) -> Optional[Item]:
        """
        Reserva un item si está disponible
        """
        item = self.repository.find_by_id(item_id)
        if not item:
            return None
        
        domain_item = ItemDomain(
            id=item.id, 
            name=item.name,
            description=item.description,
            status=getattr(item, 'status', 'available')
        )
        
        try:
            domain_item.reserve()
            item.status = domain_item.status
            item.updated_at = domain_item.updated_at
            return self.repository.save(item)
        except InvalidItemOperation as e:
            # En un caso real, habría que manejar esta excepción de manera adecuada
            raise e

# Funciones auxiliares para operaciones simples (mantener compatibilidad con código existente)
def list_items(repo: ItemRepository) -> List[Item]:
    """Función auxiliar para mantener compatibilidad con código existente"""
    service = ItemService(repo)
    return service.get_all_items()
