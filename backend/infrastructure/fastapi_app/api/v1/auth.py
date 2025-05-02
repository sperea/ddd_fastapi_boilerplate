from fastapi import APIRouter, Depends, HTTPException, status
from infrastructure.fastapi_app.models import (
    UserLoginRequest, 
    UserRegisterRequest, 
    TokenResponse, 
    UserResponse
)
from infrastructure.fastapi_app.dependencies import get_auth_service
from app.use_cases.auth_service import AuthService
from app.domain.models import InvalidCredentialsError, UserAlreadyExistsError

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegisterRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Registra un nuevo usuario en el sistema
    """
    try:
        user = auth_service.register_user(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password
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
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al registrar usuario: {str(e)}"
        )

@router.post("/token", response_model=TokenResponse)
async def login_for_access_token(
    user_credentials: UserLoginRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Obtiene un token de acceso con las credenciales proporcionadas
    """
    try:
        user = auth_service.authenticate_user(
            username=user_credentials.username,
            password=user_credentials.password
        )
        
        access_token = auth_service.create_access_token(user)
        
        return TokenResponse(
            access_token=access_token,
            user_id=user.id,
            username=user.username,
            roles=user.roles
        )
    except InvalidCredentialsError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )