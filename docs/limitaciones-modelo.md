# Limitaciones del modelo en la línea A

La evaluación vigente se limita a **fotografías e ilustraciones de propósito general**. El set contiene 20 imágenes, repartidas por igual entre ambos tipos. Las imágenes con datos se retiraron; los informes previos quedaron en el [archivo histórico](historico/evaluacion-inicial/README.md).

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

La interpretación especializada de gráficas y diagramas corresponde a otra línea. Su eliminación del set no añade un clasificador a la API: este servicio sigue aceptando archivos de imagen según sus validaciones de formato.
