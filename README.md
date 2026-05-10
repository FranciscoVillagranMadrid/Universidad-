# Sistema de Red Social con Índice Invertido

Proyecto semestral de la asignatura **Estructuras de Datos**.

Este proyecto implementa un sistema simple de red social usando datos de Reddit. La idea principal es cargar usuarios, publicaciones y relaciones entre usuarios para luego permitir búsquedas usando un índice invertido.

El sistema trabaja todo en memoria y utiliza listas enlazadas implementadas manualmente para guardar los resultados asociados a cada índice.

## Dataset utilizado

El dataset usado es:

**The Pushshift Reddit Dataset - CSV**  
https://www.kaggle.com/datasets/jaymetosineto/the-pushshift-reddit-dataset-csv

Este dataset contiene información basada en Reddit, como publicaciones, comentarios, usuarios y datos de interacción. Para este proyecto los datos fueron preprocesados y convertidos a archivos más simples para facilitar la carga desde Python.

## Archivos principales

```text
red_social.py
listas.py
indices.py
preprocesar_reddit.py
usuarios.csv
posts.csv
relaciones.csv
stopwords.txt
```

## Descripción general

El proyecto carga la información desde archivos CSV y construye dos tipos de índices:

- Un índice invertido de publicaciones, donde cada término apunta a una lista de posts que contienen esa palabra.
- Un índice de usuarios, donde cada usuario apunta a una lista de contactos relacionados.

Como Reddit no maneja una lista de amigos explícita como otras redes sociales, las relaciones entre usuarios se modelan a partir de interacciones o participación dentro del mismo contexto.

## Cómo ejecutar

Para correr el proyecto, se debe ejecutar:

```bash
python red_social.py
```

Los archivos CSV y `stopwords.txt` deben estar en la misma carpeta que el código.

## Funcionamiento básico

Al ejecutar el programa, se cargan:

- usuarios;
- publicaciones;
- relaciones entre usuarios;
- stopwords;
- índices de búsqueda.

Luego se muestran pruebas simples, como buscar publicaciones por una palabra y consultar los contactos de un usuario.

## Nota sobre el dataset

Los archivos CSV incluidos son una versión simplificada para probar el funcionamiento del programa. Si se quiere trabajar con más datos, se puede usar el archivo `preprocesar_reddit.py` para generar nuevos CSV a partir del dataset original descargado desde Kaggle.
