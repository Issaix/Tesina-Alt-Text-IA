# Alineación del proyecto con sus objetivos

Revisión del 18 de octubre de 2026, basada en la ficha «Línea A · Descripción automática de imágenes (alt-text con IA)» proporcionada por el autor y en el código disponible. El servicio mantiene el foco en fotografías e ilustraciones generales. Las gráficas y los diagramas se utilizan para evaluar límites, como piden las actividades recientes.

## Objetivo general

Diseñar, implementar y evaluar un microservicio que genere alt-text en español para fotografías e ilustraciones de propósito general presentes en contenidos educativos, con una API REST integrable a la arquitectura de remediación de accesibilidad, y valorar la calidad de sus descripciones según el criterio de contenido no textual de WCAG.

El código sigue esta dirección, pero el objetivo completo aún no se ha alcanzado. La API genera borradores y conserva evidencia de evaluación. La pertinencia final del texto, la contenerización y la integración con el orquestador requieren trabajo adicional.

## Objetivos específicos y evidencia

| Objetivo de la ficha | Implementación actual | Estado y pendiente |
|---|---|---|
| Diseñar la generación en español, el modelo, el flujo y los criterios de calidad | `app/captioning.py` fija BLIP base y OPUS-MT a revisiones concretas. `app/images.py` valida y convierte la imagen a RGB. La rúbrica define cinco criterios. | Flujo implementado. La calidad observada requiere correcciones; falta validación del autor y del contexto educativo. |
| Implementar un microservicio REST documentado y contenerizado, integrable al orquestador | `app/main.py` registra las rutas. `app/api/describe.py` recibe un archivo multipart y devuelve `description`; OpenAPI documenta el contrato y los errores. | API implementada. No hay Dockerfile ni imagen de contenedor; tampoco se ha comprobado la integración real con el orquestador. |
| Evaluar con métricas y rúbrica, registrar resultados y limitaciones | `scripts/evaluate.py` conserva respuestas, hashes y referencias; aplica revisiones explícitas y calcula medias, decisiones y errores críticos por conjunto y tipo. | Evidencia disponible: 20 imágenes principales y 18 complementarias. Las puntuaciones son preliminares; falta revisión humana independiente y evaluación con usuarios. |

## Relación con las actividades recientes

| Actividad | Evidencia actual |
|---|---|
| Definir una rúbrica con objeto, contexto y datos cuando corresponda | [Rúbrica](rubrica-alt-text.md): criterios generales y aplicación complementaria a datos, unidades, valores y relaciones. |
| Ampliar el set con imágenes y referencias | 20 fotografías e ilustraciones en [educational](../examples/educational/README.md), más 11 diagramas y 7 gráficas en [limitations](../examples/limitations/README.md). Cada imagen tiene contexto, referencia, contenido obligatorio y hash. |
| Evaluar `/describe` y registrar resultados | [Informe principal](evaluacion-principal.md) y [complementario](evaluacion-limitaciones.md), con sus respuestas y revisiones JSON. Las métricas permanecen separadas. |
| Documentar fallos en imágenes con datos | [Limitaciones del modelo](limitaciones-modelo.md), con ejemplos reales de cambios de tema, omisiones, unidades incorrectas y texto confuso. |

## Revisión del recorrido del código

1. FastAPI recibe el archivo en `POST /describe`; la ruta no recibe referencias ni respuestas esperadas.
2. `app/images.py` comprueba formato, MIME, tamaño y resolución, corrige orientación y transparencias, y devuelve RGB.
3. `CaptioningService` genera una descripción con BLIP y la traduce con OPUS-MT. No se entrenan modelos ni se añaden motores especializados para gráficas.
4. La ruta devuelve un JSON con `description` o un error documentado. La imagen y sus recursos temporales se cierran al terminar.
5. El evaluador envía las imágenes por HTTP y guarda la salida literal. La calidad procede de una revisión identificada, nunca del HTTP 200 por sí solo.

La API valida archivos, pero no clasifica semánticamente si una imagen es fotografía, gráfica o diagrama. Los tipos y el propósito se declaran en los manifiestos de evaluación. El evaluador permite diagramas en el conjunto complementario y evita mezclarlo con el principal.

## Cambios de esta revisión

Se recuperaron las 18 láminas originales del repositorio por lectura y se comprobó su identidad con los hashes de las respuestas guardadas. Se actualizó el evaluador para permitir ese alcance complementario y conservar la rúbrica y la fecha de las valoraciones históricas al reprocesarlas. Se aclaró el alcance en OpenAPI y se incorporaron medias por criterio y recuentos de errores críticos.

No se necesitó repetir la inferencia: imágenes, referencias, revisiones de modelos y código de inferencia coinciden con la evidencia del 17 de octubre. Los informes indican expresamente esa procedencia. Esta revisión no declara terminada la tesina ni certifica conformidad WCAG.
