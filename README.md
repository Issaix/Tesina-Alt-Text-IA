# Tesina Alt-Text IA

Microservicio REST para generar descripciones textuales en español de imágenes educativas mediante inteligencia artificial, orientado a apoyar la accesibilidad de estudiantes con discapacidad visual.

Proyecto de tesina de Ingeniería en Computación Inteligente de la Universidad Autónoma de Aguascalientes.

## Objetivo

Desarrollar un microservicio que reciba imágenes educativas y genere descripciones textuales mediante un modelo preentrenado de visión y lenguaje, exponiendo su funcionalidad a través de una API REST integrable con una arquitectura de remediación de accesibilidad.

## Alcance

El proyecto contempla:

- Procesamiento de imágenes estáticas: fotografías, ilustraciones y diagramas educativos.
- Generación de descripciones en español.
- Uso de un modelo preentrenado.
- Implementación y documentación de una API REST.
- Contenerización del microservicio.
- Evaluación de la pertinencia de las descripciones generadas.

Quedan fuera del alcance el procesamiento de video, el entrenamiento de modelos desde cero, la interfaz de usuario final y la orquestación entre servicios.

La generación automática de una descripción no garantiza por sí sola la conformidad con WCAG; su pertinencia deberá evaluarse considerando el contenido y propósito educativo de la imagen.

## Estado actual

Sprint 0: puesta a punto.

Se ha preparado el entorno de desarrollo local y registrado las dependencias en `requirements.txt`.

La estructura base de la aplicación está implementada (S0-03), con una instancia de FastAPI y documentación automática disponible en `/docs`. Todavía no existen endpoints propios.

La siguiente tarea es implementar el endpoint `GET /health` en la S0-04.

La recepción de imágenes y la integración del modelo de descripción corresponden al sprint 1.

## Tecnologías

- Python.
- FastAPI: desarrollo de la API REST.
- Uvicorn: ejecución del servidor.
- Git y GitHub: control de versiones.
- VS Code: entorno de edición.

## Entorno de desarrollo utilizado

- Sistema operativo: Windows.
- Terminal: PowerShell.
- Python: 3.13.14.
- Git: 2.52.0.windows.1.

Las versiones de las dependencias de Python se encuentran en `requirements.txt`.

## Preparación del entorno

### 1. Clonar el repositorio

Sustituir `TU_USUARIO` por el propietario del repositorio:

```powershell
git clone https://github.com/TU_USUARIO/Tesina-Alt-Text-IA.git
cd Tesina-Alt-Text-IA
```

Si el repositorio es privado, se necesita una cuenta de GitHub con acceso.

### 2. Crear el entorno virtual

```powershell
python -m venv .venv
```

### 3. Activar el entorno virtual

En PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la ejecución del script, abrir una terminal Command Prompt y ejecutar:

```bat
.venv\Scripts\activate.bat
```

### 4. Instalar las dependencias

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 5. Seleccionar el intérprete en VS Code

1. Presionar `Ctrl + Shift + P`.
2. Ejecutar `Python: Select Interpreter`.
3. Seleccionar el intérprete de `.venv`.

Su ubicación dentro del proyecto es:

```text
.venv\Scripts\python.exe
```

## Verificación del entorno

Comprobar que Python pertenece al entorno virtual:

```powershell
python -c "import sys; print(sys.executable)"
```

La ruta debe apuntar a `.venv\Scripts\python.exe` dentro del proyecto.

Comprobar la instalación de FastAPI y Uvicorn:

```powershell
python -c "import fastapi, uvicorn; print('FastAPI:', fastapi.__version__); print('Uvicorn:', uvicorn.__version__)"
```

Comprobar la compatibilidad de las dependencias instaladas:

```powershell
python -m pip check
```

Resultado esperado:

```text
No broken requirements found.
```

## Archivos actuales

| Archivo | Propósito |
|---|---|
| `README.md` | Descripción del proyecto e instrucciones de preparación |
| `requirements.txt` | Dependencias de Python con sus versiones |
| `.gitignore` | Exclusión de archivos locales del control de versiones |
| `app/__init__.py` | Define el paquete de la aplicación |
| `app/main.py` | Inicializa FastAPI con el título, la descripción y la versión del servicio |
| `app/api/__init__.py` | Define el paquete para las futuras rutas de la API |
| `app/api/health.py` | Archivo reservado para `GET /health` en la S0-04; sin endpoint implementado |
| `docs/sprint-0.md` | Objetivo, decisiones y resultados de las verificaciones de la S0-03 |

La carpeta `.venv` se genera localmente y no se incluye en el repositorio.

## Ejecución del microservicio

Desde la raíz del proyecto, con el entorno virtual activo:

```powershell
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload
```

La documentación automática está disponible en [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). La opción `--reload` reinicia el servidor al detectar cambios en el código durante el desarrollo.

`app/main.py` crea la aplicación principal; `app/api/` alojará las futuras rutas por separado. Todavía no hay endpoints propios registrados, por lo que `/docs` indica que no hay operaciones definidas. Es normal que `/` y `/health` respondan HTTP 404 en esta etapa. `GET /health` se implementará en la S0-04.

Para detener el servidor, presionar `Ctrl + C` en la terminal donde está ejecutándose.

## Seguimiento del trabajo

Las tareas y los criterios de aceptación se registran en el proyecto de GitHub `Tesina-Alt-Text-IA`.

Una tarea se considera terminada cuando:

- Su implementación está en el repositorio.
- Se ejecuta sin errores.
- Incluye instrucciones mínimas de uso.
- Cumple sus criterios de aceptación.

## Autor

Issai Brandon Aparicio Gutiérrez  
Ingeniería en Computación Inteligente  
Universidad Autónoma de Aguascalientes
