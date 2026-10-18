# Evaluación de las descripciones

La evaluación utiliza dos conjuntos separados:

| Conjunto | Imágenes | Finalidad |
|---|---|---|
| Principal: `examples/educational` | 10 fotografías y 10 ilustraciones | Evaluar las imágenes generales de la línea A. |
| Complementario: `examples/limitations` | 11 diagramas y 7 gráficas | Estudiar errores en datos y relaciones. |

Los resultados complementarios no se suman a los del conjunto principal. La [revisión de objetivos](alineacion-proyecto.md) explica su relación con el alcance del proyecto.

## Ejecutar la evaluación

Preparar los modelos e iniciar el servidor como indica el [README](../README.md). En otra terminal, desde la raíz del proyecto:

```powershell
.\.venv\Scripts\python.exe -m scripts.evaluate --output .cache/principal.json
.\.venv\Scripts\python.exe -m scripts.evaluate --manifest examples/limitations/manifest.json --output .cache/limitations.json
```

Si el servidor utiliza otro puerto, añadir `--base-url http://127.0.0.1:PUERTO` con el número correspondiente.

Cada comando envía las imágenes a `POST /describe` y guarda un JSON y un Markdown con la respuesta, código HTTP, tiempo, hash y referencia. Los fallos se registran sin interrumpir las demás peticiones. El código de salida es 1 si alguna petición falla.

`passed` solo indica que la respuesta cumple el contrato HTTP. La calidad queda pendiente hasta comparar el texto con la imagen y aplicar la rúbrica.

Para comprobar previamente los archivos:

```powershell
.\.venv\Scripts\python.exe -m scripts.create_examples
.\.venv\Scripts\python.exe -m scripts.create_examples --manifest examples/limitations/manifest.json
```

Los archivos principales ausentes se descargan desde las fuentes del manifiesto. Las láminas complementarias ausentes deben recuperarse del repositorio. Los archivos cuyo hash no coincide se señalan como error y no se reemplazan.

## Aplicar la rúbrica

Abrir cada imagen y comparar la salida con `context`, `reference` y `required_content`, siguiendo la [rúbrica](rubrica-alt-text.md). Se aceptan sinónimos y paráfrasis que mantengan el significado.

Los archivos [principal](evaluacion-principal-revisiones.json) y [complementario](evaluacion-limitaciones-revisiones.json) sirven como plantilla para registrar puntuaciones. Cada entrada contiene:

- Archivo, hash de la imagen y hash de la descripción exacta.
- Cinco puntuaciones de 0 a 2: identificación, contexto, información esencial, fidelidad y claridad.
- Error crítico, justificación y corrección propuesta.
- Fecha y metadatos de trazabilidad, conservados en JSON.

Para aplicar las revisiones sin repetir las peticiones:

```powershell
.\.venv\Scripts\python.exe -m scripts.evaluate --input .cache/principal.json --reviews docs/evaluacion-principal-revisiones.json --output .cache/principal-revisado.json
.\.venv\Scripts\python.exe -m scripts.evaluate --input .cache/limitations.json --reviews docs/evaluacion-limitaciones-revisiones.json --output .cache/limitations-revisado.json
```

Las revisiones guardadas solo son válidas si coinciden la imagen, la salida y los criterios. Si cambia una descripción, se debe valorar de nuevo. El evaluador rechaza hashes distintos, revisiones duplicadas y puntuaciones inválidas. No asigna puntuaciones automáticamente a partir de la similitud entre textos.

## Resultados registrados

| Conjunto | HTTP correcto | Requieren revisión | No aptas | Errores críticos | Media / 10 |
|---|---:|---:|---:|---:|---:|
| Principal | 20/20 | 20 | 0 | 0 | 7,95 |
| Complementario | 18/18 | 0 | 18 | 10 | 2,83 |

No hubo salidas clasificadas como aptas. En el principal faltó contenido obligatorio; en el complementario hubo omisiones y errores de tema, unidades o relaciones. Las puntuaciones son preliminares y están pendientes de validación.

- [Informe principal](evaluacion-principal.md): respuestas, referencias y valoraciones de las 20 imágenes.
- [Informe complementario](evaluacion-limitaciones.md): resultados de los 18 diagramas y gráficas.
- [Limitaciones del modelo](limitaciones-modelo.md): análisis de los errores observados.

## Procedencia y alcance

Las respuestas y puntuaciones corresponden al **17 de octubre de 2026**, con Windows, Python 3.12.14 y CPU. Los JSON registran las revisiones de los modelos, bibliotecas, tiempos y hashes.

El 18 de octubre se recuperaron las 18 láminas originales y se comprobaron sus hashes, referencias y código de inferencia. Se actualizaron los informes y las métricas sin repetir peticiones ni cambiar puntuaciones. Los registros originales están en [el archivo histórico](historico/evaluacion-inicial/README.md). Los JSON conservan la fecha y la rúbrica de cada evaluación.

Para esa actualización se utilizó `.cache/evaluation-venv`, un entorno aislado con las dependencias del proyecto:

```powershell
.\.cache\evaluation-venv\Scripts\python.exe -m scripts.evaluate --input .cache/principal-preserved.json --output docs/evaluacion-principal.json
.\.cache\evaluation-venv\Scripts\python.exe -m scripts.evaluate --input .cache/complementary-preserved.json --output docs/evaluacion-limitaciones.json
```

En esa comprobación pasaron 61 pruebas y las revisiones de Ruff, y coincidieron los hashes de las 38 imágenes. Hubo dos advertencias de obsolescencia. No se inició un servidor nuevo.

La muestra es pequeña y no representa todos los materiales educativos. Nueve ilustraciones comparten estilo y las fuentes públicas podrían haber aparecido en el entrenamiento. Faltan validación independiente de las puntuaciones y pruebas con usuarios de lectores de pantalla. Estos resultados no certifican conformidad WCAG.
