# Sprint 0: puesta a punto

## S0-03: estructura base del proyecto

### Objetivo

Preparar la estructura mínima del microservicio Tesina Alt-Text IA, inicializar FastAPI y comprobar que el servidor arranca y ofrece documentación automática, sin implementar todavía endpoints propios.

### Estructura y función de los archivos

```text
app/
    __init__.py
    main.py
    api/
        __init__.py
        health.py
docs/
    sprint-0.md
```

| Archivo | Función |
|---|---|
| `app/__init__.py` | Define el paquete de la aplicación; vacío por ahora |
| `app/main.py` | Crea la instancia `app` de FastAPI con los metadatos del microservicio |
| `app/api/__init__.py` | Define el paquete para las futuras rutas; vacío por ahora |
| `app/api/health.py` | Reserva el archivo para la S0-04, sin implementar ni registrar rutas |
| `docs/sprint-0.md` | Registra el objetivo, las decisiones y las comprobaciones del sprint |

Se actualizó el README para reflejar esta estructura y explicar la ejecución del servidor, conservando la descripción, los objetivos, el alcance, el autor y las instrucciones de preparación del entorno. No se modificaron las dependencias.

### Decisión de organización

La aplicación principal se inicializa en `app/main.py` y las futuras rutas se alojarán en `app/api/`. Esta separación permite organizar los endpoints sin concentrar su implementación en el punto de entrada. En esta tarea no se importa ni se registra ningún router.

Los metadatos configurados son:

- Título: `Tesina Alt-Text IA`.
- Descripción: `Microservicio para generar descripciones textuales en español de imágenes educativas.`
- Versión: `0.1.0`.

### Ejecución

Desde la raíz del proyecto, activar el entorno virtual en PowerShell e iniciar el servidor:

```powershell
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload
```

Documentación automática: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

Para detener el servidor, presionar `Ctrl + C` en su terminal.

Todavía no existen endpoints propios: la documentación no tiene operaciones definidas y las respuestas HTTP 404 de `/` y `/health` son esperadas.

### Verificaciones realizadas

Comprobaciones ejecutadas el 20 de septiembre de 2026 desde la raíz del proyecto, usando `.venv\Scripts\python.exe`. El primer intento de importación fue bloqueado por una restricción de acceso al ejecutable base de Python; se repitió con permisos ampliados y se completó correctamente. No se instalaron dependencias ni se creó una suite de pruebas.

Para verificar el arranque se ejecutó directamente el intérprete del entorno virtual, equivalente al comando anterior con el entorno activo:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

| Comprobación | Resultado real |
|---|---|
| Importar `app` desde `app.main` | Correcto usando el intérprete de `.venv` |
| Metadatos de la instancia FastAPI | Título, descripción y versión coinciden con los valores solicitados |
| Arranque de Uvicorn con `--reload` | Correcto; registro `Application startup complete.` sin errores de arranque |
| `GET /docs` | HTTP 200; la respuesta HTML contiene Swagger UI |
| `GET /openapi.json` | HTTP 200; título, descripción y versión comprobados en la respuesta JSON |
| Ausencia de endpoints propios | Confirmada: `paths` es `{}` tanto en el esquema de la instancia como en la respuesta HTTP |
| `GET /` | HTTP 404, esperado en esta etapa |
| `GET /health` | HTTP 404, esperado en esta etapa |
| Detención del servidor | Se envió `Ctrl + C`; los registros confirmaron el cierre de la aplicación, del proceso servidor y del proceso de recarga |

La comprobación de `/docs` se realizó por HTTP; no se inspeccionó visualmente en un navegador.

### Pendiente

Implementar y registrar `GET /health` en la S0-04. La recepción de imágenes y la integración de modelos de inteligencia artificial quedan fuera de esta tarea.

## S0-04: endpoint GET /health

### Objetivo

Permitir comprobar que la aplicación está en ejecución y responde solicitudes mediante un endpoint mínimo. No comprueba la disponibilidad de modelos de IA, la capacidad de describir imágenes ni el funcionamiento de dependencias externas.

### Archivos modificados

- `app/api/health.py`: implementa `router` con `APIRouter` y la función `health_check() -> dict[str, str]`, sin parámetros.
- `app/main.py`: importa y registra el router, conservando los metadatos y la versión `0.1.0`.
- `README.md`: actualiza el estado y explica cómo consultar el endpoint desde navegador, PowerShell y Swagger UI.
- `docs/sprint-0.md`: agrega este registro y conserva la sección S0-03 como evidencia histórica del estado anterior.

### Contrato y registro del router

- Método y ruta: `GET /health`, sin parámetros ni cuerpo de petición.
- Código declarado explícitamente: HTTP 200.
- Tipo de contenido: `application/json`.
- Etiqueta OpenAPI: `Health`, con resumen y descripción en español.
- Respuesta exacta:

