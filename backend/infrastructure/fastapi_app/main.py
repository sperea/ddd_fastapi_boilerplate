from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from infrastructure.database import init_db
from infrastructure.fastapi_app.api.v1 import items

app = FastAPI(
    title="Clean Architecture FastAPI",
    description="Una API basada en FastAPI con arquitectura limpia y DDD",
    version="1.0.0"
)
app.include_router(items.router, prefix="/api/v1", tags=["items"])

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
                max-width: 800px;
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
            }
            .endpoint {
                background-color: #f9f9f9;
                padding: 15px;
                border-left: 3px solid #3498db;
                margin-bottom: 10px;
            }
            .method {
                font-weight: bold;
                color: #27ae60;
            }
            .path {
                font-family: monospace;
                background-color: #ecf0f1;
                padding: 2px 5px;
            }
            footer {
                margin-top: 30px;
                border-top: 1px solid #ddd;
                padding-top: 10px;
                color: #7f8c8d;
                font-size: 0.9em;
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
        
        <div class="endpoint">
            <p><span class="method">GET</span> <span class="path">/api/v1/</span></p>
            <p>Obtiene la lista de todos los items disponibles.</p>
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

@app.on_event("startup")
def on_startup():
    init_db()
