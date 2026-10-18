# Rúbrica de calidad del texto alternativo

Esta rúbrica evalúa descripciones en español de **fotografías e ilustraciones de propósito general** usadas en actividades educativas. Las gráficas, los diagramas y los esquemas con datos quedan fuera de la línea A.

La escala es una propuesta de trabajo de la tesina. No es una escala oficial de WCAG ni sustituye una evaluación con usuarios de lectores de pantalla.

## Información esperada

Una buena descripción identifica el sujeto o la escena, explica los rasgos y las relaciones que necesita la actividad y evita añadir detalles sin respaldo. En fotografías puede importar una acción, la postura o el entorno; en ilustraciones, la forma, el color o la disposición de los objetos.

El [manifiesto](../examples/educational/manifest.json) define para cada imagen:

- `context`: propósito educativo de la revisión.
- `reference`: una descripción correcta posible.
- `required_content`: información necesaria para ese propósito y afirmaciones que deben evitarse.

Se aceptan sinónimos y otras redacciones que conserven el significado. Las advertencias no tienen que repetirse en el alt-text. El contexto sirve al revisor; la API recibe únicamente la imagen. No se exige identificar personas, especies, lugares o información obtenida solo de la fuente.

## Puntuación

Cada criterio recibe de 0 a 2 puntos; el máximo es 10.

| Criterio | 0 puntos | 1 punto | 2 puntos |
|---|---|---|---|
| Identificación del contenido | Confunde o no identifica el sujeto principal. | Reconoce una parte, pero deja ambiguo el contenido principal. | Identifica correctamente el objeto, la escena o el sujeto. |
| Contexto y relaciones | Omite o cambia la situación o las relaciones relevantes. | Conserva parte del contexto, pero faltan relaciones necesarias. | Conserva la postura, disposición o situación que necesita la actividad. |
| Información esencial | Omite la mayor parte del contenido obligatorio. | Incluye una parte, pero falta al menos un elemento importante. | Incluye todo el contenido definido en `required_content`. |
| Fidelidad a la imagen | Inventa o cambia información que altera el significado educativo. | Contiene una imprecisión secundaria o un detalle sin respaldo. | Todas las afirmaciones son comprobables y no hay contradicciones. |
| Claridad y concisión | Es confuso, repetitivo o no ofrece una descripción comprensible en español. | Se entiende, pero contiene ambigüedades, repeticiones o distracciones. | Es claro, ordenado y suficientemente breve para la información necesaria. |

La información esencial mide lo que falta; la fidelidad mide lo que se afirma incorrectamente. Una descripción genérica puede ser fiel y resultar insuficiente para la actividad.

## Decisión

Primero se identifica si hay un **error crítico**: por ejemplo, confundir el sujeto principal, inventar una acción esencial o invertir una relación necesaria. En ese caso la descripción es **no apta**, independientemente del total.

Sin errores críticos:

- **Apta para el contexto definido:** de 8 a 10 puntos, con 2 en identificación, información esencial y fidelidad, y al menos 1 en los otros criterios.
- **Requiere revisión:** de 6 a 10 puntos cuando no cumple todas las condiciones anteriores.
- **No apta:** de 0 a 5 puntos.

Una omisión obligatoria impide declarar una salida apta aunque sume 8 o más. La decisión se refiere al contexto de revisión, no certifica la accesibilidad del material completo.

## Ejemplo

Para la fotografía de la taza de café:

| Descripción | Valoración ilustrativa |
|---|---|
| «Taza de café sobre un plato, con una cucharilla, en una mesa de madera.» | Conserva sujeto, disposición e información requerida: 10 puntos, apta. |
| «Una taza.» | Identificación 1, contexto 0, información 0, fidelidad 2 y claridad 2: 5 puntos, no apta para esa actividad. |

Los ejemplos explican la escala; no son nuevas salidas del modelo.

## Registro de revisión

Abrir la imagen, leer su contexto y comparar la salida con la referencia. Registrar los cinco puntajes, los errores críticos, una justificación y la corrección necesaria. Identificar al revisor y la fecha. Las valoraciones del asistente son preliminares y requieren validación del autor.

La [guía de evaluación](evaluacion.md) explica el formato de registro y la generación de informes. La extensión del texto depende de la información que necesita la actividad; no se fija un máximo universal de caracteres. Esta revisión sigue la orientación de W3C WAI sobre el propósito y contexto de las [imágenes informativas](https://www.w3.org/WAI/tutorials/images/informative/).
