from fastapi import FastAPI
from infrastructure.database import init_db
from infrastructure.fastapi_app.api.v1 import items

app = FastAPI()
app.include_router(items.router, prefix="/api/v1", tags=["items"])

@app.on_event("startup")
def on_startup():
    init_db()
