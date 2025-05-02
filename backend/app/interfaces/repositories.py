from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models import UserDomain, RoleDomain


class UserRepository(ABC):
    """
    Repositorio para gestionar las operaciones relacionadas con usuarios.
    """
    @abstractmethod
    def get_all(self) -> List[UserDomain]:
        """Obtiene todos los usuarios registrados."""
        pass
    
    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[UserDomain]:
        """Busca un usuario por su ID."""
        pass
    
    @abstractmethod
    def find_by_username(self, username: str) -> Optional[UserDomain]:
        """Busca un usuario por su nombre de usuario."""
        pass
    
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[UserDomain]:
        """Busca un usuario por su correo electrónico."""
        pass
    
    @abstractmethod
    def save(self, user: UserDomain) -> UserDomain:
        """Guarda un usuario en la base de datos."""
        pass
    
    @abstractmethod
    def update(self, user: UserDomain) -> UserDomain:
        """Actualiza un usuario existente."""
        pass
    
    @abstractmethod
    def delete(self, user_id: int) -> None:
        """Elimina un usuario por su ID."""
        pass
    
    @abstractmethod
    def get_user_roles(self, user_id: int) -> List[str]:
        """Obtiene todos los nombres de roles asignados a un usuario."""
        pass
    
    @abstractmethod
    def add_role_to_user(self, user_id: int, role_name: str) -> None:
        """Asigna un rol a un usuario."""
        pass
    
    @abstractmethod
    def remove_role_from_user(self, user_id: int, role_name: str) -> None:
        """Remueve un rol de un usuario."""
        pass

class RoleRepository(ABC):
    """
    Repositorio para gestionar las operaciones relacionadas con roles.
    """
    @abstractmethod
    def get_all(self) -> List[RoleDomain]:
        """Obtiene todos los roles disponibles."""
        pass
    
    @abstractmethod
    def find_by_id(self, role_id: int) -> Optional[RoleDomain]:
        """Busca un rol por su ID."""
        pass
    
    @abstractmethod
    def find_by_name(self, name: str) -> Optional[RoleDomain]:
        """Busca un rol por su nombre."""
        pass
    
    @abstractmethod
    def save(self, role: RoleDomain) -> RoleDomain:
        """Guarda un nuevo rol."""
        pass
    
    @abstractmethod
    def update(self, role: RoleDomain) -> RoleDomain:
        """Actualiza un rol existente."""
        pass
    
    @abstractmethod
    def delete(self, role_id: int) -> None:
        """Elimina un rol por su ID."""
        pass
