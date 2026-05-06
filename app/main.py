from fastapi import FastAPI
from app.core.config import settings
from app.api.users import router as users_router

app = FastAPI(title=settings.app_name, version=settings.app_version)
app.include_router(users_router, prefix="/api/v1")
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "version": settings.app_version,
        "debug": settings.debug
    }