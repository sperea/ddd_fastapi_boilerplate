from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING, ForwardRef
from datetime import datetime

# Definir el modelo de enlace primero
class UserRole(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    role_id: int = Field(foreign_key="role.id", primary_key=True)

# Definir los modelos principales con referencias correctas
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    
    # Relaciones
    roles: List["Role"] = Relationship(back_populates="users", link_model=UserRole)

class Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = None
    
    # Relación con usuarios
    users: List[User] = Relationship(back_populates="roles", link_model=UserRole)

# Declaración tardía para resolver referencias circulares
User.model_rebuild()
Role.model_rebuild()