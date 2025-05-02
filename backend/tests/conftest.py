import os
import sys
import pytest
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy import text
from fastapi.testclient import TestClient
from datetime import datetime

# Asegurarse de que el directorio raíz está en el path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Importar después de asegurar que el path está configurado
from infrastructure.fastapi_app.main import app
from infrastructure.orm.models import User, Role, UserRole
from infrastructure.database import get_session
from app.use_cases.security_service import PasswordService
from infrastructure.orm.user_repository import SQLModelUserRepository
from infrastructure.orm.role_repository import SQLModelRoleRepository
from app.use_cases.auth_service import AuthService

# Crear una base de datos SQLite en memoria para las pruebas
TEST_DATABASE_URL = "sqlite:///./test.db"
test_engine = create_engine(TEST_DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

# Reemplazar la dependencia de sesión de base de datos en FastAPI
def get_test_session():
    with Session(test_engine) as session:
        yield session

app.dependency_overrides[get_session] = get_test_session

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Configurar la base de datos de prueba una vez para toda la sesión de prueba"""
    # Crear todas las tablas
    SQLModel.metadata.create_all(test_engine)
    
    yield
    
    # Limpiar después de todas las pruebas
    SQLModel.metadata.drop_all(test_engine)

@pytest.fixture(autouse=True)
def session():
    """Crear una sesión de base de datos para cada prueba con limpieza automática"""
    with Session(test_engine) as session:
        # Limpiar tablas antes de cada prueba
        session.exec(text("DELETE FROM UserRole"))
        session.exec(text("DELETE FROM User"))
        session.exec(text("DELETE FROM Role"))
        session.commit()
        
        # Crear roles básicos
        session.add(Role(name="ADMIN", description="Administrador"))
        session.add(Role(name="USER", description="Usuario Regular"))
        session.commit()
        
        yield session

@pytest.fixture
def test_client():
    with TestClient(app) as client:
        yield client

@pytest.fixture
def user_repository(session):
    return SQLModelUserRepository(session)

@pytest.fixture
def role_repository(session):
    return SQLModelRoleRepository(session)

@pytest.fixture
def auth_service(user_repository, role_repository):
    return AuthService(user_repository, role_repository)

@pytest.fixture
def test_user(session, auth_service):
    """Crear un usuario de prueba"""
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=PasswordService.hash_password("password123"),
        is_active=True,
        created_at=datetime.now()
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    
    # Agregar rol de usuario
    user_role = session.exec(text("SELECT * FROM Role WHERE name = 'USER'")).first()
    session.add(UserRole(user_id=user.id, role_id=user_role.id))
    session.commit()
    
    return auth_service.get_user_by_username("testuser")

@pytest.fixture
def test_admin_user(session, auth_service):
    """Crear un usuario administrador de prueba"""
    user = User(
        username="admin",
        email="admin@example.com",
        hashed_password=PasswordService.hash_password("admin123"),
        is_active=True,
        created_at=datetime.now()
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    
    # Agregar roles
    admin_role = session.exec(text("SELECT * FROM Role WHERE name = 'ADMIN'")).first()
    user_role = session.exec(text("SELECT * FROM Role WHERE name = 'USER'")).first()
    
    session.add(UserRole(user_id=user.id, role_id=admin_role.id))
    session.add(UserRole(user_id=user.id, role_id=user_role.id))
    session.commit()
    
    return auth_service.get_user_by_username("admin")

@pytest.fixture
def auth_header(test_user, auth_service):
    """Proporcionar un header de autorización para un usuario autenticado"""
    token = auth_service.create_access_token(test_user)
    return {"Authorization": f"Bearer {token}"}