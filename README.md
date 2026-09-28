# Tesina Alt-Text IA

Este servicio recibe una imagen educativa y genera una descripción en español. La idea es ayudar a preparar textos alternativos que puedan leer los lectores de pantalla.

Es parte de una tesina de Ingeniería en Computación Inteligente de la Universidad Autónoma de Aguascalientes. En esta primera versión, el servicio ya recibe imágenes, las procesa y devuelve el resultado en JSON. La calidad del texto todavía necesita revisión: el modelo puede omitir información o inventar detalles.

## Requisitos

El proyecto se ha probado en Windows con Python 3.12 de 64 bits y procesamiento en CPU. No necesitas una GPU ni una clave de API.

La primera instalación necesita conexión a PyPI y Hugging Face. Los pesos de los modelos ocupan cerca de 1.3 GB. Como referencia, conviene disponer de 8 GB de RAM y 5 GB de espacio libre para el entorno y los modelos; no son requisitos mínimos medidos. Las imágenes se procesan en tu equipo.

## Instalación

Abre PowerShell en la carpeta del proyecto y ejecuta:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Si ya tienes el entorno creado, basta con el segundo comando. Si tu equipo no reconoce `py`, utiliza la ruta de tu ejecutable de Python 3.12. Los ejemplos usan directamente el intérprete del entorno, así que no hace falta activarlo.

En Linux o macOS, las rutas equivalentes son `python3.12` y `.venv/bin/python`. Estas plataformas todavía no se han probado.

## Preparar los modelos

Antes de iniciar el servidor, ejecuta:

```powershell
.\.venv\Scripts\python.exe -m scripts.warmup
```

Este comando descarga los modelos en `.cache/models` y comprueba que pueden generar una descripción. La primera vez puede tardar varios minutos. Las siguientes ejecuciones reutilizan los archivos descargados.

