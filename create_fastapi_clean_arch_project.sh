#!/bin/bash

PROJECT_NAME="my_project"
mkdir -p $PROJECT_NAME/{app/{domain,interfaces,services,use_cases},infrastructure/fastapi_app/api/v1,infrastructure/fastapi_app/admin,infrastructure,tests}

cd $PROJECT_NAME

echo "✅ Estructura de carpetas creada."

# requirements.txt
cat <<EOF > requirements.txt
fastapi
uvicorn[standard]
sqlmodel
sqlalchemy
fastapi-admin
aiosqlite
EOF

# database.py
cat <<EOF > infrastructure/database.py
from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///./db.sqlite3"
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    from app.domain.models import Item
    SQLModel.metadata.create_all(engine)
EOF

# config.py (vacío por ahora)
touch infrastructure/config.py

# models.py
cat <<EOF > app/domain/models.py
from sqlmodel import SQLModel, Field
from typing import Optional

class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
EOF

# interfaces/repositories.py
cat <<EOF > app/interfaces/repositories.py
from abc import ABC, abstractmethod
from typing import List
from app.domain.models import Item

class ItemRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Item]:
        pass
EOF

# services/sqlmodel_repo.py
cat <<EOF > app/services/sqlmodel_repo.py
from sqlmodel import Session, select
from typing import List
from app.domain.models import Item
from app.interfaces.repositories import ItemRepository

class SQLModelItemRepository(ItemRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Item]:
        statement = select(Item)
        return self.session.exec(statement).all()
EOF

# use_cases/operations.py
cat <<EOF > app/use_cases/operations.py
from app.interfaces.repositories import ItemRepository

def list_items(repo: ItemRepository):
    return repo.get_all()
EOF

# main.py
cat <<EOF > infrastructure/fastapi_app/main.py
from fastapi import FastAPI
from infrastructure.database import init_db
from infrastructure.fastapi_app.api.v1 import items

app = FastAPI()
app.include_router(items.router, prefix="/api/v1", tags=["items"])

@app.on_event("startup")
def on_startup():
    init_db()
EOF

# items.py
cat <<EOF > infrastructure/fastapi_app/api/v1/items.py
from fastapi import APIRouter, Depends
from sqlmodel import Session
from infrastructure.database import get_session
from app.services.sqlmodel_repo import SQLModelItemRepository
from app.use_cases.operations import list_items

router = APIRouter()

@router.get("/")
def get_items(session: Session = Depends(get_session)):
    repo = SQLModelItemRepository(session)
    return list_items(repo)
EOF

# dependencies.py (vacío por ahora)
touch infrastructure/fastapi_app/dependencies.py

echo "✅ Archivos generados con éxito."
echo ""
echo "👉 Recuerda activar tu entorno virtual e instalar dependencias con:"
echo "   pip install -r requirements.txt"
echo ""
echo "🚀 Para ejecutar el proyecto:"
echo "   uvicorn infrastructure.fastapi_app.main:app --reload"
