from fastapi import FastAPI

from app.api.health import router

app = FastAPI(
    title="Tesina Alt-Text IA",
    description="Microservicio para generar descripciones textuales en español de imágenes educativas.",
    version="0.1.0",
)

app.include_router(router)
