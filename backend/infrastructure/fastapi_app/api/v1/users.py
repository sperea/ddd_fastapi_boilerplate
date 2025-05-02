from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.domain.models import UserDomain
from infrastructure.fastapi_app.dependencies import get_user_repository, get_role_repository, has_role, get_current_user
from infrastructure.fastapi_app.models import UserResponse, UserUpdateRequest
from app.interfaces.repositories import UserRepository, RoleRepository
from app.use_cases.security_service import PasswordService

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: UserDomain = Depends(get_current_user)
):
    """
    Obtiene información del usuario actual autenticado
    """
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        is_active=current_user.is_active,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
        roles=current_user.roles
    )

@router.get("", response_model=List[UserResponse])
async def get_all_users(
    user_repository: UserRepository = Depends(get_user_repository),
    _: UserDomain = Depends(has_role(["ADMIN"]))
):
    """
    Obtiene todos los usuarios (solo administradores)
    """
    users = user_repository.get_all()
    result = []
    
    for user in users:
        result.append(UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
            roles=user.roles
        ))
    
    return result

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    user_repository: UserRepository = Depends(get_user_repository),
    current_user: UserDomain = Depends(get_current_user)
):
    """
    Obtiene información de un usuario específico
    """
    # Solo el propio usuario o un admin pueden ver información de usuario
    if current_user.id != user_id and "ADMIN" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver información de este usuario"
        )
    
    user = user_repository.find_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at,
        roles=user.roles
    )

@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdateRequest,
    user_repository: UserRepository = Depends(get_user_repository),
    current_user: UserDomain = Depends(get_current_user)
):
    """
    Actualiza información de un usuario
    """
    # Solo el propio usuario o un admin pueden actualizar información
    if current_user.id != user_id and "ADMIN" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para actualizar este usuario"
        )
    
    user = user_repository.find_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Actualizar solo los campos proporcionados
    if user_data.email is not None:
        user.email = user_data.email
    
    if user_data.password is not None:
        user.hashed_password = PasswordService.hash_password(user_data.password)
    
    # Solo los admin pueden cambiar el estado activo/inactivo
    if user_data.is_active is not None and "ADMIN" in current_user.roles:
        user.is_active = user_data.is_active
    
    # Actualizar
    updated_user = user_repository.update(user)
    
    return UserResponse(
        id=updated_user.id,
        username=updated_user.username,
        email=updated_user.email,
        is_active=updated_user.is_active,
        created_at=updated_user.created_at,
        updated_at=updated_user.updated_at,
        roles=updated_user.roles
    )