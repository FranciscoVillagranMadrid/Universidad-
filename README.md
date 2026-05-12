# Proyecto de Red Social con Índice Invertido

Proyecto de Estructuras de Datos hecho en Python. La idea es cargar datos de Reddit, guardar usuarios, posts y relaciones en memoria, y después buscar información usando índices invertidos.

## Dataset

Se usa como base el dataset:

The Pushshift Reddit Dataset - CSV  
https://www.kaggle.com/datasets/jaymetosineto/the-pushshift-reddit-dataset-csv

Reddit sirve para este trabajo porque tiene usuarios, publicaciones/comentarios, texto y score. La parte que no viene igual a la pauta son los contactos, porque Reddit no maneja amigos como Facebook. Por eso se toman como contactos las interacciones o co-participaciones entre usuarios.

## Cómo se pasó Reddit a la pauta

- Usuario: autor del post o comentario.
- Post: publicación o comentario de Reddit.
- Texto: title, selftext o body, según lo que traiga el CSV.
- Likes: se usa el score como aproximación.
- Contactos: se generan desde respuestas o participación en el mismo contexto.
- Índice de posts: palabra -> lista enlazada de posts.
- Índice de usuarios: usuario -> lista enlazada de contactos.

No se dice que los contactos sean amigos reales. Son relaciones usadas para representar interacción entre usuarios, que es lo más cercano que entrega Reddit para esta pauta.

## Archivos

```text
red_social.py          carga los archivos y ejecuta el programa
listas.py              nodos y listas enlazadas
indices.py             stopwords e índices invertidos
preprocesar_reddit.py  genera usuarios.csv, posts.csv y relaciones.csv
usuarios.csv           user_id|username|karma
posts.csv              post_id|username|texto|likes
relaciones.csv         usuario_origen|usuario_contacto
stopwords.txt          palabras que no se indexan
```

Los archivos finales usan `|` como separador. Se hizo así porque los textos de Reddit pueden traer comas y eso complica la lectura si se separa por coma.

## Cómo ejecutar

Con los CSV incluidos:

```bash
python red_social.py
```

Para generar los CSV desde el dataset descargado:

1. Descargar el CSV desde Kaggle.
2. Dejarlo en la misma carpeta del proyecto.
3. Cambiar en `preprocesar_reddit.py` el nombre:

```python
ARCHIVO_ORIGINAL = "reddit_dataset.csv"
```

4. Ejecutar:

```bash
python preprocesar_reddit.py
python red_social.py
```

## Estructuras usadas

En `listas.py` están las listas enlazadas hechas a mano:

- `ListaTerminos`
- `ListaPosts`
- `ListaUsuarios`
- `ListaLikes`

Cada una guarda su `cabeza` y su `tamanio`. Los datos se enlazan con nodos, no con listas Python internas.

Los métodos `recorrer()` devuelven una lista Python solamente para imprimir o mostrar resultados. La estructura guardada sigue siendo la lista enlazada.

## Índices invertidos

En `indices.py` hay dos índices principales:

```text
termino -> ListaPosts
usuario -> ListaUsuarios
```

El diccionario se usa como mapa principal, y el valor asociado a cada clave es una lista enlazada hecha por nosotros.

## División de trabajo

- Persona 1: `red_social.py`, carga de archivos y pruebas.
- Persona 2: `listas.py`, nodos y listas enlazadas.
- Persona 3: `indices.py`, stopwords e índices invertidos.

## Detalles importantes para explicar

- Reddit entrega score, pero no entrega quién votó. Por eso los likes son simbólicos: `like_1`, `like_2`, etc. Se limita a 30 para no crear demasiados nodos por post.
- Los contactos no son amigos reales de Reddit. Se generan como interacción o co-participación.
- Los CSV que vienen en la carpeta son una muestra para probar rápido. Para usar más datos se ejecuta `preprocesar_reddit.py` con el CSV real descargado.

## Ejemplo de salida

```text
Resumen de carga
Usuarios cargados: 30
Posts cargados: 50
Relaciones cargadas: 60
Stopwords cargadas: 111
Términos indexados: 304

Búsqueda de posts por término: python
- Post(...)

Contactos de usuario: spez
- qgyh2
- karmanaut
```

## Para la defensa

La parte central es explicar que el índice permite no recorrer todos los posts cada vez. Al construirlo una vez, cada palabra queda apuntando a una lista enlazada con los posts donde aparece. Lo mismo pasa con los usuarios: cada usuario apunta a una lista enlazada de contactos.
