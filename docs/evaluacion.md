# Evaluación de las descripciones

La evaluación mantiene el objetivo de la línea A y cumple las actividades de revisión de límites mediante dos conjuntos separados:

| Conjunto | Carpeta | Imágenes | Finalidad |
|---|---|---:|---|
| Principal | `examples/educational` | 20: 10 fotografías y 10 ilustraciones | Valorar la generación de alt-text para imágenes generales |
| Complementario | `examples/limitations` | 18: 11 diagramas y 7 gráficas | Documentar dónde falla el flujo ante datos y relaciones |

Los resultados complementarios no se suman a la calidad del objetivo principal ni convierten el servicio en un intérprete especializado. La [revisión de alineación](alineacion-proyecto.md) relaciona el código con los objetivos de la ficha.

## Ejecutar el servicio sobre los conjuntos

Prepara los modelos e inicia el servidor como indica el [README](../README.md). En otra terminal, desde la raíz:

```powershell
.\.venv\Scripts\python.exe -m scripts.evaluate --output .cache/principal.json
.\.venv\Scripts\python.exe -m scripts.evaluate --manifest examples/limitations/manifest.json --output .cache/limitations.json
```

Usa `--base-url` si el servidor está en otro puerto. Cada comando produce JSON y Markdown. El evaluador envía cada imagen a `POST /describe` y guarda salida literal, código HTTP, tiempo, hash, contexto, referencia y contenido obligatorio. Conserva los fallos y continúa con las demás imágenes.

El campo `passed` y el código de salida 0 comprueban el contrato HTTP. La calidad queda pendiente hasta incorporar una revisión identificada. Los manifiestos deben contener un único alcance y tipos compatibles con él; el predeterminado sigue siendo el principal de 20 imágenes.

Para verificar los archivos antes de evaluar:

```powershell
.\.venv\Scripts\python.exe -m scripts.create_examples
.\.venv\Scripts\python.exe -m scripts.create_examples --manifest examples/limitations/manifest.json
```

Las imágenes principales ausentes se recuperan desde sus fuentes públicas. Las láminas originales del proyecto se recuperan del repositorio; el verificador no inventa sustituciones si falta alguna o cambia su hash.

## Comparar con la referencia

Abrir cada imagen y comparar la salida con `context`, `reference` y `required_content`, siguiendo la [rúbrica](rubrica-alt-text.md). Se aceptan paráfrasis y sinónimos. Las advertencias del manifiesto indican qué no debe afirmarse; no hay que repetirlas en el alt-text.

Registrar una lista JSON de revisiones:

| Campo | Contenido |
|---|---|
| `file`, `sha256` | Archivo y hash de la imagen |
| `description_sha256` | SHA-256 de la salida exacta en UTF-8 |
| `scores` | `identification`, `context`, `essential`, `fidelity` y `clarity`, de 0 a 2 |
| `critical_error` | Error crítico identificado o cadena vacía |
| `notes`, `correction` | Justificación y corrección necesaria |
| `reviewer`, `reviewed_at` | Revisor y fecha |

`scripts.evaluate.description_hash(texto)` calcula el hash del texto. El evaluador rechaza revisiones duplicadas, hashes distintos y puntuaciones inválidas. Una petición fallida queda sin evaluación de calidad.

Para aplicar revisiones sin repetir la inferencia:

```powershell
.\.venv\Scripts\python.exe -m scripts.evaluate --input .cache/principal.json --reviews docs/evaluacion-principal-revisiones.json --output .cache/principal-revisado.json
.\.venv\Scripts\python.exe -m scripts.evaluate --input .cache/limitations.json --reviews docs/evaluacion-limitaciones-revisiones.json --output .cache/limitations-revisado.json
```

Solo reutilizar revisiones para las mismas imágenes, salidas, referencias y criterios. Si cambia la salida, hay que revisarla de nuevo. Las valoraciones del asistente son preliminares y requieren validación del autor para su uso definitivo en la tesina.

Las métricas son medias totales y por criterio, decisiones por tipo de imagen y recuento de errores críticos. Se calculan sobre las salidas revisadas; no se presenta una similitud literal como medida de pertinencia ni se interpreta HTTP 200 como aprobación de calidad.

## Resultados y procedencia

| Conjunto | HTTP correcto | Requieren revisión | No aptas | Errores críticos | Media / 10 |
|---|---:|---:|---:|---:|---:|
| Principal | 20/20 | 20 | 0 | 0 | 7,95 |
| Complementario | 18/18 | 0 | 18 | 10 | 2,83 |

En ambos conjuntos hubo 0 salidas clasificadas como aptas. En el principal faltó al menos un elemento obligatorio por salida. En el complementario se observaron omisiones y cambios de tema, unidades o relaciones.

Informes con cada respuesta y su justificación:

- Principal: [Markdown](evaluacion-principal.md), [JSON](evaluacion-principal.json) y [revisiones](evaluacion-principal-revisiones.json).
- Complementario: [Markdown](evaluacion-limitaciones.md), [JSON](evaluacion-limitaciones.json) y [revisiones](evaluacion-limitaciones-revisiones.json).
- Discusión: [limitaciones del modelo](limitaciones-modelo.md).

Las respuestas HTTP y las puntuaciones proceden del **17 de octubre de 2026**, con Windows, Python 3.12.14 y procesamiento en CPU. Las revisiones concretas de BLIP y OPUS-MT, las bibliotecas y los tiempos están en los JSON. La primera petición puede incluir la carga de modelos; estos tiempos no constituyen una comparación de rendimiento.

El **18 de octubre** se recuperaron las 18 imágenes originales por lectura del repositorio. Todas coinciden por SHA-256 con las evaluadas. Se comprobaron también referencias, salidas y código de inferencia. Se conservaron las 20 imágenes principales y se reprocesaron ambos informes para añadir métricas y aclarar la procedencia, sin nuevas peticiones ni nuevas puntuaciones.

Cada JSON conserva la fecha HTTP, el hash y la ubicación de la rúbrica usada en sus valoraciones, además del hash de la rúbrica vigente. La ampliación de esta última añade el apartado complementario y mantiene las cinco reglas de puntuación. Las copias originales permanecen en `docs/historico`.

Comandos utilizados para actualizar los informes desde esa evidencia verificada:

```powershell
.\.cache\evaluation-venv\Scripts\python.exe -m scripts.evaluate --input .cache/principal-preserved.json --output docs/evaluacion-principal.json
.\.cache\evaluation-venv\Scripts\python.exe -m scripts.evaluate --input .cache/complementary-preserved.json --output docs/evaluacion-limitaciones.json
```

Se utilizó el entorno aislado de evaluación con las dependencias ya declaradas. La comprobación terminó con **61 pruebas correctas**, Ruff sin errores y hashes válidos en las 38 imágenes. Hubo dos advertencias de deprecación de las herramientas de pruebas, sin fallos. No se inició un servidor nuevo ni se ejecutaron comandos de Git.

## Límites de la evidencia

El principal es una muestra de conveniencia y nueve ilustraciones comparten estilo. Las fuentes públicas podrían haber aparecido en el entrenamiento. El complementario contiene láminas sencillas definidas para esta exploración, no todos los casos posibles de imágenes con datos.

Falta validar las puntuaciones con el autor y, de ser posible, medir el acuerdo con otro revisor y evaluar con usuarios de lectores de pantalla. Los resultados no certifican conformidad WCAG. La contenerización y la integración real del microservicio también siguen pendientes, como recoge la revisión de objetivos.
