from sqlmodel import SQLModel, Field
from typing import Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto

class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    status: str = Field(default="available")

class ItemStatus(Enum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    SOLD_OUT = "sold_out"

class DomainException(Exception):
    """Excepción base para errores de dominio"""
    pass

class InvalidItemOperation(DomainException):
    """Se lanza cuando se intenta realizar una operación no permitida sobre un item"""
    pass

@dataclass
class ItemDomain:
    """
    Modelo de dominio para Item. 
    En DDD, las entidades de dominio contienen no solo datos, sino también comportamiento y reglas de negocio.
    """
    id: Optional[int]
    name: str
    description: Optional[str] = None
    created_at: datetime = None
    updated_at: Optional[datetime] = None
    status: str = ItemStatus.AVAILABLE.value
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        
        if len(self.name) < 3:
            raise DomainException("El nombre del item debe tener al menos 3 caracteres.")
    
    def update_description(self, new_description: str):
        """Actualiza la descripción y marca la entidad como modificada"""
        self.description = new_description
        self.updated_at = datetime.now()
    
    def reserve(self):
        """Marca el item como reservado"""
        if self.status == ItemStatus.SOLD_OUT.value:
            raise InvalidItemOperation("No se puede reservar un item que está agotado")
        
        self.status = ItemStatus.RESERVED.value
        self.updated_at = datetime.now()
    
    def mark_as_sold_out(self):
        """Marca el item como agotado"""
        self.status = ItemStatus.SOLD_OUT.value
        self.updated_at = datetime.now()
    
    def make_available(self):
        """Marca el item como disponible"""
        self.status = ItemStatus.AVAILABLE.value
        self.updated_at = datetime.now()
        
    def is_available(self) -> bool:
        """Verifica si el item está disponible"""
        return self.status == ItemStatus.AVAILABLE.value
