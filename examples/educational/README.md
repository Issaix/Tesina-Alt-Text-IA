# Conjunto de imágenes de la línea A

El conjunto contiene **20 imágenes: 10 fotografías y 10 ilustraciones de propósito general**. No incluye gráficas, diagramas, esquemas con datos, duplicados ni variantes recortadas de una misma imagen.

Cada entrada del [manifiesto](manifest.json) incluye contexto educativo, referencia, contenido obligatorio, fuente, licencia y SHA-256. Las referencias se redactaron tras inspeccionar las imágenes. La API recibe solo la imagen; el contexto sirve para evaluar la salida.

## Catálogo

| Archivo | Tipo | Tema | Fuente y licencia |
|---|---|---|---|
| [astronauta.png](astronauta.png) | fotografía | Tecnología espacial | scikit-image; Dominio público |
| [gato.png](gato.png) | fotografía | Biología | scikit-image; CC0 |
| [fotografo.png](fotografo.png) | fotografía | Tecnología | scikit-image; CC0 |
| [cafe.png](cafe.png) | fotografía | Vida cotidiana | scikit-image; CC0 |
| [cohete.jpg](cohete.jpg) | fotografía | Tecnología espacial | scikit-image; Dominio público según scikit-image |
| [caballo.png](caballo.png) | ilustración | Biología | Openclipart / scikit-image; CC0 |
| [campo_estelar.jpg](campo_estelar.jpg) | fotografía | Astronomía | scikit-image; Dominio público según scikit-image |
| [ladrillos.png](ladrillos.png) | fotografía | Materiales | scikit-image; CC0 |
| [pasto.png](pasto.png) | fotografía | Ciencias naturales | scikit-image; CC0 |
| [grava.png](grava.png) | fotografía | Materiales | scikit-image; CC0 |
| [arbol.png](arbol.png) | ilustración | Ciencias naturales | OpenMoji 16.0.0; CC BY-SA 4.0 |
| [bicicleta.png](bicicleta.png) | ilustración | Transporte | OpenMoji 16.0.0; CC BY-SA 4.0 |
| [mariposa.png](mariposa.png) | ilustración | Biología | OpenMoji 16.0.0; CC BY-SA 4.0 |
| [pez.png](pez.png) | ilustración | Biología | OpenMoji 16.0.0; CC BY-SA 4.0 |
| [girasol.png](girasol.png) | ilustración | Ciencias naturales | OpenMoji 16.0.0; CC BY-SA 4.0 |
| [libro.png](libro.png) | ilustración | Lectura | OpenMoji 16.0.0; CC BY-SA 4.0 |
| [manzana.png](manzana.png) | ilustración | Alimentación | OpenMoji 16.0.0; CC BY-SA 4.0 |
| [paraguas.png](paraguas.png) | ilustración | Vida cotidiana | OpenMoji 16.0.0; CC BY-SA 4.0 |
| [casa.png](casa.png) | ilustración | Entorno construido | OpenMoji 16.0.0; CC BY-SA 4.0 |
| [aguila.png](aguila.png) | fotografía | Biología | scikit-image; CC0 |

## Procedencia y atribución

Las nueve ilustraciones nuevas son archivos originales de **OpenMoji 16.0.0**, proyecto abierto de emojis e iconos de HfG Schwäbisch Gmünd y sus colaboradores, bajo **CC BY-SA 4.0**. No se modificaron. La licencia corresponde a esas imágenes y se conserva en cada entrada del manifiesto.

- [Proyecto y atribución de OpenMoji](https://github.com/hfg-gmuend/openmoji/tree/16.0.0).
- [Licencia CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
- [Fuentes y licencias de scikit-image 0.25.2](https://github.com/scikit-image/scikit-image/blob/v0.25.2/skimage/data/_fetchers.py).

Las fotografías y la silueta del caballo proceden del conjunto de scikit-image. Sus autores y URL individuales están en el manifiesto. La fotografía del águila coincide con el hash publicado en el registro de scikit-image.

Las ilustraciones son representaciones sencillas de objetos o seres vivos, sin rótulos explicativos, flechas, ejes ni datos. El libro contiene líneas que simbolizan texto; no son palabras legibles. Los PNG transparentes se procesan con fondo blanco mediante el flujo habitual de la API.

## Comprobar o restaurar archivos

Desde la raíz del proyecto:

```powershell
.\.venv\Scripts\python.exe -m scripts.create_examples
```

El comando verifica los hashes y descarga únicamente los archivos ausentes desde las fuentes fijadas. Requiere conexión si falta alguno; no genera diagramas ni modifica imágenes existentes con contenido distinto.

La muestra es de conveniencia: nueve ilustraciones comparten estilo y las fuentes públicas podrían haber estado en datos de entrenamiento. Los resultados no representan toda la diversidad de imágenes educativas. Las 18 imágenes con datos están disponibles en un [conjunto complementario](../limitations/README.md) para estudiar limitaciones. Se añaden a estas 20 imágenes y sus métricas se calculan aparte. Los informes originales se conservan como [antecedente histórico](../../docs/historico/evaluacion-inicial/README.md).
