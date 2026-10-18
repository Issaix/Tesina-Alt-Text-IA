# Limitaciones del modelo en la línea A

El objetivo principal de la línea A son **fotografías e ilustraciones de propósito general**, evaluadas con un set de 20 imágenes. Las actividades de revisión de límites añaden un conjunto complementario de 18 imágenes con datos: 11 diagramas y 7 gráficas. Sus resultados se mantienen separados.

## Alcance de los resultados

El servicio describe la imagen con BLIP base y traduce el resultado mediante OPUS-MT. Recibe únicamente la imagen: no conoce el contexto de la actividad ni la referencia utilizada por el revisor. La generación está limitada a 60 tokens en inglés y 100 en español.

Los resultados corresponden al flujo completo. Sin registrar el texto intermedio en inglés, no es posible atribuir un fallo concreto exclusivamente al modelo visual o a la traducción. Una respuesta HTTP 200 acredita que se generó texto con el contrato esperado, pero no que ese texto sea suficiente para la actividad educativa.

El [informe vigente](evaluacion-principal.md) conserva la salida literal, la referencia, las puntuaciones y la corrección propuesta para cada imagen. Las valoraciones del asistente son preliminares y deben ser validadas por el autor.

## Resultados observados en el set de 20 imágenes

Las 20 imágenes se procesaron correctamente por HTTP. La revisión preliminar clasificó sus 20 salidas como **requiere revisión**, con media de **7,95/10**: 7,8 en fotografías y 8,1 en ilustraciones. No se identificaron errores críticos, pero todas las salidas omitieron al menos un elemento obligatorio del contexto definido. Estos resultados no equivalen a una evaluación humana independiente.

| Imagen | Salida real | Limitación observada |
|---|---|---|
| Café | «una taza de café en una mesa de madera» | Faltan el plato y la cucharilla. |
| Mariposa | «una mariposa azul sobre un fondo blanco» | Omite las alas extendidas, el cuerpo y las antenas. |
| Libro | «un icono de libro abierto» | Omite las páginas y las líneas que representan texto. |
| Casa | «una casa con un techo rojo» | Omite la puerta y la ventana. |
| Águila | «una foto en blanco y negro de un pájaro sentado en una pipa» | No precisa que es un ave rapaz ni sus alas plegadas; pipa es una expresión imprecisa para el soporte tubular. |

Se observaron dos patrones: descripciones breves que reconocen el sujeto pero no cubren la actividad, y expresiones secundarias imprecisas. En las fotografías conservadas, por ejemplo, se atribuye hombre a la astronauta de la referencia y traje al abrigo del fotógrafo. Se registraron como imprecisiones secundarias, no como cambios del tema principal.

En las ilustraciones, acertar el objeto y el color no garantiza conservar los rasgos necesarios. La media ligeramente mayor de las ilustraciones no permite concluir que el modelo funcione mejor en esa categoría: son pocos casos, con objetos y estilos distintos de las fotografías.

## Limitaciones observadas en gráficas y diagramas

El [informe complementario](evaluacion-limitaciones.md) conserva 18 respuestas HTTP correctas, valoradas preliminarmente como no aptas para recuperar los datos de sus contextos. La media es 2,83/10 y se identificaron errores críticos en 10 casos. Estas métricas no se suman al conjunto principal ni indican que la interpretación especializada sea responsabilidad de la línea A.

Las respuestas se obtuvieron el 17 de octubre de 2026. El 18 se recuperaron las imágenes originales y se comprobaron sus hashes, referencias y código de inferencia frente al informe guardado. No se ejecutó una inferencia nueva ni se modificaron las puntuaciones al recuperar la evidencia.

| Imagen | Salida real | Fallo frente a la referencia |
|---|---|---|
| Libros leídos | «un gráfico de barras muestra el número de personas que están utilizando Internet» | Reconoce las barras, cambia el tema y omite A: 4, B: 7 y C: 10 libros. |
| Temperaturas | «un gráfico de líneas que muestra el número de personas en el país» | Cambia temperatura por personas y omite días, grados, escala, valores y extremos. |
| Rectángulo | «superficie 8 cm superficie 8 m quado 4 m» | Mezcla unidades y no conserva área de 32 cm cuadrados ni perímetro de 24 cm. |
| Estados del agua | «un diagrama que muestra el flujo de un líquido en un líquido» | No distingue sólido, líquido y gas ni los cambios de estado y sus sentidos. |
| Ciclo de mariposa | «cio vida una impo» | No ofrece una secuencia comprensible ni conserva huevo, larva, pupa y adulto. |
| Reciclaje | «un gráfico de barras que muestra el porcentaje del número de personas en México» | Inventa tema, unidad y ubicación en lugar de masa de papel, vidrio y plástico. |

Se observaron omisiones de etiquetas, cifras y relaciones, cambios de tema y problemas de redacción. Reconocer la forma global de una gráfica no implica interpretar sus datos. El flujo actual genera una descripción general y la traduce; no incluye una etapa especializada de lectura de ejes, extracción de valores o reconstrucción de diagramas.

Sin revisar el texto intermedio en inglés no se puede atribuir cada error a BLIP o a OPUS-MT por separado. Los fallos observados pertenecen al flujo completo y a este conjunto concreto, no demuestran que todas las imágenes con datos fallen.

Para imágenes complejas, la [guía de W3C WAI](https://www.w3.org/WAI/tutorials/images/complex/) contempla una identificación breve acompañada de información detallada. La referencia completa de este piloto representa la información que debe conservarse; no se presupone que toda ella deba insertarse en un atributo HTML `alt`.

## Limitaciones de la evaluación

- El conjunto de 20 imágenes es una muestra de conveniencia, no una muestra representativa de todos los materiales educativos.
- Nueve de las diez ilustraciones comparten el estilo de OpenMoji. Es necesario incorporar otros estilos y escenas más complejas antes de generalizar.
- Varias fotografías muestran texturas o primeros planos; hay poca diversidad de acciones e interacciones entre personas y objetos.
- Las fuentes son públicas y podrían haber formado parte del entrenamiento. No se garantiza independencia respecto de esos datos.
- Los contextos y el contenido obligatorio se fijaron antes de revisar las salidas. Una descripción puede resultar insuficiente para ese contexto aunque sea útil en otro; no se juzga por coincidencia literal con la referencia.
- No se realizó una evaluación con usuarios de lectores de pantalla ni se midió el acuerdo entre revisores. Una puntuación alta no certifica conformidad WCAG.
- Los tiempos incluyen transporte HTTP e inferencia. La primera petición puede incluir la carga de los modelos; no son una comparación de rendimiento entre modelos.

## Uso de las descripciones

Las salidas deben tratarse como borradores. La revisión debe comprobar sujeto, rasgos necesarios, disposición de los objetos y cualquier afirmación sin respaldo. Para fortalecer la discusión de la tesina conviene validar las puntuaciones con el asesor y añadir una segunda revisión independiente.

La interpretación especializada de gráficas y diagramas corresponde a otra línea. Su inclusión en pruebas complementarias no añade un clasificador ni un intérprete especializado a la API: el servicio sigue aceptando archivos según sus validaciones de formato.
