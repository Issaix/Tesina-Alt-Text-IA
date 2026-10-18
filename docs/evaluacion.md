# Evaluación de las descripciones

El set vigente de la línea A contiene **20 imágenes: 10 fotografías y 10 ilustraciones de propósito general**. Las gráficas, los diagramas y los esquemas con datos se eliminaron del set. La delimitación procede de la ficha de proyecto proporcionada por el autor.

## Ejecutar la evaluación

Prepara los modelos e inicia el servidor como indica el [README](../README.md). En otra terminal, desde la raíz del proyecto:

```powershell
.\.venv\Scripts\python.exe -m scripts.evaluate --output .cache/evaluation.json
```

El evaluador envía cada imagen a `POST /describe` y guarda código HTTP, respuesta literal, tiempo, hash, referencia y contexto. Produce informes JSON y Markdown. Conserva los fallos y continúa con las otras imágenes. Usa `--base-url` si el servidor está en otro puerto.

El campo `passed` y el código de salida 0 indican que se cumplió el contrato HTTP. La calidad queda pendiente hasta incorporar una revisión de contenido. No se puntúa por coincidencia literal con la referencia: se aceptan paráfrasis que conserven la información requerida.

## Revisar la calidad

Abrir cada imagen y comparar la salida con `context`, `reference` y `required_content`, siguiendo la [rúbrica](rubrica-alt-text.md). Registrar una lista JSON de revisiones con:

| Campo | Contenido |
|---|---|
| `file`, `sha256` | Archivo y hash de la imagen, copiados del informe |
| `description_sha256` | SHA-256 del texto exacto de la salida en UTF-8 |
| `scores` | `identification`, `context`, `essential`, `fidelity` y `clarity`, de 0 a 2 |
| `critical_error` | Error crítico identificado o cadena vacía |
| `notes`, `correction` | Justificación y corrección necesaria |
| `reviewer`, `reviewed_at` | Revisor y fecha |

`scripts.evaluate.description_hash(texto)` calcula el hash de una salida. El evaluador rechaza revisiones duplicadas, hashes que no corresponden y puntuaciones inválidas. Las peticiones fallidas quedan sin evaluación de calidad.

Para aplicar una revisión sin repetir la inferencia:

```powershell
.\.venv\Scripts\python.exe -m scripts.evaluate --input .cache/evaluation.json --reviews docs/evaluacion-principal-revisiones.json --output docs/evaluacion-principal.json
```

Solo reutilizar una revisión si corresponde a las mismas imágenes y salidas. Las puntuaciones del asistente son preliminares y requieren validación del autor antes de utilizarlas como resultados definitivos de la tesina.

## Evidencia vigente

- [Informe legible](evaluacion-principal.md).
- [Respuestas, metadatos y puntuaciones](evaluacion-principal.json).
- [Revisiones con sus justificaciones](evaluacion-principal-revisiones.json).
- [Discusión de limitaciones](limitaciones-modelo.md).

La nueva ejecución usa Windows, CPU y Python 3.12.14 en `.cache/evaluation-venv`, con las dependencias ya declaradas. No sustituye el `.venv` anterior ni modifica dependencias. Los pesos de BLIP y OPUS-MT están fijados a las revisiones de `app/captioning.py`; se usan desde la caché local, con `HF_HUB_OFFLINE=1`.

Comandos utilizados para esta ejecución, en terminales distintas:

```powershell
$env:HF_HUB_OFFLINE='1'
.\.cache\evaluation-venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 58823
```

```powershell
.\.cache\evaluation-venv\Scripts\python.exe -m scripts.evaluate --base-url http://127.0.0.1:58823 --output .cache/linea-a-20-raw.json
.\.cache\evaluation-venv\Scripts\python.exe -m scripts.evaluate --input .cache/linea-a-20-raw.json --reviews docs/evaluacion-principal-revisiones.json --output docs/evaluacion-principal.json
```

El puerto 58823 corresponde a una instancia propia para esta comprobación. Los tiempos incluyen transporte HTTP e inferencia; la primera petición puede incluir la carga de modelos. Las versiones y hashes se conservan en el JSON.

## Resultados de la ejecución actual

Las **20 peticiones respondieron HTTP 200** con el contrato esperado. La revisión preliminar del asistente clasificó las 20 descripciones como **requiere revisión**, con una media de **7,95/10**. Ninguna cubrió todo el contenido obligatorio; no se identificaron errores críticos en esta revisión.

| Tipo | Imágenes | HTTP correcto | Requieren revisión | Media / 10 |
|---|---:|---:|---:|---:|
| Fotografía | 10 | 10 | 10 | 7,8 |
| Ilustración | 10 | 10 | 10 | 8,1 |

Una suma de 8 o más no basta para declarar una salida apta: la rúbrica exige 2 puntos en información esencial. Las comparaciones por tipo son descriptivas y no demuestran una ventaja general de un tipo sobre otro.

La ejecución completa se repitió sobre las 20 imágenes. Para las diez conservadas se reutilizaron los juicios anteriores solo después de confirmar que imagen, referencia y texto generado eran los mismos; las diez añadidas se revisaron tras inspeccionar sus imágenes y salidas.

Al finalizar se detuvo la instancia propia con `Ctrl+C` y los registros confirmaron su cierre. La validación terminó con **59 pruebas correctas**, Ruff sin errores de lint o formato, y los 20 hashes verificados. Persisten dos advertencias de deprecación de las herramientas de pruebas, sin fallos. No se ejecutaron comandos de Git.

## Cambio de conjunto y límites

Se eliminaron las 18 imágenes con datos, su manifiesto y sus generadores. Se añadieron una fotografía y nueve ilustraciones generales al conjunto anterior de 10 imágenes. El catálogo y el manifiesto actuales contienen exactamente 20 archivos distintos, con referencias y licencias. El comando `scripts.create_examples` ahora verifica o restaura estos archivos desde sus fuentes.

Los informes anteriores se conservan como [antecedente histórico](historico/evaluacion-inicial/README.md). Sus resultados no se mezclan con la evaluación vigente.

El set es una muestra de conveniencia. Nueve ilustraciones comparten el estilo de OpenMoji y varias fotografías son texturas o primeros planos; no representa toda la diversidad educativa. Las fuentes públicas pueden haber aparecido en el entrenamiento. No se ha medido el acuerdo entre revisores ni realizado una evaluación con usuarios de lectores de pantalla.
