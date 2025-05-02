from fastapi import Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from typing import List, Optional

from infrastructure.database import get_session
from infrastructure.orm.user_repository import SQLModelUserRepository
from infrastructure.orm.role_repository import SQLModelRoleRepository
from app.use_cases.auth_service import AuthService
from app.domain.models import UserDomain

# OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

# Obtener repositorios
def get_user_repository(session: Session = Depends(get_session)):
    return SQLModelUserRepository(session)

def get_role_repository(session: Session = Depends(get_session)):
    return SQLModelRoleRepository(session)

# Obtener servicios
def get_auth_service(
    user_repository = Depends(get_user_repository),
    role_repository = Depends(get_role_repository)
):
    return AuthService(user_repository, role_repository)

# Verificar y obtener el usuario actual
def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service)
):
    payload = auth_service.verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = auth_service.get_user_by_username(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo",
        )
    
    return user

# Verificar roles
def has_role(required_roles: List[str]):
    def _has_role(user: UserDomain = Security(get_current_user)):
        for role in required_roles:
            if role in user.roles:
                return user
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Acceso denegado. Se requiere uno de estos roles: {', '.join(required_roles)}",
        )
    return _has_role