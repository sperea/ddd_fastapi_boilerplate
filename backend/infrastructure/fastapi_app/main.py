import contextlib
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from infrastructure.database import init_db
from infrastructure.fastapi_app.api.v1 import auth, users
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código de inicialización: se ejecuta antes de iniciar la aplicación
    init_db()
    yield
    # Código de limpieza: se ejecuta al cerrar la aplicación
    pass

app = FastAPI(
    title="Clean Architecture FastAPI",
    description="Una API basada en FastAPI con arquitectura limpia y DDD",
    version="1.0.0",
    lifespan=lifespan
)

# Routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["autenticación"])
app.include_router(users.router, prefix="/api/v1/users", tags=["usuarios"])

@app.get("/", response_class=HTMLResponse, tags=["documentación"])
async def get_api_info():
    """
    Muestra información general sobre la API.
    """
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Clean Architecture FastAPI</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                max-width: 900px;
                margin: 0 auto;
                padding: 20px;
                color: #333;
            }
            h1 {
                color: #2c3e50;
                border-bottom: 2px solid #3498db;
                padding-bottom: 10px;
            }
            h2 {
                color: #2980b9;
                margin-top: 30px;
            }
            h3 {
                color: #16a085;
                margin-top: 20px;
            }
            .endpoint {
                background-color: #f9f9f9;
                padding: 15px;
                border-left: 3px solid #3498db;
                margin-bottom: 10px;
                border-radius: 4px;
            }
            .method {
                font-weight: bold;
                display: inline-block;
                min-width: 60px;
            }
            .method.get {
                color: #27ae60;
            }
            .method.post {
                color: #2980b9;
            }
            .method.put, .method.patch {
                color: #f39c12;
            }
            .method.delete {
                color: #c0392b;
            }
            .path {
                font-family: monospace;
                background-color: #ecf0f1;
                padding: 2px 5px;
                border-radius: 3px;
            }
            .description {
                margin-top: 5px;
                margin-bottom: 0;
                color: #555;
            }
            .auth-required {
                font-size: 0.8em;
                margin-left: 10px;
                color: #e74c3c;
            }
            .role-required {
                font-size: 0.8em;
                margin-left: 5px;
                color: #8e44ad;
            }
            footer {
                margin-top: 40px;
                border-top: 1px solid #ddd;
                padding-top: 10px;
                color: #7f8c8d;
                font-size: 0.9em;
                text-align: center;
            }
            .section {
                margin-bottom: 30px;
            }
        </style>
    </head>
    <body>
        <h1>Clean Architecture FastAPI</h1>
        
        <p>Bienvenido a la API desarrollada con FastAPI siguiendo los principios de Clean Architecture y Domain-Driven Design (DDD).</p>
        
        <h2>Información General</h2>
        <ul>
            <li><strong>Versión:</strong> 1.0.0</li>
            <li><strong>Documentación API:</strong> <a href="/docs">/docs</a> (Swagger UI)</li>
            <li><strong>Documentación API Alternativa:</strong> <a href="/redoc">/redoc</a> (ReDoc)</li>
        </ul>
        
        <h2>Endpoints Disponibles</h2>
        
        <div class="section">
            <h3>🔐 Autenticación</h3>
            
            <div class="endpoint">
                <p>
                    <span class="method post">POST</span>
                    <span class="path">/api/v1/auth/register</span>
                </p>
                <p class="description">Registra un nuevo usuario en el sistema.</p>
            </div>
            
            <div class="endpoint">
                <p>
                    <span class="method post">POST</span>
                    <span class="path">/api/v1/auth/token</span>
                </p>
                <p class="description">Obtiene un token JWT para autenticación.</p>
            </div>
        </div>
        
        <div class="section">
            <h3>👤 Gestión de Usuarios</h3>
            
            <div class="endpoint">
                <p>
                    <span class="method get">GET</span>
                    <span class="path">/api/v1/users/me</span>
                    <span class="auth-required">🔒 Requiere autenticación</span>
                </p>
                <p class="description">Obtiene información del usuario autenticado.</p>
            </div>
            
            <div class="endpoint">
                <p>
                    <span class="method get">GET</span>
                    <span class="path">/api/v1/users</span>
                    <span class="auth-required">🔒 Requiere autenticación</span>
                    <span class="role-required">👑 Rol: ADMIN</span>
                </p>
                <p class="description">Obtiene la lista de todos los usuarios (solo administradores).</p>
            </div>
            
            <div class="endpoint">
                <p>
                    <span class="method get">GET</span>
                    <span class="path">/api/v1/users/{user_id}</span>
                    <span class="auth-required">🔒 Requiere autenticación</span>
                </p>
                <p class="description">Obtiene información de un usuario específico (propio usuario o admin).</p>
            </div>
            
            <div class="endpoint">
                <p>
                    <span class="method patch">PATCH</span>
                    <span class="path">/api/v1/users/{user_id}</span>
                    <span class="auth-required">🔒 Requiere autenticación</span>
                </p>
                <p class="description">Actualiza información de un usuario (propio usuario o admin).</p>
            </div>
        </div>
        
        <h2>Estructura del Proyecto</h2>
        <p>Este proyecto sigue los principios de Clean Architecture y Domain-Driven Design:</p>
        <ul>
            <li><strong>Domain Layer:</strong> Contiene las entidades y reglas de negocio centrales.</li>
            <li><strong>Application Layer:</strong> Contiene los casos de uso de la aplicación.</li>
            <li><strong>Infrastructure Layer:</strong> Proporciona implementaciones concretas para bases de datos, APIs, etc.</li>
        </ul>
        
        <footer>
            <p>Clean Architecture FastAPI &copy; 2025</p>
        </footer>
    </body>
    </html>
    """
    return html_content
