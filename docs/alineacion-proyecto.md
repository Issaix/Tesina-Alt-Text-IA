# Alineación del proyecto con sus objetivos

Esta revisión, del 18 de octubre de 2026, compara el código con la ficha «Línea A · Descripción automática de imágenes (alt-text con IA)».

## Objetivo general

Diseñar, implementar y evaluar un microservicio que genere texto alternativo en español para fotografías e ilustraciones generales de contenidos educativos, mediante una API REST integrable a la arquitectura de remediación de accesibilidad. La calidad se valora según el propósito del contenido no textual de WCAG.

El servicio ya genera borradores y dispone de resultados de evaluación. Las gráficas y los diagramas se incluyen para estudiar limitaciones, sin ampliar el objetivo principal.

## Objetivos específicos

| Objetivo | Implementación | Pendiente |
|---|---|---|
| Diseñar la generación en español y los criterios de calidad. | BLIP base y OPUS-MT en `app/captioning.py`; validación de imágenes en `app/images.py`; rúbrica de cinco criterios. | Mejorar la calidad y validar las puntuaciones en su contexto educativo. |
| Implementar una API REST documentada, contenerizada e integrable al orquestador. | Rutas registradas en `app/main.py`; recepción de imágenes en `app/api/describe.py`; documentación OpenAPI. | Crear el contenedor y comprobar la integración real con el orquestador. |
| Evaluar las salidas y documentar limitaciones. | `scripts/evaluate.py` guarda respuestas y aplica puntuaciones; informes de 20 imágenes principales y 18 complementarias. | Validación independiente y pruebas con usuarios. |

## Actividades recientes

| Actividad | Evidencia |
|---|---|
| Definir la calidad del texto alternativo. | [Rúbrica](rubrica-alt-text.md), con criterios para objetos, contexto, datos y relaciones. |
| Ampliar las imágenes de prueba y sus referencias. | [Conjunto principal](../examples/educational/README.md) y [complementario](../examples/limitations/README.md). |
| Evaluar `/describe`. | [Informe principal](evaluacion-principal.md) e [informe complementario](evaluacion-limitaciones.md), con métricas separadas. |
| Documentar errores en gráficas y diagramas. | [Limitaciones del modelo](limitaciones-modelo.md), con respuestas reales y comparación con la referencia. |

## Recorrido de una petición

1. `POST /describe` recibe un archivo; no recibe el contexto ni la referencia.
2. `app/images.py` comprueba formato, MIME, tamaño y resolución, corrige orientación y transparencia, y convierte la imagen a RGB.
3. `CaptioningService` genera una descripción con BLIP y la traduce con OPUS-MT.
4. La API devuelve `description` o un error documentado y libera los recursos de la imagen.
5. El evaluador guarda la respuesta. La calidad se determina con la rúbrica, no por el código HTTP.

La API valida los archivos, pero no identifica si son fotografías, gráficas o diagramas. Los manifiestos declaran el tipo y alcance; el evaluador impide mezclar los dos conjuntos.

## Procedencia y pendientes

Las 18 láminas complementarias se recuperaron del repositorio y sus hashes coinciden con los de las respuestas del 17 de octubre. También coinciden las referencias y el código de inferencia. Se actualizaron las métricas y la documentación sin repetir la generación.

Las puntuaciones siguen siendo preliminares. Faltan su validación, la evaluación con usuarios, el contenedor y la integración con el orquestador. La evidencia actual no certifica conformidad WCAG.