```json
{
  "status": "ok",
  "service": "alt-text",
  "version": "0.1.0"
}
```

`app/main.py` importa `router` de `app.api.health` y lo registra mediante `app.include_router(router)`, sin prefijo. Uvicorn entrega la petición a la aplicación FastAPI; la ruta registrada selecciona `health_check`, que devuelve el diccionario y FastAPI lo serializa como JSON.

### Comandos utilizados y verificaciones

Las comprobaciones se ejecutaron con el intérprete de `.venv`, desde la raíz del proyecto y con permisos ampliados para acceder al ejecutable base de Python. No se instalaron dependencias ni se agregó una suite de pruebas.

Se comprobó la importación y se seleccionó un puerto libre mediante un socket local:

```powershell
.\.venv\Scripts\python.exe -c "import socket, sys; from app.main import app; print('Interpreter:', sys.executable); print('Import: OK'); assert app.version == '0.1.0'; s = socket.socket(); s.bind(('127.0.0.1', 0)); print('Free port:', s.getsockname()[1]); s.close()"
```

El puerto obtenido fue **54022**. Se inició una instancia propia y su arranque confirmó que pudo utilizarlo:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 54022
```

En otra terminal se ejecutó esta comprobación HTTP directa con la biblioteca estándar de Python:

```powershell
@'
import json
from urllib.request import urlopen

base = "http://127.0.0.1:54022"
expected = {"status": "ok", "service": "alt-text", "version": "0.1.0"}
with urlopen(base + "/health", timeout=10) as response:
    assert response.status == 200
    assert response.headers.get_content_type() == "application/json"
    body = json.load(response)
    assert body == expected
    print("GET /health: HTTP 200; application/json;", body)
with urlopen(base + "/docs", timeout=10) as response:
    assert response.status == 200
    assert "swagger-ui" in response.read().decode("utf-8")
    print("GET /docs: HTTP 200; Swagger UI HTML presente")
with urlopen(base + "/openapi.json", timeout=10) as response:
    assert response.status == 200
    schema = json.load(response)
    assert schema["info"]["title"] == "Tesina Alt-Text IA"
    assert schema["info"]["version"] == expected["version"]
    assert set(schema["paths"]) == {"/health"}
    operation = schema["paths"]["/health"]["get"]
    assert operation["tags"] == ["Health"]
    assert "200" in operation["responses"]
    assert operation["summary"] and operation["description"]
    assert not operation.get("parameters")
    assert "requestBody" not in operation
    print("GET /openapi.json: HTTP 200; GET /health, Health y respuesta 200; sin parametros ni cuerpo; unica ruta propia")
'@ | .\.venv\Scripts\python.exe -
```

| Comprobación | Resultado real |
|---|---|
| Importar la aplicación con `.venv` | Correcto |
| Arranque de Uvicorn con `--reload` en el puerto 54022 | Sin errores; `Application startup complete.` |
| `GET /health` | HTTP 200 |
| Tipo de contenido de `/health` | `application/json` |
| Cuerpo de `/health` | Coincide exactamente con los tres campos y valores del contrato |
| `GET /docs` | HTTP 200; HTML de Swagger UI presente |
| `GET /openapi.json` | HTTP 200; incluye `/health`, método GET y etiqueta `Health` |
| Contrato OpenAPI | Respuesta 200, resumen y descripción presentes; sin parámetros ni cuerpo de petición |
| Rutas propias y metadatos | Única ruta propia: `/health`; título conservado y versión `0.1.0` coincidente con la respuesta |
| Detención de la instancia propia | Se envió `Ctrl + C`; los registros confirmaron el cierre de la aplicación, del servidor y del proceso de recarga |

Solo se detuvo la instancia iniciada para esta verificación; no se detuvieron servidores ajenos. El puerto 54022 se usó únicamente para las comprobaciones. El comando habitual de desarrollo sigue siendo:

```powershell
python -m uvicorn app.main:app --reload
```

Con el entorno virtual activo, ese comando permite consultar [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health) y [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### Limitaciones y revisión manual

No se inspeccionó visualmente Swagger UI ni se ejecutó su botón “Execute”; las comprobaciones realizadas fueron HTTP y de esquema OpenAPI. Para revisar manualmente la interfaz, iniciar el servidor, abrir `/docs`, expandir `GET /health` bajo `Health`, pulsar “Try it out” y “Execute”, y comprobar el código 200 y el JSON anterior.

La recepción de imágenes y la generación de descripciones siguen pendientes para el sprint 1. Este registro corresponde únicamente a la S0-04 y no declara completado todo el sprint 0.
