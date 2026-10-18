# Tesina Alt-Text IA

Microservicio REST que recibe imágenes educativas y genera borradores de texto alternativo en español. Forma parte de una tesina de Ingeniería en Computación Inteligente de la Universidad Autónoma de Aguascalientes.

La línea A se centra en fotografías e ilustraciones de propósito general. Las gráficas y los diagramas se utilizan en pruebas complementarias para estudiar limitaciones. El servicio usa BLIP base para describir la imagen y OPUS-MT para traducir el resultado. Las descripciones necesitan revisión antes de usarse en materiales educativos.

## Preparar el entorno

Se ha probado en Windows con Python 3.12 de 64 bits y procesamiento en CPU. No requiere GPU ni clave de API. La primera instalación necesita conexión a PyPI y Hugging Face; los modelos ocupan aproximadamente 1,3 GB.

Desde la raíz del proyecto, ejecutar en PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m scripts.warmup
```

Si el entorno ya existe, omitir el primer comando. Si `py` no está disponible, usar la ruta de Python 3.12. Los comandos utilizan directamente el entorno virtual; no hace falta activarlo.

`scripts.warmup` descarga los modelos en `.cache/models` y comprueba que pueden generar una descripción. Las siguientes ejecuciones reutilizan esos archivos. Las imágenes se procesan en el equipo local.

## Iniciar el servidor

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Mantener la terminal abierta. Para detener el servidor, pulsar `Ctrl + C`. Durante el desarrollo se puede añadir `--reload` al comando.

- Documentación interactiva: <http://127.0.0.1:8000/docs>.
- Estado del servicio: <http://127.0.0.1:8000/health>.
- Esquema OpenAPI: <http://127.0.0.1:8000/openapi.json>.

`GET /health` comprueba que la API responde, sin verificar la disponibilidad de los modelos. Devuelve HTTP 200:

```json
{"status": "ok", "service": "alt-text", "version": "0.1.0"}
```

## Enviar una imagen

En `/docs`, abrir **POST /describe**, pulsar **Try it out**, seleccionar un archivo en **image** y pulsar **Execute**.

También se puede enviar una imagen desde otra terminal:

```powershell
curl.exe --fail-with-body -X POST "http://127.0.0.1:8000/describe" -F "image=@examples/educational/gato.png;type=image/png"
```

Una respuesta correcta devuelve HTTP 200 con este formato:

```json
{"description": "un primer plano de un gato con ojos verdes"}
```

Se aceptan JPG, JPEG y PNG estáticos de hasta 10 MiB y 20 megapíxeles. El archivo se envía en el campo `image`, con MIME `image/jpeg` o `image/png`. También se acepta un MIME ausente o `application/octet-stream`; siempre se valida el contenido. No se reciben rutas ni URL de imágenes.

La primera petición puede tardar más por la carga de los modelos. Se procesa una imagen a la vez por proceso; usar un solo proceso para evitar cargar varias copias de los modelos. Si aparece HTTP 503, consultar la terminal del servidor. Si faltan pesos, repetir `scripts.warmup` con conexión.

Para ejecutar la evaluación de imágenes y las comprobaciones de desarrollo, consultar la [guía de evaluación](docs/evaluacion.md) y la [guía de desarrollo](docs/desarrollo.md).