El servicio usa [BLIP base](https://huggingface.co/Salesforce/blip-image-captioning-base) para describir la imagen en inglés y [OPUS-MT](https://huggingface.co/Helsinki-NLP/opus-mt-en-es) para traducir el texto al español. Las versiones de ambos modelos están fijadas en el código.

## Iniciar el servidor

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Deja la terminal abierta mientras haces las pruebas. Para detener el servidor, presiona `Ctrl+C`.

Puedes abrir estas direcciones:

- [Documentación interactiva](http://127.0.0.1:8000/docs), para enviar imágenes desde el navegador.
- [Estado del servicio](http://127.0.0.1:8000/health), para comprobar que la API responde.
- [Esquema OpenAPI](http://127.0.0.1:8000/openapi.json), para consultar sus operaciones y respuestas.

La primera petición tarda más porque carga los modelos en memoria. Después se reutilizan. En esta versión se procesa una imagen a la vez por proceso; usa un solo proceso para evitar cargar varias copias de los modelos.

## Probar con una imagen

En la documentación interactiva, abre **POST /describe**, pulsa **Try it out**, selecciona un archivo en **image** y pulsa **Execute**.

También puedes enviar una imagen desde otra terminal:

```powershell
curl.exe --fail-with-body -X POST "http://127.0.0.1:8000/describe" -F "image=@examples/educational/triangulo.png;type=image/png"
```

En PowerShell conviene escribir `curl.exe` para evitar el alias de algunas versiones. Cambia la ruta del ejemplo para probar una imagen propia.

Esta es una respuesta real de la imagen del triángulo incluida en el proyecto:

```json
{
  "description": "un triángulo se muestra en el lado derecho de un triángulo derecho"
}
```

La respuesta permite comprobar que el flujo funciona, aunque la descripción todavía es imprecisa. Antes de usar el texto, compáralo con la imagen y corrige lo que haga falta.

### Formatos y límites

El endpoint recibe un archivo en el campo `image` de una petición `multipart/form-data`.

- Acepta JPG, JPEG y PNG estáticos, incluidas extensiones en mayúsculas.
- El archivo puede ocupar hasta 10 MiB y tener hasta 20 megapíxeles.
- Comprueba el contenido real, la extensión y el tipo MIME.
- Corrige la orientación EXIF y coloca un fondo blanco detrás de las zonas transparentes.

El tipo MIME debe ser `image/jpeg` o `image/png`, según el archivo. También se acepta `application/octet-stream` o un MIME ausente, porque siempre se comprueban los bytes. No se reciben rutas, URL ni imágenes en Base64.

El tamaño se comprueba después de recibir el formulario multipart. Por tanto, este límite no restringe el tamaño total de una petición HTTP. Las imágenes no se guardan de forma permanente; durante la recepción pueden usarse archivos temporales que se cierran al terminar.

### Respuestas de la API

| Código | Qué significa |
|---|---|
| 200 | Se generó una descripción. El JSON contiene `description`. |
| 400 | El archivo está vacío, dañado o no puede leerse como imagen. |
| 413 | La imagen supera el tamaño o la resolución permitidos. |
| 415 | El formato no se acepta o no coincide con la extensión o el MIME. |
| 422 | Falta el archivo en `image` o se envió otro tipo de dato. |
| 503 | El modelo está ocupado o no pudo procesar la imagen. |

Los errores usan el campo `detail`. En el caso de 422, FastAPI devuelve una lista con los errores de validación. Si el modelo está ocupado, la respuesta incluye `Retry-After: 5`; espera unos segundos y vuelve a intentar.

`GET /health` responde con `{"status":"ok","service":"alt-text","version":"0.1.0"}`. Indica que la API está disponible, pero no comprueba los modelos.

## Ejecutar las pruebas

Instala las herramientas de desarrollo:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

Con el servidor encendido, prueba las cuatro imágenes educativas incluidas:

```powershell
.\.venv\Scripts\python.exe -m scripts.evaluate
```

El resultado se guarda en `.cache/evaluation.json`, sin modificar el informe original del sprint. El evaluador conserva también las peticiones fallidas y termina con un código distinto de cero si alguna no funciona. Puedes cambiar el destino con `--output` o el servidor con `--base-url`.

Para revisar el código y ejecutar las pruebas automatizadas, no hace falta iniciar el servidor:

```powershell
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
.\.venv\Scripts\python.exe -m pytest -q
```

Las pruebas automatizadas usan un sustituto del modelo para comprobar la API sin descargar pesos. La evaluación de las cuatro imágenes sí ejecuta los modelos reales. Los detalles de mantenimiento están en la [guía de desarrollo](docs/desarrollo.md).

## Si algo falla

Si aparece un error 503, revisa la terminal del servidor. Si está ocupado, espera a que termine la petición anterior. Si falla la carga, comprueba la conexión y el espacio disponible, y vuelve a ejecutar `scripts.warmup`.

Puedes elegir otra carpeta para los pesos con `MODEL_CACHE_DIR`. Después de descargarlos por completo, puedes trabajar sin conexión:

```powershell
$env:HF_HUB_OFFLINE='1'
```

Si falta algún archivo en caché, retira esa variable con `Remove-Item Env:HF_HUB_OFFLINE` y repite la preparación con conexión. Al cambiar de carpeta de caché, también debes preparar los modelos en esa ubicación.

## Resultados y siguientes pasos

Las cuatro imágenes del Sprint 1 se procesaron correctamente por HTTP. Eso no significa que sus descripciones sean correctas: el modelo llegó a describir un gráfico de libros leídos como si tratara sobre personas que utilizan Internet.

Puedes consultar las respuestas y observaciones en el [informe del Sprint 1](docs/sprint-1.md). El [registro del Sprint 0](docs/sprint-0.md) conserva la preparación inicial del proyecto.

Este servicio produce borradores de texto alternativo. El [criterio WCAG 1.1.1](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html) exige que la alternativa cumpla el propósito del contenido original. Todavía falta mejorar la interpretación de gráficos y etiquetas, incorporar el contexto de la lección y evaluar los textos con usuarios de lectores de pantalla. La contenerización y la integración con el orquestador quedan para las siguientes etapas.
