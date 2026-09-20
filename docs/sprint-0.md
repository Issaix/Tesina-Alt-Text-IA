# Sprint 0: puesta a punto

## Estado de los requisitos

| Requisito | Estado y evidencia |
|---|---|
| Crear el repositorio en GitHub y configurar accesos | Realizado y confirmado por el autor |
| Configurar el entorno local | Entorno `.venv` utilizado correctamente en las comprobaciones de S0-03 y S0-04; dependencias registradas en `requirements.txt` |
| Definir la estructura base | Implementada en S0-03 |
| Implementar un endpoint REST mínimo | `GET /health` implementado y comprobado en S0-04 |
| Elaborar un README con descripción y ejecución | Disponible en [README.md](../README.md) |
| Registrar las primeras tareas en el tablero | Realizado y confirmado por el autor |

Los requisitos listados cuentan con comprobaciones locales o confirmación del autor. El autor realizó la publicación en GitHub, la configuración de accesos y el registro de tareas en el tablero; estas acciones no se verificaron de forma independiente durante la revisión local.

## S0-03: estructura base

**Objetivo:** preparar una aplicación FastAPI que pueda arrancar y ofrecer documentación automática.

| Archivo | Función actual |
|---|---|
| `app/__init__.py` | Define el paquete de la aplicación |
| `app/main.py` | Inicializa FastAPI y registra las rutas |
| `app/api/__init__.py` | Define el paquete de rutas |
| `app/api/health.py` | Contiene el endpoint de salud incorporado en S0-04 |
| `docs/sprint-0.md` | Resume las tareas y sus verificaciones |

Se separó la aplicación principal de las rutas para mantener el código sencillo y organizado. Los metadatos son: título `Tesina Alt-Text IA`, versión `0.1.0` y descripción «Microservicio para generar descripciones textuales en español de imágenes educativas.»

En S0-03 se verificaron la importación, el arranque, `/docs` y `/openapi.json` con HTTP 200. En esa etapa no había rutas propias: `/` y `/health` devolvían 404. El archivo de salud quedó reservado y se implementó después, en S0-04.

## S0-04: endpoint de salud

**Objetivo:** comprobar que la aplicación responde solicitudes. No verifica modelos de IA, procesamiento de imágenes ni servicios externos.

**Archivos modificados:** `app/api/health.py`, `app/main.py`, `README.md` y este documento.

**Contrato:** `GET /health`, sin parámetros ni cuerpo de petición. Devuelve HTTP 200, con tipo `application/json`:

```json
{
  "status": "ok",
  "service": "alt-text",
  "version": "0.1.0"
}
```

`app/main.py` registra el router mediante `app.include_router(router)`, sin prefijo. FastAPI dirige la petición a `health_check` y convierte el diccionario devuelto en JSON. La documentación agrupa la operación bajo `Health`, con resumen y descripción en español.

### Verificaciones realizadas

Se utilizó el intérprete de `.venv`. Para S0-04 se seleccionó el puerto libre **54022** y se inició una instancia propia con:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 54022
```

Las solicitudes se comprobaron con `urllib.request.urlopen` y `json.load` de la biblioteca estándar de Python, comparando el cuerpo completo y el esquema OpenAPI.

| Comprobación | Resultado |
|---|---|
| Importación y arranque con `--reload` | Correctos, sin errores de arranque |
| `GET /health` | HTTP 200, `application/json` y JSON exacto |
| `GET /docs` | HTTP 200; HTML de Swagger UI presente |
| `GET /openapi.json` | HTTP 200; incluye GET `/health`, etiqueta `Health` y respuesta 200 |
| Contrato OpenAPI | Sin parámetros ni cuerpo de petición; única ruta propia: `/health` |
| Versión | `0.1.0` en la aplicación y en la respuesta |
| Cierre | Servidor propio y proceso de recarga detenidos con `Ctrl + C` |

Estos resultados corresponden a las comprobaciones de implementación registradas en esta conversación; no se repitieron al simplificar la documentación. No se instalaron dependencias ni se creó una suite de pruebas. No se detuvieron servidores ajenos.

La revisión visual de Swagger UI no se realizó. Puede comprobarse manualmente en `/docs` mediante **GET /health → Try it out → Execute**.

## Criterios de terminado

| Criterio | Verificación |
|---|---|
| El código está en el repositorio | Archivos presentes en el proyecto local; publicación en GitHub confirmada por el autor |
| Se ejecuta sin errores | Arranque y comprobaciones HTTP satisfactorios en S0-03 y S0-04 |
| Incluye una nota mínima de uso | El README explica preparación, inicio, consulta y cierre |
| Cumple el criterio de la tarea | S0-03 y S0-04 verificadas localmente; GitHub, accesos y tablero confirmados por el autor; README revisado |

La recepción de imágenes y la generación de descripciones quedan pendientes para el sprint 1. Las instrucciones de ejecución habituales están en el [README](../README.md).
