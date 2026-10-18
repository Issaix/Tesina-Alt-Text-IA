# Guía de desarrollo

Esta guía reúne las convenciones del proyecto y los pasos para comprobar un cambio antes de subirlo.

## Preparar el entorno

Usa Python 3.12 y un entorno virtual. Para instalar las dependencias de la aplicación y las herramientas de desarrollo:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

`requirements.txt` contiene las dependencias directas de la aplicación. `requirements-dev.txt` añade las herramientas de pruebas y formato. `requirements-lock.txt` registra todas las versiones del entorno probado, incluidas las de desarrollo. Para reproducir ese entorno desde cero, instala el archivo lock en un entorno nuevo.

Cuando cambies una dependencia, comprueba primero que el servicio y las pruebas siguen funcionando. Después actualiza el lock desde un entorno dedicado al proyecto:

```powershell
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m pip freeze | Set-Content -Encoding utf8 requirements-lock.txt
```

## Organización del código

| Archivo | Responsabilidad |
|---|---|
| `app/main.py` | Crea la aplicación y registra las rutas. |
| `app/api/describe.py` | Recibe el archivo, coordina el procesamiento y construye la respuesta HTTP. |
| `app/api/health.py` | Comprueba que la API está disponible. |
| `app/images.py` | Valida y normaliza las imágenes sin depender de FastAPI. |
| `app/captioning.py` | Descarga, carga y ejecuta los modelos de descripción y traducción. |
| `scripts/warmup.py` | Prepara los modelos y prueba una inferencia. |
| `scripts/evaluate.py` | Envía imágenes por HTTP y guarda los resultados, incluidos los fallos. |
| `scripts/create_examples.py` | Verifica los hashes y restaura las imágenes ausentes del set de la línea A. |
| `tests/` | Comprueba la API, las imágenes, el servicio de modelos y el evaluador. |

La versión de la aplicación está definida en `app/__init__.py`. Tanto OpenAPI como `/health` usan ese mismo valor.

La función `create_app()` permite construir una aplicación independiente para cada prueba. Las pruebas de API sustituyen el servicio de modelos mediante las dependencias de FastAPI, sin modificar su funcionamiento normal.

## Formato y revisión

Ruff mantiene un formato uniforme y comprueba imports, variables sin uso y otros errores comunes. Su configuración está en `pyproject.toml`. `.editorconfig` define UTF-8, indentación con espacios y finales de línea LF.

Antes de dar por terminado un cambio, ejecuta:

```powershell
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m pip check
```

Para aplicar el formato:

```powershell
.\.venv\Scripts\python.exe -m ruff format .
```

Mantén las funciones pequeñas y con una responsabilidad clara. Añade tipos a las interfaces y comentarios cuando expliquen una decisión que no resulte evidente al leer el código. En los documentos, usa español directo, títulos y listas de Markdown. Evita adornos y no presentes resultados esperados como si fueran pruebas realizadas.

El flujo de GitHub Actions en `.github/workflows/quality.yml` repite estas comprobaciones al subir cambios o abrir un pull request. Usa Python 3.12 en Windows y no descarga modelos. Las acciones están fijadas a commits concretos. La configuración se ha revisado localmente; su ejecución en GitHub se podrá comprobar al publicarla.

## Procesamiento y recursos

La decodificación de la imagen y la inferencia se ejecutan fuera del bucle de la API. Así, una operación lenta no impide atender `/health`.

`decode_image()` devuelve una imagen RGB que debe cerrar quien la use. La ruta de la API la cierra tanto si la inferencia funciona como si falla. Las copias intermedias de Pillow también se cierran. Las imágenes opacas se convierten directamente a RGB para evitar copias innecesarias.

Los modelos se cargan al recibir la primera imagen válida y se conservan durante la vida del proceso. Un bloqueo permite una sola inferencia a la vez y se libera incluso si la carga o generación falla. Evita aumentar el número de workers sin revisar primero el consumo de memoria: cada proceso tendría sus propios modelos.

Los errores de imagen se convierten en respuestas HTTP en la ruta. Los fallos de inferencia se registran en la consola del servidor; al cliente se le devuelve un mensaje breve, sin el detalle interno de la excepción.

## Pruebas con modelos reales

Los tests automatizados comprueban comportamiento, no calidad de las descripciones. Después de cambiar la carga o generación del modelo, inicia el servidor y ejecuta:

```powershell
.\.venv\Scripts\python.exe -m scripts.evaluate --output .cache/evaluation.json
```

Revisa tanto el código HTTP como el contenido de cada descripción. El campo `passed` solo indica que se recibió una respuesta con el formato esperado. Una frase puede cumplir ese formato y aun así ser incorrecta.

El evaluador guarda por separado las respuestas no válidas, los errores de conexión y los archivos ausentes. Continúa con las otras imágenes y termina con código 1 si alguna petición falla. Por defecto escribe en `.cache`, de modo que las pruebas habituales no reemplazan la evidencia del sprint.

La [guía de evaluación](evaluacion.md) explica cómo incorporar revisiones con `--input` y `--reviews`. El manifiesto vigente contiene exactamente 20 imágenes: 10 fotografías y 10 ilustraciones generales. El evaluador rechaza entradas cuyo tipo sea una gráfica o un diagrama.

Para verificar los hashes o restaurar archivos ausentes desde sus fuentes:

```powershell
.\.venv\Scripts\python.exe -m scripts.create_examples
```

El comando conserva los archivos existentes y falla si su hash no coincide. Solo necesita conexión cuando hay que recuperar una imagen. Ya no existen generadores de láminas con datos.

## Modelos y licencias

BLIP base se distribuye con licencia BSD-3-Clause y OPUS-MT con Apache-2.0. Las revisiones concretas están en `app/captioning.py` y en el informe de evaluación.

Los archivos se descargan desde Hugging Face y se cargan desde rutas locales. La aplicación no solicita conversiones remotas ni envía las imágenes a un servicio de inferencia. El entorno virtual, los pesos y los resultados de trabajo en `.cache` están excluidos de Git.
