# Sprint 1: descripción de imágenes

**Informe histórico:** las cuatro láminas de esta prueba inicial forman parte del [conjunto complementario de limitaciones](../examples/limitations/README.md). El conjunto principal contiene 20 fotografías e ilustraciones generales; sus resultados están en el [informe actual](evaluacion-principal.md).

## Objetivo

El objetivo fue completar una primera versión que recibiera una imagen por HTTP y devolviera una descripción. Se priorizó que el flujo funcionara antes de mejorar la calidad del texto.

La implementación y las pruebas se realizaron el 27 de septiembre de 2026 en Windows, con Python 3.12.14 y PyTorch 2.7.1 en CPU. Este informe recoge el trabajo local; la publicación y el estado del tablero de GitHub se gestionan por separado.

## Actividades realizadas

| Actividad | Prioridad | Resultado |
|---|---|---|
| 1. Preparar el entorno | Alta | Se creó el entorno virtual, se instalaron las dependencias y se comprobó el arranque de la API. |
| 2. Recibir imágenes | Alta | Se añadió `POST /describe` con un archivo multipart en el campo `image`. |
| 3. Validar la entrada | Media | Se comprobaron JPG, JPEG y PNG, archivos dañados, tamaños, resolución y formatos incompatibles. |
| 4. Integrar el modelo | Alta | Se conectaron BLIP base y OPUS-MT para obtener una descripción en español. |
| 5. Conectar la API con el modelo | Alta | La imagen recibida se normaliza y se procesa automáticamente. |
| 6. Devolver JSON | Alta | La respuesta exitosa contiene una cadena no vacía en `description`. |
| 7. Probar imágenes educativas | Alta | Se enviaron cuatro imágenes por HTTP y se guardaron sus respuestas. |
| 8. Documentar el uso | Media | Se añadieron instrucciones de instalación, ejecución y pruebas al README. |

## Modelos utilizados

| Función | Modelo | Revisión |
|---|---|---|
| Descripción en inglés | `Salesforce/blip-image-captioning-base` | `82a37760796d32b1411fe092ab5d4e227313294b` |
| Traducción al español | `Helsinki-NLP/opus-mt-en-es` | `5bc4493d463cf000c1f0b50f8d56886a392ed4ab` |

Los pesos se descargan una vez y se cargan desde disco. Cada proceso conserva los modelos en memoria y atiende una inferencia a la vez. No se entrenó ni ajustó ninguno de los modelos.

La generación usa tres candidatos de búsqueda y evita repetir secuencias de tres tokens. Este ajuste reduce las repeticiones, pero no impide que el modelo invente información.

## Prueba con imágenes educativas

Se inició Uvicorn en `127.0.0.1:54023` con los pesos descargados y el modo sin conexión activado. Las imágenes se enviaron con el evaluador del proyecto. Las respuestas siguientes pertenecen a aquella ejecución. Para realizar una prueba nueva, seguir la [guía de evaluación](evaluacion.md).

Las cuatro láminas se crearon con Pillow y se incluyeron en la entrega original. El archivo de respuestas conserva su procedencia y referencia. Esas referencias se usaron para revisar las respuestas, no como entrada del modelo. Tras ajustar el conjunto a la ficha de la línea A, estas láminas se ubicaron en el conjunto complementario; los resultados históricos se conservan sin cambios.

Estos fueron los resultados de la entrega inicial, conservados sin corregir el texto generado:

| Imagen | HTTP | Descripción generada | Segundos |
|---|---|---|---:|
| Triángulo | 200 | un triángulo se muestra en el lado derecho de un triángulo derecho | 15.387 |
| Gráfico de barras | 200 | un gráfico de barras muestra el número de personas que están utilizando Internet | 5.098 |
| Sol, Tierra y Luna | 200 | un diagrama de los planetas y sus nombres | 3.215 |
| Planta | 200 | un diagrama de una flor con el nombre de la planta | 4.110 |

La primera petición incluyó la carga de los modelos en memoria. Los tiempos corresponden a una sola ejecución y sirven como referencia, no como una medición general de rendimiento.

El [registro original](sprint-1-results.json) conserva la fecha, las respuestas, las revisiones de los modelos y el hash de cada imagen. El campo `passed` indica que la petición devolvió el JSON esperado; no evalúa si la descripción es correcta.

## Qué falta mejorar

En el triángulo, el modelo reconoce la figura, pero omite las medidas de 3, 4 y 5 cm y produce una frase confusa. En el gráfico de barras, identifica el tipo de gráfico, pero inventa que trata sobre el uso de Internet; los datos reales son libros leídos por tres grupos.

En la lámina de astronomía, llama planetas al conjunto y no distingue el Sol, la Tierra y la Luna. En la planta, reconoce la flor, pero omite las hojas, el tallo y las raíces, y confunde las etiquetas con un nombre.

El flujo funciona, pero estas descripciones todavía no son suficientes para sustituir las imágenes en una actividad educativa. Hace falta revisar el contenido, añadir el contexto de la lección y comprobar qué información necesita quien usa un lector de pantalla. Por ello, esta versión no demuestra cumplimiento del [criterio WCAG 1.1.1](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html).

## Pruebas y mantenimiento

En la entrega inicial pasaron 26 pruebas automatizadas. En la revisión de mantenimiento de esa etapa se aprobaron **37 pruebas**. Comprueban formatos, archivos dañados, límites, orientación, transparencia, errores del modelo, disponibilidad de la API durante el procesamiento y conservación de los resultados cuando una evaluación falla.

También se repitieron las cuatro peticiones con los modelos reales tras la revisión. Todas devolvieron HTTP 200 y conservaron las mismas descripciones de la tabla. El registro original del sprint se mantuvo sin cambios.

La revisión añadió tipos a las interfaces, un formato uniforme con Ruff y comprobaciones de GitHub Actions. La decodificación de imágenes pasó a ejecutarse fuera del bucle de la API y se redujeron las copias de imágenes opacas. Las instrucciones para mantener estas comprobaciones están en la [guía de desarrollo](desarrollo.md).

Las próximas etapas se centrarán en la calidad del texto, las pruebas con usuarios, la contenerización y la integración con el orquestador.
