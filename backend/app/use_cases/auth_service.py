from datetime import datetime, timedelta, UTC
from typing import Optional, Dict, Any
import jwt

from app.domain.models import UserDomain, RoleDomain, InvalidCredentialsError, UserAlreadyExistsError
from app.interfaces.repositories import UserRepository, RoleRepository
from app.use_cases.security_service import PasswordService

# Constantes para JWT
SECRET_KEY = "your-secret-key"  # ¡En producción, usa variables de entorno!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class AuthService:
    """
    Servicio de aplicación para gestionar la autenticación y autorización de usuarios.
    """
    
    def __init__(self, user_repository: UserRepository, role_repository: RoleRepository):
        self.user_repository = user_repository
        self.role_repository = role_repository
    
    def register_user(self, username: str, email: str, password: str) -> UserDomain:
        """
        Registra un nuevo usuario en el sistema
        """
        # Verificar si ya existe el usuario
        if self.user_repository.find_by_username(username):
            raise UserAlreadyExistsError(f"El usuario {username} ya existe")
        
        if self.user_repository.find_by_email(email):
            raise UserAlreadyExistsError(f"El email {email} ya está registrado")
        
        # Crear entidad de dominio
        user_domain = UserDomain(
            id=None,
            username=username,
            email=email,
            hashed_password=PasswordService.hash_password(password),
            is_active=True,
            roles=[]
        )
        
        # Guardar en repositorio
        saved_user = self.user_repository.save(user_domain)
        
        # Verificar si existe el rol USER, si no, crearlo
        user_role = self.role_repository.find_by_name("USER")
        if not user_role:
            role_domain = RoleDomain(id=None, name="USER", description="Usuario regular")
            user_role = self.role_repository.save(role_domain)
        
        # Asignar rol básico al nuevo usuario
        self.user_repository.add_role_to_user(saved_user.id, "USER")
        
        # Recargar el usuario para incluir el rol
        return self.user_repository.find_by_id(saved_user.id)
    
    def authenticate_user(self, username: str, password: str) -> UserDomain:
        """
        Autentica a un usuario y devuelve su información de dominio
        """
        user = self.user_repository.find_by_username(username)
        if not user:
            raise InvalidCredentialsError("Credenciales incorrectas")
        
        # Verificar contraseña usando el servicio
        if not PasswordService.verify_password(password, user.hashed_password):
            raise InvalidCredentialsError("Credenciales incorrectas")
        
        # Verificar si la cuenta está activa
        if not user.is_active:
            raise InvalidCredentialsError("Tu cuenta está desactivada")
        
        return user
    
    def create_access_token(self, user_domain: UserDomain) -> str:
        """
        Crea un token JWT para el usuario autenticado
        """
        # Datos para incluir en el token
        token_data = {
            "sub": user_domain.username,
            "id": user_domain.id,
            "email": user_domain.email,
            "roles": user_domain.roles,
            "exp": datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        }
        
        # Crear token
        encoded_jwt = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verifica un token JWT y devuelve los datos de usuario
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username is None:
                return None
            return payload
        except jwt.PyJWTError:
            return None
    
    def get_user_by_username(self, username: str) -> Optional[UserDomain]:
        """
        Obtiene un usuario por su nombre de usuario
        """
        return self.user_repository.find_by_username(username)