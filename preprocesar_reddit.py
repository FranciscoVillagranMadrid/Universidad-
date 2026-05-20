# preprocesar_reddit.py

#este archivo toma el dataset original de reddit y genera los csv que usa red_social.py
#no es el sistema principal, solo prepara los datos para usuarios, posts y relaciones

#archivo original del dataset de reddit
ARCHIVO_ORIGINAL = "reddit_dataset.csv"

#cantidad maxima de posts que se van a procesar
MAX_POSTS = 2000

#cantidad maxima de posts que se guardan por usuario para no cargar demasiado un solo usuario
MAX_POSTS_POR_USUARIO = 80

#separador que se usara en los archivos csv generados
SEPARADOR_SALIDA = "|"


#funcion que separa una linea csv respetando las comillas
def separar_csv(linea):
    campos = [] #lista donde se guardan los campos separados
    campo = "" #campo temporal que se va armando caracter por caracter
    dentro_comillas = False #indica si el recorrido esta dentro de comillas
    i = 0 #indice para recorrer la linea

    while i < len(linea): #mientras no termine de recorrer la linea
        c = linea[i] #guarda el caracter actual

        if c == '"': #si encuentra comillas
            if dentro_comillas and i + 1 < len(linea) and linea[i + 1] == '"': #si hay doble comilla dentro de un texto
                campo = campo + '"' #agrega una comilla al campo
                i = i + 1 #salta la siguiente comilla
            else:
                dentro_comillas = not dentro_comillas #cambia el estado de dentro o fuera de comillas

        elif c == "," and not dentro_comillas: #si encuentra coma fuera de comillas separa el campo
            campos.append(campo) #agrega el campo a la lista
            campo = "" #reinicia el campo para guardar el siguiente

        else:
            campo = campo + c #agrega el caracter actual al campo

        i = i + 1 #avanza al siguiente caracter

    campos.append(campo) #agrega el ultimo campo de la linea
    return campos #retorna la lista con los campos separados


#funcion que limpia el texto para que se pueda guardar bien en el csv
def limpiar_texto(texto):
    limpio = "" #variable donde se arma el texto limpio
    i = 0 #indice para recorrer el texto

    while i < len(texto): #mientras no termine de recorrer el texto
        c = texto[i] #guarda el caracter actual

        if c == "\n" or c == "\r" or c == "\t": #si hay saltos de linea o tabulaciones
            limpio = limpio + " " #los cambia por espacio

        elif c == SEPARADOR_SALIDA: #si aparece el separador que usamos en los csv
            limpio = limpio + " " #lo cambia por espacio para no romper el archivo

        else:
            limpio = limpio + c #si no hay problema agrega el caracter normal

        i = i + 1 #avanza al siguiente caracter

    while "  " in limpio: #mientras existan espacios dobles
        limpio = limpio.replace("  ", " ") #los reemplaza por un solo espacio

    return limpio.strip() #retorna el texto sin espacios al inicio ni al final


#funcion que transforma texto a numero entero
def numero(texto):
    texto = texto.strip() #quita espacios al inicio y al final
    if texto == "": #si el texto esta vacio retorna 0
        return 0
    try:
        return int(texto) #intenta convertir el texto a numero
    except ValueError:
        return 0 #si no se puede convertir retorna 0


#funcion que busca el indice de una columna dentro del encabezado
def indice_columna(encabezado, opciones):
    i = 0 #indice para recorrer el encabezado

    while i < len(encabezado): #mientras queden columnas por revisar
        nombre = encabezado[i].strip().lower() #limpia el nombre de la columna
        j = 0 #indice para recorrer las opciones posibles

        while j < len(opciones): #mientras queden opciones por comparar
            if nombre == opciones[j]: #si el nombre de la columna coincide con una opcion
                return i #retorna la posicion de esa columna
            j = j + 1 #avanza a la siguiente opcion

        i = i + 1 #avanza a la siguiente columna

    return -1 #si no encuentra la columna retorna -1


