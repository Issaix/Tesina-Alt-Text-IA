import logging
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import BaseModel, Field
from starlette.concurrency import run_in_threadpool

from app import images
from app.captioning import CaptioningService, ModelBusyError, get_captioning_service
from app.images import ImageValidationError

router = APIRouter()
logger = logging.getLogger(__name__)


class DescriptionResponse(BaseModel):
    description: str = Field(min_length=1, description="Descripción generada en español")


class ErrorResponse(BaseModel):
    detail: str


@router.post(
    "/describe",
    tags=["Descripción"],
    response_model=DescriptionResponse,
    summary="Describir una imagen educativa en español",
    responses={
        400: {"model": ErrorResponse, "description": "Imagen vacía o dañada"},
        413: {"model": ErrorResponse, "description": "Tamaño o resolución excesivos"},
        415: {"model": ErrorResponse, "description": "Formato no admitido"},
        503: {"model": ErrorResponse, "description": "Modelo ocupado o no disponible"},
    },
)
async def describe_image(
    image: Annotated[UploadFile, File()],
    captioner: Annotated[CaptioningService, Depends(get_captioning_service)],
) -> DescriptionResponse:
    # Cerrar el archivo recibido también libera el temporal usado por multipart.
    try:
        data = await image.read(images.MAX_IMAGE_BYTES + 1)
    finally:
        await image.close()
    try:
        decoded = await run_in_threadpool(
            images.decode_image,
            data,
            image.filename or "",
            image.content_type,
        )
    except ImageValidationError as exc:
        raise HTTPException(exc.status_code, exc.detail) from exc
    finally:
        del data
    try:
        description = await run_in_threadpool(captioner.describe, decoded)
        if not isinstance(description, str) or not description.strip():
            raise RuntimeError("La descripción está vacía.")
        return DescriptionResponse(description=description.strip())
    except ModelBusyError as exc:
        raise HTTPException(
            503, "El modelo está ocupado. Intenta de nuevo.", headers={"Retry-After": "5"}
        ) from exc
    except Exception as exc:
        logger.exception("No se pudo generar la descripción")
        raise HTTPException(
            503, "No se pudo generar la descripción. Revisa la disponibilidad de los modelos."
        ) from exc
    finally:
        decoded.close()
