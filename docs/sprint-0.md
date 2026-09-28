# Sprint 0: preparación del proyecto

En este sprint se preparó la estructura del microservicio y una primera ruta para comprobar que la API respondía. Este documento conserva lo realizado en esa etapa; las instrucciones actuales están en el [README](../README.md).

## Trabajo realizado

| Actividad | Resultado |
|---|---|
| Crear el repositorio y configurar accesos | Confirmado por el autor. |
| Preparar el entorno local | Se utilizó `.venv` y se registraron las dependencias. |
| Organizar la aplicación | Se separó la creación de la API de sus rutas. |
| Crear una ruta de comprobación | Se implementó `GET /health`. |
| Documentar la ejecución | Se añadieron instrucciones al README. |
| Registrar las tareas del tablero | Confirmado por el autor. |

La publicación en GitHub, los accesos y el tablero fueron confirmados por el autor. Las pruebas locales se centraron en el arranque y las respuestas de la API.

## Estructura inicial

`app/main.py` creaba la aplicación FastAPI. Las rutas se agruparon en `app/api`, donde se añadió `health.py`. Los archivos `__init__.py` definían los paquetes de Python.

Durante S0-03 se comprobaron la importación, el arranque y las respuestas de `/docs` y `/openapi.json`. La ruta `/health` se incorporó después, en S0-04.

## Ruta de comprobación

`GET /health` no recibe parámetros y devuelve HTTP 200 con este cuerpo:

```json
{
  "status": "ok",
  "service": "alt-text",
  "version": "0.1.0"
}
```

Esta ruta comprueba que la API responde. No carga modelos ni revisa servicios externos.

## Pruebas realizadas

Se inició una instancia local en el puerto 54022 con el intérprete de `.venv`:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 54022
```

Se comprobaron el arranque, el JSON de `/health`, el HTML de `/docs` y el esquema de `/openapi.json`. La versión coincidía entre la aplicación y la respuesta. Al terminar, se detuvo el servidor de prueba.

En esa etapa las comprobaciones se hicieron con herramientas de la biblioteca estándar de Python. Todavía no había una suite de pruebas automatizadas ni se había realizado una revisión visual de Swagger UI.

La recepción de imágenes y la generación de descripciones se dejaron para el [Sprint 1](sprint-1.md).