#funcion que obtiene un campo segun su indice
def obtener(campos, indice):
    if indice >= 0 and indice < len(campos): #si el indice existe dentro de la lista de campos
        return campos[indice].strip() #retorna el campo limpio
    return "" #si no existe retorna texto vacio


#funcion que escribe el archivo usuarios.csv
def escribir_usuarios(usuarios):
    archivo = open("usuarios.csv", "w", encoding="utf-8") #crea el archivo de usuarios
    archivo.write("user_id|username|karma\n") #escribe el encabezado del archivo
    contador = 1 #contador para crear ids simples de usuario

    for username in usuarios: #recorre cada usuario guardado
        archivo.write("u" + str(contador) + SEPARADOR_SALIDA + username + SEPARADOR_SALIDA + str(usuarios[username]) + "\n") #escribe id, username y karma
        contador = contador + 1 #avanza al siguiente id

    archivo.close() #cierra el archivo


#funcion que escribe el archivo posts.csv
def escribir_posts(posts):
    archivo = open("posts.csv", "w", encoding="utf-8") #crea el archivo de posts
    archivo.write("post_id|username|texto|score\n") #escribe el encabezado del archivo
    i = 0 #indice para recorrer los posts

    while i < len(posts): #mientras queden posts por escribir
        post_id = posts[i][0] #obtiene el id del post
        username = posts[i][1] #obtiene el usuario que hizo el post
        texto = posts[i][2] #obtiene el texto del post
        score = posts[i][3] #obtiene el score del post

        archivo.write(post_id + SEPARADOR_SALIDA + username + SEPARADOR_SALIDA + texto + SEPARADOR_SALIDA + str(score) + "\n") #escribe el post en el csv
        i = i + 1 #avanza al siguiente post

    archivo.close() #cierra el archivo


#funcion que escribe el archivo relaciones.csv
def escribir_relaciones(relaciones):
    archivo = open("relaciones.csv", "w", encoding="utf-8") #crea el archivo de relaciones
    archivo.write("usuario_origen|usuario_contacto\n") #escribe el encabezado del archivo

    for clave in relaciones: #recorre las relaciones guardadas
        partes = clave.split("->") #separa origen y contacto usando el simbolo ->
        if len(partes) == 2: #si la relacion tiene origen y contacto
            archivo.write(partes[0] + SEPARADOR_SALIDA + partes[1] + "\n") #escribe la relacion en el csv

    archivo.close() #cierra el archivo


