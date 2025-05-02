import time
from fastapi.testclient import TestClient
import pytest
from app.use_cases.auth_service import AuthService

class TestAuthFlow:
    def test_complete_auth_flow(self, test_client: TestClient):
        """Test del flujo completo de autenticación: registro -> login -> acceso a recursos protegidos"""
        # 1. Registrar un nuevo usuario con nombre único basado en timestamp
        username = f"flowuser_{int(time.time())}"
        register_response = test_client.post(
            "/api/v1/auth/register",
            json={
                "username": username,
                "email": f"{username}@example.com",
                "password": "flowpass123"
            }
        )
        
        assert register_response.status_code == 201
        
        # 2. Iniciar sesión con el usuario registrado
        login_response = test_client.post(
            "/api/v1/auth/token",
            json={
                "username": username,
                "password": "flowpass123"
            }
        )
        
        assert login_response.status_code == 200
        token_data = login_response.json()
        assert "access_token" in token_data
        assert token_data["token_type"] == "bearer"
        
        # 3. Acceder a un recurso protegido con el token
        headers = {"Authorization": f"Bearer {token_data['access_token']}"}
        me_response = test_client.get("/api/v1/users/me", headers=headers)
        
        assert me_response.status_code == 200
        user_data = me_response.json()
        assert user_data["username"] == username
        assert user_data["email"] == f"{username}@example.com"

    def test_token_expiration_simulation(self, test_client: TestClient, test_user, auth_service, monkeypatch):
        """
        Simula la expiración de un token y verifica que el acceso es denegado

        Nota: Este test simula la expiración de un token modificando la verificación del token,
        ya que esperar a que expire naturalmente no es práctico en tests automatizados.
        """
        # 1. Login para obtener un token válido
        login_response = test_client.post(
            "/api/v1/auth/token",
            json={
                "username": "testuser",
                "password": "password123"
            }
        )
        
        assert login_response.status_code == 200
        token_data = login_response.json()
        assert "access_token" in token_data
        
        # 2. Parchar el método de verificación de token a nivel de módulo
        import app.use_cases.auth_service as auth_module
        original_verify_token = auth_module.AuthService.verify_token
        
        def mock_verify_token(self, token):
            return None  # Simula token expirado o inválido
            
        monkeypatch.setattr(auth_module.AuthService, "verify_token", mock_verify_token)
        
        # 3. Intentar acceder a un recurso protegido con el token "expirado"
        headers = {"Authorization": f"Bearer {token_data['access_token']}"}
        me_response = test_client.get("/api/v1/users/me", headers=headers)
        
        # 4. Verificar que el acceso es denegado
        assert me_response.status_code == 401
        
        # 5. Restaurar la implementación original
        monkeypatch.setattr(auth_module.AuthService, "verify_token", original_verify_token)

    def test_logout_simulation(self, test_client: TestClient, test_user):
        """
        Simula el proceso de logout

        Nota: En JWT puro, el logout se maneja típicamente en el cliente eliminando el token,
        pero este test simula un flujo completo de logout incluyendo un posible endpoint para invalidar tokens.
        """
        # 1. Login para obtener un token
        login_response = test_client.post(
            "/api/v1/auth/token",
            json={
                "username": "testuser",
                "password": "password123"
            }
        )
        
        assert login_response.status_code == 200
        token_data = login_response.json()
        assert "access_token" in token_data
        
        # 2. Acceder a un recurso protegido con el token (validar que funciona)
        headers = {"Authorization": f"Bearer {token_data['access_token']}"}
        me_response = test_client.get("/api/v1/users/me", headers=headers)
        assert me_response.status_code == 200
        
        # 3. Simular logout (esto sería un nuevo endpoint)
        # Por ahora, simulamos que el cliente elimina el token
        headers_without_token = {}
        me_response_after_logout = test_client.get("/api/v1/users/me", headers=headers_without_token)
        
        # 4. Verificar que el acceso es denegado sin token
        assert me_response_after_logout.status_code == 401