# Sistema de Red Social con Índice Invertido

Proyecto semestral desarrollado para la asignatura **Estructuras de Datos**.

El objetivo del proyecto es implementar una base simple de una red social utilizando datos provenientes de Reddit, aplicando estructuras de datos vistas en clases, principalmente **listas enlazadas** e **índices invertidos**.

El sistema permite cargar usuarios, publicaciones y relaciones entre usuarios desde archivos CSV, construir índices en memoria y realizar búsquedas de publicaciones por término y de contactos por usuario.

---

## Dataset utilizado

El dataset utilizado corresponde a:

**The Pushshift Reddit Dataset - CSV**  
https://www.kaggle.com/datasets/jaymetosineto/the-pushshift-reddit-dataset-csv

El dataset original fue preprocesado para generar archivos más simples y manejables para el proyecto:

- `usuarios.csv`
- `posts.csv`
- `relaciones.csv`

Estos archivos son los que utiliza directamente el sistema principal.

---

## Estructura del proyecto

```text
listas.py
indices.py
red_social.py
preprocesar_reddit.py
usuarios.csv
posts.csv
relaciones.csv
stopwords.txt
README.md