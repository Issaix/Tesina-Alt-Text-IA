from fastapi import FastAPI

from app import __version__
from app.api.describe import router as describe_router
from app.api.health import router as health_router


def create_app() -> FastAPI:
    """Construye la API sin cargar los modelos."""
    application = FastAPI(
        title="Tesina Alt-Text IA",
        description=(
            "Genera borradores de descripciones en español para fotografías e ilustraciones "
            "de propósito general en contenidos educativos. Las imágenes con datos se "
            "utilizan en pruebas complementarias de limitaciones; no se clasifican "
            "automáticamente ni se garantiza su interpretación especializada."
        ),
        version=__version__,
    )
    application.include_router(health_router)
    application.include_router(describe_router)
    return application


app = create_app()
