# Sistema de Red Social Reddit con Índice Invertido

Proyecto semestral de **Estructuras de Datos**. La idea es cargar datos de Reddit, guardarlos en memoria y permitir búsquedas usando índices invertidos.

## Dataset usado

Dataset base: **The Pushshift Reddit Dataset - CSV**  
Link: https://www.kaggle.com/datasets/jaymetosineto/the-pushshift-reddit-dataset-csv

El dataset tiene publicaciones y comentarios de Reddit. Para el proyecto se usan datos como autor, texto y score.

## Cómo se adapta Reddit a la pauta

| Pauta | En este proyecto |
|---|---|
| Usuarios | autores de Reddit (`author`) |
| Posts | publicaciones o comentarios |
| Texto del post | `title`, `selftext` o `body` |
| Likes | `score` del post/comentario |
| Contactos | relaciones por respuesta o co-participación |
| Índice de posts | palabra -> lista enlazada de posts |
| Índice de usuarios | usuario -> lista enlazada de contactos |

Reddit no tiene amigos declarados como Facebook. Por eso los contactos se modelan como interacción: si un usuario responde a otro, o si dos usuarios participan en el mismo contexto, se registra una relación. Eso queda generado en `relaciones.csv`.

## Archivos

```text
red_social.py          sistema principal y carga de archivos
listas.py              nodos y listas enlazadas propias
indices.py             filtro de stopwords e índices invertidos
preprocesar_reddit.py  genera CSV simples desde el dataset original
usuarios.csv           usuarios: user_id|username|karma
posts.csv              posts: post_id|username|texto|likes
relaciones.csv         relaciones: usuario_origen|usuario_contacto
stopwords.txt          palabras a ignorar
```

Los CSV finales usan separador `|` para evitar problemas con comas dentro de los textos de Reddit.

## Cómo ejecutar

Con los archivos ya generados:

```bash
python red_social.py
```

Para generar los CSV desde el dataset original:

1. Descargar el dataset de Kaggle.
2. Copiar el CSV original en esta carpeta.
3. Cambiar en `preprocesar_reddit.py` la variable:

```python
ARCHIVO_ORIGINAL = "reddit_dataset.csv"
```

4. Ejecutar:

```bash
python preprocesar_reddit.py
python red_social.py
```

## Estructuras implementadas

### Listas enlazadas propias

En `listas.py`:

- `ListaTerminos`
- `ListaPosts`
- `ListaUsuarios`
- `ListaLikes`

Cada lista usa nodos propios y mantiene su tamaño con `tamanio`. No se usan listas Python como estructura interna de estas listas. Los métodos `recorrer()` devuelven una lista Python solo para mostrar resultados en pantalla, no para guardar la estructura.

### Índices invertidos

En `indices.py`:

```text
termino -> ListaPosts
usuario -> ListaUsuarios
```

El diccionario se usa solo como mapa principal del índice. Los valores del diccionario son listas enlazadas propias.

## División de trabajo

**Persona 1:** `red_social.py`  
Carga archivos, crea usuarios/posts, carga relaciones y ejecuta pruebas.

**Persona 2:** `listas.py`  
Implementa nodos y listas enlazadas.

**Persona 3:** `indices.py`  
Implementa stopwords, índice de posts e índice de usuarios.

## Limitaciones honestas

- El dataset entrega `score`, pero no la identidad de cada usuario que votó. Por eso los likes se representan como `like_1`, `like_2`, etc., con un límite de 30 por post.
- Los contactos no son amistades explícitas. Son relaciones derivadas desde respuestas o co-participación.
- Los CSV incluidos son una muestra para probar el programa. Para la entrega definitiva se debe generar una muestra desde el CSV real descargado desde Kaggle usando `preprocesar_reddit.py`.

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

## Nota para la defensa

Explicar que Reddit sí entrega usuarios, posts, texto y score. Lo que no entrega como amistad directa se modeló como interacción entre usuarios. La estructura importante del proyecto no son esos contactos como dato social perfecto, sino cómo se cargan y se representan mediante listas enlazadas e índices invertidos.
