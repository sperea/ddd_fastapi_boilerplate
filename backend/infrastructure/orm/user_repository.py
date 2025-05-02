from sqlmodel import Session, select
from typing import List, Optional
from app.domain.models import UserDomain
from app.interfaces.repositories import UserRepository
from infrastructure.orm.models import User, Role, UserRole
from datetime import datetime

class SQLModelUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session
    
    def get_all(self) -> List[UserDomain]:
        statement = select(User)
        users = self.session.exec(statement).all()
        return [self._to_domain(user) for user in users]
    
    def find_by_id(self, user_id: int) -> Optional[UserDomain]:
        user = self.session.get(User, user_id)
        if not user:
            return None
        return self._to_domain(user)
    
    def find_by_username(self, username: str) -> Optional[UserDomain]:
        statement = select(User).where(User.username == username)
        user = self.session.exec(statement).first()
        if not user:
            return None
        return self._to_domain(user)
    
    def find_by_email(self, email: str) -> Optional[UserDomain]:
        statement = select(User).where(User.email == email)
        user = self.session.exec(statement).first()
        if not user:
            return None
        return self._to_domain(user)
    
    def save(self, user_domain: UserDomain) -> UserDomain:
        # Si ya existe, actualizar
        if user_domain.id:
            return self.update(user_domain)
            
        # Convertir a modelo ORM
        user = User(
            username=user_domain.username,
            email=user_domain.email,
            hashed_password=user_domain.hashed_password,
            is_active=user_domain.is_active,
            created_at=user_domain.created_at,
            updated_at=user_domain.updated_at
        )
        
        # Guardar en base de datos
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        
        # Asignar roles si los hay
        if user_domain.roles:
            for role_name in user_domain.roles:
                self._add_role_to_user_internal(user.id, role_name)
                
        # Retornar objeto de dominio actualizado
        return self.find_by_id(user.id)
    
    def update(self, user_domain: UserDomain) -> UserDomain:
        # Buscar usuario existente
        user = self.session.get(User, user_domain.id)
        if not user:
            raise ValueError(f"No se encontró el usuario con ID {user_domain.id}")
        
        # Actualizar campos
        user.username = user_domain.username
        user.email = user_domain.email
        if user_domain.hashed_password:
            user.hashed_password = user_domain.hashed_password
        user.is_active = user_domain.is_active
        user.updated_at = datetime.now()
        
        # Guardar cambios
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        
        return self._to_domain(user)
    
    def delete(self, user_id: int) -> None:
        user = self.session.get(User, user_id)
        if user:
            # Eliminar primero relaciones
            self._delete_all_roles_for_user(user_id)
            # Luego eliminar usuario
            self.session.delete(user)
            self.session.commit()
    
    def get_user_roles(self, user_id: int) -> List[str]:
        # Obtener roles usando join
        statement = select(Role).join(UserRole).where(UserRole.user_id == user_id)
        roles = self.session.exec(statement).all()
        return [role.name for role in roles]
    
    def add_role_to_user(self, user_id: int, role_name: str) -> None:
        self._add_role_to_user_internal(user_id, role_name)
    
    def remove_role_from_user(self, user_id: int, role_name: str) -> None:
        # Buscar el rol
        statement = select(Role).where(Role.name == role_name.upper())
        role = self.session.exec(statement).first()
        
        if not role:
            return  # No existe el rol
        
        # Buscar la relación usuario-rol
        statement = select(UserRole).where(
            UserRole.user_id == user_id, 
            UserRole.role_id == role.id
        )
        user_role = self.session.exec(statement).first()
        
        if user_role:
            self.session.delete(user_role)
            self.session.commit()
    
    # Métodos auxiliares privados
    def _to_domain(self, user: User) -> UserDomain:
        """Convierte un modelo ORM a modelo de dominio"""
        roles = self.get_user_roles(user.id)
        
        return UserDomain(
            id=user.id,
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
            roles=roles
        )
    
    def _add_role_to_user_internal(self, user_id: int, role_name: str) -> None:
        """Lógica interna para añadir un rol a un usuario"""
        # Normalizar nombre
        role_name = role_name.upper()
        
        # Buscar el rol
        statement = select(Role).where(Role.name == role_name)
        role = self.session.exec(statement).first()
        
        if not role:
            # Crear rol si no existe
            role = Role(name=role_name, description=f"Rol {role_name}")
            self.session.add(role)
            self.session.commit()
            self.session.refresh(role)
        
        # Verificar si ya existe la relación
        statement = select(UserRole).where(
            UserRole.user_id == user_id, 
            UserRole.role_id == role.id
        )
        existing = self.session.exec(statement).first()
        
        if not existing:
            user_role = UserRole(user_id=user_id, role_id=role.id)
            self.session.add(user_role)
            self.session.commit()
    
    def _delete_all_roles_for_user(self, user_id: int) -> None:
        """Elimina todas las relaciones de rol para un usuario"""
        statement = select(UserRole).where(UserRole.user_id == user_id)
        user_roles = self.session.exec(statement).all()
        
        for user_role in user_roles:
            self.session.delete(user_role)
        
        self.session.commit()