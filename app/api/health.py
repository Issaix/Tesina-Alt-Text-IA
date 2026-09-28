from fastapi import APIRouter

from app import __version__

router = APIRouter()


@router.get(
    "/health",
    status_code=200,
    tags=["Health"],
    summary="Comprobar que la aplicación responde",
    description=(
        "Comprueba que la API responde. "
        "La disponibilidad de los modelos se comprueba al procesar una imagen."
    ),
)
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "alt-text", "version": __version__}
