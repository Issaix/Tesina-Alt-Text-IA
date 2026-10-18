# Conjunto complementario de limitaciones

Estas **18 imágenes —11 diagramas y 7 gráficas—** permiten estudiar los límites del modelo ante información educativa con datos. Se añaden a las 20 imágenes principales de la línea A y se evalúan por separado. No cambian el objetivo de producción del microservicio.

El [manifiesto](manifest.json) incluye tipo, contexto, referencia, contenido obligatorio, procedencia y SHA-256. Las láminas son originales del proyecto. Se recuperaron sin cambios del repositorio el 18 de octubre de 2026; sus hashes coinciden con los de las respuestas reales obtenidas el 17 de octubre. No se atribuye una licencia de redistribución que el autor no haya declarado.

## Contenido

| Tipo | Archivos |
|---|---|
| Diagramas de geometría | `triangulo.png`, `tipos_triangulos.png`, `rectangulo.png`, `fracciones.png`, `coordenadas.png` |
| Diagramas de ciencias | `astronomia.jpeg`, `planta.png`, `estados_agua.png`, `cadena_alimentaria.png`, `circuito.png`, `ciclo_mariposa.png` |
| Gráficas | `barras.jpg`, `temperaturas.png`, `transporte.png`, `precipitacion.png`, `reciclaje.png`, `temperaturas_negativas.png`, `dispersion_plantas.png` |

Las referencias requieren conservar medidas, relaciones y etapas en diagramas; categorías, valores, unidades, signos y comparaciones en gráficas. Los datos ficticios están identificados en cada caso. El modelo recibe solo la imagen, no estos textos.

## Uso

Con el servidor en ejecución:

```powershell
.\.venv\Scripts\python.exe -m scripts.evaluate --manifest examples/limitations/manifest.json --output .cache/limitations.json
```

Para comprobar los archivos y sus hashes:

```powershell
.\.venv\Scripts\python.exe -m scripts.create_examples --manifest examples/limitations/manifest.json
```

Si falta una lámina, se debe recuperar su versión original del repositorio; el verificador no genera una sustitución con contenido o hash diferente.

Resultados: [informe complementario](../../docs/evaluacion-limitaciones.md). Método y alcance: [guía de evaluación](../../docs/evaluacion.md) y [alineación con los objetivos](../../docs/alineacion-proyecto.md).
