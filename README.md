# Sistema de Red Social con Índice Invertido

Proyecto semestral de la asignatura **Estructuras de Datos**.

El trabajo consiste en modelar una red social en memoria, cargando usuarios, publicaciones y relaciones entre usuarios. A partir de esos datos se construyen índices invertidos para realizar búsquedas de publicaciones por términos y búsquedas de contactos por usuario.

El proyecto fue desarrollado en **Python**, usando clases, nodos y listas enlazadas propias, de acuerdo con los contenidos vistos en la asignatura.

---

## Dataset utilizado

El dataset usado corresponde a datos de Reddit obtenidos desde Kaggle:

**The Pushshift Reddit Dataset - CSV**  
https://www.kaggle.com/datasets/jaymetosineto/the-pushshift-reddit-dataset-csv

Reddit se utilizó como red social base porque contiene usuarios, publicaciones, comentarios y métricas de interacción. Como Reddit no maneja una lista de amigos explícita como otras redes sociales, las relaciones entre usuarios se modelaron a partir de interacciones o co-participación dentro de la plataforma.

Para trabajar de forma más simple con los datos, se generaron archivos CSV finales con la información necesaria para el sistema.

---

## Archivos del proyecto

```text
red_social.py
listas.py
indices.py
preprocesar_reddit.py
usuarios.csv
posts.csv
relaciones.csv
stopwords.txt
README.md
```

### `red_social.py`

Archivo principal del programa. Se encarga de cargar los datos, crear los usuarios y posts, cargar relaciones, construir los índices y ejecutar pruebas básicas.

### `listas.py`

Contiene las listas enlazadas implementadas manualmente. Estas listas se usan para guardar términos, posts, usuarios/contactos y likes.

### `indices.py`

Contiene el filtro de stopwords y los índices invertidos del sistema:

- índice de posts;
- índice de usuarios/contactos.

### `preprocesar_reddit.py`

Archivo usado para preparar los datos del dataset original y generar archivos más simples para el proyecto.

### Archivos CSV

- `usuarios.csv`: usuarios cargados en el sistema.
- `posts.csv`: publicaciones o comentarios usados como posts.
- `relaciones.csv`: relaciones entre usuarios.
- `stopwords.txt`: palabras que se ignoran al construir el índice.

---

## Adaptación del dataset

La pauta pide trabajar con usuarios, posts, likes, contactos e índices invertidos. En el proyecto se usó la siguiente adaptación:

| Elemento solicitado | Representación usada |
|---|---|
| Usuario | Usuario de Reddit |
| Post | Publicación o comentario |
| Texto del post | Texto asociado al post/comentario |
| Likes | Score del post |
| Contactos | Interacciones o co-participación entre usuarios |
| Índice de posts | Término → lista enlazada de posts |
| Índice de usuarios | Usuario → lista enlazada de contactos |

Esta adaptación se hizo porque el dataset no entrega todos los datos exactamente en el mismo formato de la pauta, pero sí permite representar una red social de manera coherente.

---

## Cómo ejecutar

Para ejecutar el proyecto:

```bash
python red_social.py
```

Los archivos `.csv` y `stopwords.txt` deben estar en la misma carpeta que los archivos `.py`.

Al ejecutar, el programa muestra una prueba básica con la cantidad de usuarios, posts, relaciones, stopwords y términos indexados. También muestra ejemplos de búsqueda de posts y contactos.

---

## Estructuras utilizadas

El proyecto utiliza listas enlazadas propias para almacenar los datos asociados a los índices.

Los diccionarios se utilizan como mapas principales para acceder rápido a usuarios, posts y entradas del índice. Cada entrada del índice apunta a una lista enlazada implementada manualmente.

Ejemplo general del índice de posts:

```text
python -> Post 1 -> Post 2 -> Post 3
```

Ejemplo general del índice de usuarios:

```text
usuario1 -> usuario2 -> usuario3 -> usuario4
```

---

## Funcionamiento general

El flujo principal del sistema es:

1. Cargar stopwords.
2. Cargar usuarios.
3. Cargar posts.
4. Cargar relaciones entre usuarios.
5. Construir el índice invertido de posts.
6. Construir el índice invertido de usuarios.
7. Realizar búsquedas.

Este orden permite que los posts tengan autores válidos y que las relaciones se creen solo entre usuarios existentes.

---

## División del trabajo

El proyecto se organizó en tres partes principales:

### Persona 1: Carga de datos y sistema principal

Encargada de la carga de archivos, creación de usuarios y posts, carga de relaciones y ejecución del sistema.

### Persona 2: Listas enlazadas

Encargada de implementar los nodos y listas enlazadas usadas en el proyecto.

### Persona 3: Índices y filtros

Encargada de implementar el índice invertido de posts, el índice de usuarios/contactos y el filtro de stopwords.

---

## Consideraciones

- Reddit no tiene amigos explícitos, por lo que los contactos se modelaron como interacciones.
- El score del dataset se usa como base para representar likes.
- Los archivos incluidos permiten probar el funcionamiento del sistema.
- Si se desea trabajar con más datos, se puede usar el preprocesador sobre el dataset original.
- El proyecto evita librerías externas y mantiene la lógica principal con estructuras implementadas manualmente.

---

## Conclusión

El sistema permite representar una red social en memoria usando estructuras de datos lineales e índices invertidos. La implementación permite buscar publicaciones por términos y consultar contactos de usuarios, manteniendo el uso de listas enlazadas propias como parte central del trabajo.
