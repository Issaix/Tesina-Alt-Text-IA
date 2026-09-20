from fastapi import APIRouter

router = APIRouter()


@router.get(
    "/health",
    status_code=200,
    tags=["Health"],
    summary="Comprobar que la aplicación responde",
    description="Comprueba que la aplicación está en ejecución y responde solicitudes. No verifica modelos de IA ni dependencias externas.",
)
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "alt-text", "version": "0.1.0"}
