import pytest
from app.domain.models import InvalidCredentialsError, UserAlreadyExistsError

class TestAuthService:
    """
    Tests unitarios para el servicio de autenticación
    """
    
    def test_register_user_success(self, auth_service):
        """Test que un usuario se registra correctamente"""
        user = auth_service.register_user(
            username="newuser",
            email="newuser@example.com",
            password="secure123"
        )
        
        assert user is not None
        assert user.id is not None
        assert user.username == "newuser"
        assert user.email == "newuser@example.com"
        assert "USER" in user.roles
    
    def test_register_user_duplicate_username(self, auth_service, test_user):
        """Test que verifica que no se puede registrar un usuario con nombre duplicado"""
        with pytest.raises(UserAlreadyExistsError):
            auth_service.register_user(
                username="testuser",  # username ya existente
                email="another@example.com",
                password="password123"
            )
    
    def test_register_user_duplicate_email(self, auth_service, test_user):
        """Test que verifica que no se puede registrar un usuario con email duplicado"""
        with pytest.raises(UserAlreadyExistsError):
            auth_service.register_user(
                username="another_user",
                email="test@example.com",  # email ya existente
                password="password123"
            )
    
    def test_authenticate_user_success(self, auth_service, test_user):
        """Test que verifica que un usuario puede autenticarse correctamente con credenciales válidas"""
        user = auth_service.authenticate_user(
            username="testuser",
            password="password123"
        )
        
        assert user is not None
        assert user.id == test_user.id
        assert user.username == "testuser"
    
    def test_authenticate_user_invalid_username(self, auth_service):
        """Test que verifica que no se puede autenticar un usuario con nombre de usuario inválido"""
        with pytest.raises(InvalidCredentialsError):
            auth_service.authenticate_user(
                username="nonexistent",
                password="password123"
            )
    
    def test_authenticate_user_invalid_password(self, auth_service, test_user):
        """Test que verifica que no se puede autenticar un usuario con contraseña inválida"""
        with pytest.raises(InvalidCredentialsError):
            auth_service.authenticate_user(
                username="testuser",
                password="wrong_password"
            )
    
    def test_create_access_token(self, auth_service, test_user):
        """Test que verifica la creación correcta de un token de acceso"""
        token = auth_service.create_access_token(test_user)
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_verify_token_valid(self, auth_service, test_user):
        """Test que verifica que un token válido se verifica correctamente"""
        token = auth_service.create_access_token(test_user)
        payload = auth_service.verify_token(token)
        
        assert payload is not None
        assert payload["sub"] == test_user.username
        assert payload["id"] == test_user.id
        assert "roles" in payload
    
    def test_verify_token_invalid(self, auth_service):
        """Test que verifica que un token inválido no se verifica"""
        payload = auth_service.verify_token("invalid_token")
        assert payload is None