#funcion principal que preprocesa el dataset original
def preprocesar():
    print("Leyendo:", ARCHIVO_ORIGINAL) #muestra que archivo se esta leyendo
    archivo = open(ARCHIVO_ORIGINAL, "r", encoding="utf-8", errors="ignore") #abre el dataset original ignorando errores de lectura

    encabezado = separar_csv(archivo.readline().strip()) #lee el encabezado y separa sus columnas

    #busca las posiciones de las columnas importantes dentro del csv original
    idx_id = indice_columna(encabezado, ["id", "post_id", "comment_id", "submission_id"])
    idx_author = indice_columna(encabezado, ["author", "username", "user"])
    idx_title = indice_columna(encabezado, ["title"])
    idx_selftext = indice_columna(encabezado, ["selftext"])
    idx_body = indice_columna(encabezado, ["body", "text"])
    idx_score = indice_columna(encabezado, ["score", "ups", "like_count"])
    idx_parent = indice_columna(encabezado, ["parent_id"])
    idx_subreddit = indice_columna(encabezado, ["subreddit"])

    if idx_author == -1 or idx_id == -1: #si no encuentra columnas minimas para trabajar
        print("No encontré columnas mínimas id/author. Revisa el encabezado del CSV.")
        archivo.close() #cierra el archivo
        return #termina la funcion

    usuarios = {} #diccionario donde se guarda username y karma acumulado
    posts = [] #lista donde se guardan los posts procesados
    id_a_autor = {} #diccionario que relaciona id de post con su autor
    ultimo_autor_por_subreddit = {} #guarda el ultimo autor visto por subreddit
    relaciones = {} #diccionario donde se guardan relaciones entre usuarios
    posts_por_usuario = {} #diccionario para contar cuantos posts lleva cada usuario

    linea = archivo.readline() #lee la primera linea con datos

    while linea != "" and len(posts) < MAX_POSTS: #mientras no termine el archivo y no supere el maximo de posts
        campos = separar_csv(linea.strip()) #separa los campos de la linea actual

        post_id = obtener(campos, idx_id) #obtiene el id del post
        autor = obtener(campos, idx_author) #obtiene el autor del post
        title = obtener(campos, idx_title) #obtiene el titulo si existe
        selftext = obtener(campos, idx_selftext) #obtiene el texto del post si existe
        body = obtener(campos, idx_body) #obtiene el cuerpo del comentario si existe
        score = numero(obtener(campos, idx_score)) #obtiene el score como numero
        parent_id = obtener(campos, idx_parent) #obtiene el id del padre si es respuesta
        subreddit = obtener(campos, idx_subreddit) #obtiene el subreddit

        if autor != "" and autor != "[deleted]" and post_id != "": #si el autor y el post son validos
            if autor not in posts_por_usuario: #si el autor no tiene contador de posts
                posts_por_usuario[autor] = 0 #inicia su contador en 0

            if posts_por_usuario[autor] < MAX_POSTS_POR_USUARIO: #si el usuario no supera el maximo de posts permitidos
                texto = title + " " + selftext + " " + body #junta titulo, texto y cuerpo en un solo texto
                texto = limpiar_texto(texto) #limpia el texto antes de guardarlo

                if texto != "" and texto != "[deleted]" and texto != "[removed]": #si el texto es valido
                    if len(texto) > 350: #si el texto es muy largo
                        texto = texto[:350] #lo corta para dejarlo mas corto

                    posts.append((post_id, autor, texto, score)) #guarda el post procesado
                    id_a_autor[post_id] = autor #relaciona el id del post con su autor
                    posts_por_usuario[autor] = posts_por_usuario[autor] + 1 #aumenta el contador de posts del usuario

                    if autor not in usuarios: #si el usuario no estaba registrado
                        usuarios[autor] = 0 #lo agrega con karma inicial 0

                    usuarios[autor] = usuarios[autor] + score #suma el score del post al karma del usuario

                    #crea una relacion real si el post responde a otro post ya leido
                    parent_limpio = parent_id #guarda el id padre
                    if "_" in parent_limpio: #si el id padre viene con prefijo
                        parent_limpio = parent_limpio.split("_")[-1] #deja solo la parte final del id

                    if parent_limpio in id_a_autor and id_a_autor[parent_limpio] != autor: #si el padre existe y es de otro autor
                        relaciones[autor + "->" + id_a_autor[parent_limpio]] = True #guarda una relacion entre ambos usuarios

                    #crea una relacion alternativa si usuarios participan en el mismo subreddit
                    if subreddit != "": #si el subreddit existe
                        if subreddit in ultimo_autor_por_subreddit: #si ya habia un autor anterior en ese subreddit
                            otro = ultimo_autor_por_subreddit[subreddit] #obtiene el ultimo autor de ese subreddit
                            if otro != autor: #si el ultimo autor no es el mismo
                                relaciones[autor + "->" + otro] = True #crea una relacion por co-participacion

                        ultimo_autor_por_subreddit[subreddit] = autor #actualiza el ultimo autor visto en ese subreddit

        linea = archivo.readline() #lee la siguiente linea del dataset

    archivo.close() #cierra el archivo original

    escribir_usuarios(usuarios) #genera usuarios.csv
    escribir_posts(posts) #genera posts.csv
    escribir_relaciones(relaciones) #genera relaciones.csv

    print("Usuarios generados:", len(usuarios)) #muestra cantidad de usuarios generados
    print("Posts generados:", len(posts)) #muestra cantidad de posts generados
    print("Relaciones generadas:", len(relaciones)) #muestra cantidad de relaciones generadas
    print("Listo. Ahora ejecuta: python red_social.py") #indica el siguiente paso


#ejecuta el preprocesamiento si este archivo se corre directamente
if __name__ == "__main__":
    preprocesar()