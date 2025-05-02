import pytest
import time
from fastapi.testclient import TestClient
from app.domain.models import UserDomain

class TestAuthAPI:
    """
    Tests de integración para las APIs de autenticación
    """
    
    def test_register_user_success(self, test_client: TestClient):
        """Test que verifica el registro exitoso de un usuario a través de la API"""
        # Usar un nombre único basado en timestamp para evitar conflictos
        username = f"apiuser_{int(time.time())}"
        response = test_client.post(
            "/api/v1/auth/register",
            json={
                "username": username,
                "email": f"{username}@example.com",
                "password": "securepass123"
            }
        )
        
        assert response.status_code == 201
        
        # Verificar que el usuario se creó correctamente
        data = response.json()
        assert "id" in data
        assert data["username"] == username
        assert data["email"] == f"{username}@example.com"
        assert "hashed_password" not in data
    
    def test_register_user_duplicate(self, test_client: TestClient, test_user):
        """Test que verifica que no se puede registrar un usuario duplicado a través de la API"""
        response = test_client.post(
            "/api/v1/auth/register",
            json={
                "username": "testuser",  # Username ya existente
                "email": "another@example.com",
                "password": "securepass123"
            }
        )
        
        assert response.status_code == 409  # Conflict
    
    def test_login_success(self, test_client: TestClient, test_user):
        """Test que verifica el login exitoso y la obtención de un token JWT"""
        response = test_client.post(
            "/api/v1/auth/token",
            json={
                "username": "testuser",
                "password": "password123"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_invalid_credentials(self, test_client: TestClient):
        """Test que verifica que no se puede hacer login con credenciales inválidas"""
        response = test_client.post(
            "/api/v1/auth/token",
            json={
                "username": "testuser",
                "password": "wrongpassword"
            }
        )
        
        assert response.status_code == 401  # Unauthorized
    
    def test_get_current_user_with_token(self, test_client: TestClient, auth_header):
        """Test que verifica acceso a un endpoint protegido con un token válido"""
        response = test_client.get(
            "/api/v1/users/me",
            headers=auth_header
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
    
    def test_get_current_user_without_token(self, test_client: TestClient):
        """Test que verifica el acceso denegado a un endpoint protegido sin token"""
        response = test_client.get("/api/v1/users/me")
        assert response.status_code == 401
    
    def test_get_current_user_with_invalid_token(self, test_client: TestClient):
        """Test que verifica el acceso denegado con token inválido"""
        response = test_client.get(
            "/api/v1/users/me",
            headers={"Authorization": "Bearer invalid-token"}
        )
        assert response.status_code == 401