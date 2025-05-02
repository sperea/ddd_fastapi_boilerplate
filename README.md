## 📄 `README.md`


# 🧱 FastAPI Clean Architecture Starter

Este proyecto es una plantilla inicial para crear APIs REST en Python con FastAPI, basada en **Clean Architecture** y **Domain-Driven Design (DDD)**. Utiliza **SQLModel** como ORM, soporta logs estructurados a consola y archivo, y está preparada para extensiones como autenticación JWT, FastAPI-Admin y observabilidad avanzada.

---

## 🗂 Estructura del Proyecto

```bash
backend/
├── app/                      # Dominio, interfaces y lógica de negocio
│   ├── domain/               # Modelos del dominio (SQLModel)
│   ├── interfaces/           # Puertos / interfaces
│   ├── services/             # Adaptadores / implementación de puertos
│   ├── use_cases/            # Casos de uso
│   └── auth/                 # (opcional) Autenticación
├── infrastructure/
│   ├── database.py           # Engine y sesión SQLModel
│   ├── config.py             # Configuración general
│   ├── logging/logger.py     # Configuración de logging (rotación incluida)
│   └── fastapi_app/
│       ├── main.py           # Aplicación FastAPI
│       ├── api/v1/           # Rutas organizadas por versión
│       └── dependencies.py
├── logs/                     # Carpeta generada automáticamente para logs
├── main.py                   # Punto de entrada (ejecuta Uvicorn)
├── requirements.txt
└── README.md
```

---

## 🚀 Cómo ejecutar

### 1. Crear entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar la app

```bash
python main.py
```

La API estará disponible en: [http://localhost:8000](http://localhost:8000)  
Documentación automática en: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🛠 Funcionalidades incluidas

- ✅ API modular con FastAPI
- ✅ Estructura limpia y desacoplada (DDD + Clean Architecture)
- ✅ ORM: SQLModel (sobre SQLAlchemy y Pydantic)
- ✅ Logs en consola y en archivo (`logs/app.log`)
- ✅ Rotación automática de logs (1MB, 5 copias)
- ✅ Punto de entrada limpio con `main.py`
- ⏳ Preparado para:
  - JWT Auth
  - FastAPI-Admin
  - Observabilidad (Prometheus, OpenTelemetry, etc.)

---

## 🧪 Pruebas

El proyecto incluye una suite completa de tests organizados por niveles siguiendo las mejores prácticas para arquitecturas limpias:

### Estructura de Tests

```
tests/
├── conftest.py                # Configuración y fixtures de pytest
├── unit/                      # Tests unitarios
│   ├── domain/                # Tests de modelos de dominio
│   └── use_cases/             # Tests de casos de uso
├── integration/               # Tests de integración
│   └── test_auth_api.py       # Tests de la API de autenticación
└── e2e/                       # Tests End-to-End
    └── test_auth_flow.py      # Flujos completos de autenticación
```

### Ejecución de Tests

Para ejecutar todos los tests:

```bash
# Desde la raíz del proyecto
cd backend
pytest
```

Para ejecutar tests específicos:

```bash
# Tests unitarios
pytest tests/unit/

# Tests de integración
pytest tests/integration/

# Tests end-to-end
pytest tests/e2e/

# Tests específicos por nombre
pytest tests/ -k "login"

# Con más detalle y reporte de cobertura
pytest tests/ -v --cov=app --cov=infrastructure
```

### Requisitos para Testing

Instala las dependencias de desarrollo:

```bash
pip install pytest pytest-cov
```

### Docker

Si utilizas Docker, puedes ejecutar los tests dentro del contenedor:

```bash
docker compose run --rm web pytest
```

---

## 📦 Dependencias principales

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLModel](https://sqlmodel.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [Passlib + PyJWT (opcional para Auth)](https://passlib.readthedocs.io/)
- [FastAPI-Admin](https://github.com/fastapi-admin/fastapi-admin)

---

## 📄 Licencia

MIT

---

