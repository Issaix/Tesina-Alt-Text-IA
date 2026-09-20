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
