import uvicorn
from infrastructure.logging.logger import init_logging

if __name__ == "__main__":
    init_logging()
    uvicorn.run("infrastructure.fastapi_app.main:app", host="0.0.0.0", port=8000, reload=True)
