from fastapi import FastAPI

from app import __version__
from app.api.describe import router as describe_router
from app.api.health import router as health_router


def create_app() -> FastAPI:
    """Construye la API sin cargar los modelos."""
    application = FastAPI(
        title="Tesina Alt-Text IA",
        description="Genera una descripción en español a partir de una imagen educativa.",
        version=__version__,
    )
    application.include_router(health_router)
    application.include_router(describe_router)
    return application


app = create_app()
