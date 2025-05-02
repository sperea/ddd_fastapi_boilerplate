import bcrypt
from app.domain.models import UserDomain

class PasswordService:
    """
    Servicio para manejar operaciones relacionadas con contraseñas.
    Este servicio separa la lógica de hashing de contraseñas del modelo de dominio.
    """
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Crea un hash seguro para una contraseña.
        """
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verifica si una contraseña en texto plano coincide con el hash almacenado.
        """
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    
    @staticmethod
    def update_user_password(user: UserDomain, new_password: str) -> UserDomain:
        """
        Actualiza la contraseña de un usuario.
        """
        user.hashed_password = PasswordService.hash_password(new_password)
        user.plain_password = None
        return user