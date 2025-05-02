from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

# DTOs para la autenticación
class UserLoginRequest(BaseModel):
    username: str
    password: str

class UserRegisterRequest(BaseModel):
    username: str
    email: str = Field(..., description="Correo electrónico válido")
    password: str = Field(..., min_length=8, description="Contraseña (mínimo 8 caracteres)")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    username: str
    roles: List[str]

# DTOs para usuarios
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    roles: List[str]

class UserCreateRequest(BaseModel):
    username: str
    email: str
    password: str = Field(..., min_length=8)
    is_active: bool = True

class UserUpdateRequest(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8)
    is_active: Optional[bool] = None

# DTOs para roles
class RoleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

class RoleCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None

class RoleUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None