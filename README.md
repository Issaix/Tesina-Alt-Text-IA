# Tesina Alt-Text IA

## Descripción

Microservicio REST orientado a generar descripciones en español de imágenes educativas mediante un modelo preentrenado de inteligencia artificial, para apoyar la accesibilidad de estudiantes con discapacidad visual.

Proyecto de tesina de Ingeniería en Computación Inteligente de la Universidad Autónoma de Aguascalientes. Actualmente permite comprobar que la aplicación responde mediante `GET /health`. La recepción de imágenes y la generación de descripciones están pendientes.

## Instrucciones de ejecución

Requisito: Python 3.13. Ejecutar los comandos desde la raíz del proyecto en PowerShell.

**Preparación inicial:** crear el entorno virtual si no existe e instalar las dependencias.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

**Iniciar el servicio:** activar el entorno y ejecutar Uvicorn.

```powershell
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload
```

Si PowerShell bloquea la activación, iniciar directamente con el intérprete del entorno:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

**Comprobar la ejecución:** abrir [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health). La respuesta esperada es HTTP 200 con este JSON:

```json
{"status": "ok", "service": "alt-text", "version": "0.1.0"}
```

Esta consulta comprueba que la aplicación responde; no verifica la disponibilidad de un modelo de IA. La documentación interactiva está en [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

**Detener el servicio:** presionar `Ctrl + C` en la terminal donde está ejecutándose.
