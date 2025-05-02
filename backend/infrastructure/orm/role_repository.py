from sqlmodel import Session, select
from typing import List, Optional
from app.domain.models import RoleDomain
from app.interfaces.repositories import RoleRepository
from infrastructure.orm.models import Role

class SQLModelRoleRepository(RoleRepository):
    def __init__(self, session: Session):
        self.session = session
    
    def get_all(self) -> List[RoleDomain]:
        statement = select(Role)
        roles = self.session.exec(statement).all()
        return [self._to_domain(role) for role in roles]
    
    def find_by_id(self, role_id: int) -> Optional[RoleDomain]:
        role = self.session.get(Role, role_id)
        if not role:
            return None
        return self._to_domain(role)
    
    def find_by_name(self, name: str) -> Optional[RoleDomain]:
        # Normalizar el nombre para buscar
        name = name.upper()
        statement = select(Role).where(Role.name == name)
        role = self.session.exec(statement).first()
        if not role:
            return None
        return self._to_domain(role)
    
    def save(self, role_domain: RoleDomain) -> RoleDomain:
        # Si ya existe, actualizar
        if role_domain.id:
            return self.update(role_domain)
            
        # Normalizar el nombre antes de guardar
        name = role_domain.name.upper()
        
        # Convertir a modelo ORM
        role = Role(
            name=name,
            description=role_domain.description
        )
        
        # Guardar en base de datos
        self.session.add(role)
        self.session.commit()
        self.session.refresh(role)
        
        # Retornar objeto de dominio actualizado
        return self._to_domain(role)
    
    def update(self, role_domain: RoleDomain) -> RoleDomain:
        # Buscar rol existente
        role = self.session.get(Role, role_domain.id)
        if not role:
            raise ValueError(f"No se encontró el rol con ID {role_domain.id}")
        
        # Normalizar el nombre antes de actualizar
        name = role_domain.name.upper()
        
        # Actualizar campos
        role.name = name
        role.description = role_domain.description
        
        # Guardar cambios
        self.session.add(role)
        self.session.commit()
        self.session.refresh(role)
        
        return self._to_domain(role)
    
    def delete(self, role_id: int) -> None:
        role = self.session.get(Role, role_id)
        if role:
            self.session.delete(role)
            self.session.commit()
    
    # Métodos auxiliares privados
    def _to_domain(self, role: Role) -> RoleDomain:
        """Convierte un modelo ORM a modelo de dominio"""
        return RoleDomain(
            id=role.id,
            name=role.name,
            description=role.description
        )