from typing import Optional, List
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

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

class UserAlreadyExistsError(DomainException):
    """Se lanza cuando se intenta crear un usuario que ya existe"""
    pass

class InvalidCredentialsError(DomainException):
    """Se lanza cuando las credenciales proporcionadas son inválidas"""
    pass

class UnauthorizedError(DomainException):
    """Se lanza cuando un usuario intenta acceder a un recurso sin autorización"""
    pass

@dataclass
class RoleDomain:
    """
    Modelo de dominio para Role.
    """
    id: Optional[int]
    name: str
    description: Optional[str] = None
    
    def __post_init__(self):
        if not self.name:
            raise DomainException("Role name is required")
        
        # Normalizar el nombre del rol
        self.name = self.name.upper()

@dataclass
class UserDomain:
    """
    Modelo de dominio para User. 
    """
    id: Optional[int]
    username: str
    email: str
    hashed_password: Optional[str] = None
    plain_password: Optional[str] = None
    is_active: bool = True
    created_at: datetime = None
    updated_at: Optional[datetime] = None
    roles: List[str] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
            
        if self.roles is None:
            self.roles = []
            
        if len(self.username) < 3:
            raise DomainException("El nombre de usuario debe tener al menos 3 caracteres")
    
    def hash_password(self):
        """Hashea la contraseña en texto plano"""
        if not self.plain_password:
            raise DomainException("No password provided")
        
        # Aquí usaremos una función hash de la capa de servicios
        # en lugar de implementarla directamente para mantener el dominio puro
        self.plain_password = None  # Eliminar contraseña en texto plano después de hashear
    
    def verify_password(self, password: str) -> bool:
        """
        Determina si la contraseña proporcionada coincide con el hash almacenado.
        Esta es una operación de dominio que requiere un servicio externo para la verificación.
        """
        # Esta función debe ser implementada por un servicio externo
        # para mantener el dominio puro
        return False  # Placeholder, será reemplazado por el servicio
    
    def assign_role(self, role_name: str):
        """Asigna un rol al usuario"""
        role_name = role_name.upper()
        if role_name not in self.roles:
            self.roles.append(role_name)
            self.updated_at = datetime.now()
    
    def remove_role(self, role_name: str):
        """Remueve un rol del usuario"""
        role_name = role_name.upper()
        if role_name in self.roles:
            self.roles.remove(role_name)
            self.updated_at = datetime.now()
    
    def has_role(self, role_name: str) -> bool:
        """Verifica si el usuario tiene un rol específico"""
        return role_name.upper() in [r.upper() for r in self.roles]
    
    def deactivate(self):
        """Desactiva la cuenta de usuario"""
        self.is_active = False
        self.updated_at = datetime.now()
    
    def activate(self):
        """Activa la cuenta de usuario"""
        self.is_active = True
        self.updated_at = datetime.now()
