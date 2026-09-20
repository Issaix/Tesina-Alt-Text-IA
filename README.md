# Tesina Alt-Text IA

## Descripción

Microservicio REST orientado a generar descripciones textuales en español de imágenes educativas mediante un modelo preentrenado de inteligencia artificial, para apoyar la accesibilidad de estudiantes con discapacidad visual.

Proyecto de tesina de Ingeniería en Computación Inteligente de la Universidad Autónoma de Aguascalientes. Actualmente dispone de un endpoint `GET /health` para comprobar que la aplicación responde; la recepción de imágenes y la generación de descripciones aún no están implementadas.

## Instrucciones de ejecución

Desde la raíz del proyecto, en PowerShell, con Python 3.13 instalado:

Si todavía no existe el entorno virtual, crearlo:

```powershell
python -m venv .venv
```

Activar el entorno e instalar las dependencias si aún no están instaladas:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Iniciar el servidor de desarrollo:

```powershell
python -m uvicorn app.main:app --reload
```

Si PowerShell bloquea la activación, utilizar directamente el intérprete del entorno virtual:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Con el servidor en ejecución:

- Abrir [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health) para comprobar que responde. Debe devolver HTTP 200 y `{"status":"ok","service":"alt-text","version":"0.1.0"}`. Esto no verifica la disponibilidad de un modelo de IA.
- Consultar la documentación interactiva en [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

Para detener el servidor, presionar `Ctrl + C` en la terminal donde está ejecutándose.
