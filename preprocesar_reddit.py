# preprocesar_reddit.py
# Genera archivos simples desde el dataset Pushshift Reddit CSV.
# No usa el modulo csv. Lee el archivo original con una funcion simple que respeta comillas.

ARCHIVO_ORIGINAL = "reddit_dataset.csv"
MAX_POSTS = 2000
MAX_POSTS_POR_USUARIO = 80
SEPARADOR_SALIDA = "|"


def separar_csv(linea):
    campos = []
    campo = ""
    dentro_comillas = False
    i = 0
    while i < len(linea):
        c = linea[i]
        if c == '"':
            if dentro_comillas and i + 1 < len(linea) and linea[i + 1] == '"':
                campo = campo + '"'
                i = i + 1
            else:
                dentro_comillas = not dentro_comillas
        elif c == "," and not dentro_comillas:
            campos.append(campo)
            campo = ""
        else:
            campo = campo + c
        i = i + 1
    campos.append(campo)
    return campos


def limpiar_texto(texto):
    limpio = ""
    i = 0
    while i < len(texto):
        c = texto[i]
        if c == "\n" or c == "\r" or c == "\t":
            limpio = limpio + " "
        elif c == SEPARADOR_SALIDA:
            limpio = limpio + " "
        else:
            limpio = limpio + c
        i = i + 1
    while "  " in limpio:
        limpio = limpio.replace("  ", " ")
    return limpio.strip()


def numero(texto):
    texto = texto.strip()
    if texto == "":
        return 0
    try:
        return int(texto)
    except ValueError:
        return 0


def indice_columna(encabezado, opciones):
    i = 0
    while i < len(encabezado):
        nombre = encabezado[i].strip().lower()
        j = 0
        while j < len(opciones):
            if nombre == opciones[j]:
                return i
            j = j + 1
        i = i + 1
    return -1


def obtener(campos, indice):
    if indice >= 0 and indice < len(campos):
        return campos[indice].strip()
    return ""


def escribir_usuarios(usuarios):
    archivo = open("usuarios.csv", "w", encoding="utf-8")
    archivo.write("user_id|username|karma\n")
    contador = 1
    for username in usuarios:
        archivo.write("u" + str(contador) + SEPARADOR_SALIDA + username + SEPARADOR_SALIDA + str(usuarios[username]) + "\n")
        contador = contador + 1
    archivo.close()


def escribir_posts(posts):
    archivo = open("posts.csv", "w", encoding="utf-8")
    archivo.write("post_id|username|texto|likes\n")
    i = 0
    while i < len(posts):
        post_id = posts[i][0]
        username = posts[i][1]
        texto = posts[i][2]
        score = posts[i][3]
        archivo.write(post_id + SEPARADOR_SALIDA + username + SEPARADOR_SALIDA + texto + SEPARADOR_SALIDA + str(score) + "\n")
        i = i + 1
    archivo.close()


def escribir_relaciones(relaciones):
    archivo = open("relaciones.csv", "w", encoding="utf-8")
    archivo.write("usuario_origen|usuario_contacto\n")
    for clave in relaciones:
        partes = clave.split("->")
        if len(partes) == 2:
            archivo.write(partes[0] + SEPARADOR_SALIDA + partes[1] + "\n")
    archivo.close()


def preprocesar():
    print("Leyendo:", ARCHIVO_ORIGINAL)
    archivo = open(ARCHIVO_ORIGINAL, "r", encoding="utf-8", errors="ignore")

    encabezado = separar_csv(archivo.readline().strip())

    idx_id = indice_columna(encabezado, ["id", "post_id", "comment_id", "submission_id"])
    idx_author = indice_columna(encabezado, ["author", "username", "user"])
    idx_title = indice_columna(encabezado, ["title"])
    idx_selftext = indice_columna(encabezado, ["selftext"])
    idx_body = indice_columna(encabezado, ["body", "text"])
    idx_score = indice_columna(encabezado, ["score", "ups", "like_count"])
    idx_parent = indice_columna(encabezado, ["parent_id"])
    idx_subreddit = indice_columna(encabezado, ["subreddit"])

    if idx_author == -1 or idx_id == -1:
        print("No encontré columnas mínimas id/author. Revisa el encabezado del CSV.")
        archivo.close()
        return

    usuarios = {}
    posts = []
    id_a_autor = {}
    ultimo_autor_por_subreddit = {}
    relaciones = {}
    posts_por_usuario = {}

    linea = archivo.readline()
    while linea != "" and len(posts) < MAX_POSTS:
        campos = separar_csv(linea.strip())

        post_id = obtener(campos, idx_id)
        autor = obtener(campos, idx_author)
        title = obtener(campos, idx_title)
        selftext = obtener(campos, idx_selftext)
        body = obtener(campos, idx_body)
        score = numero(obtener(campos, idx_score))
        parent_id = obtener(campos, idx_parent)
        subreddit = obtener(campos, idx_subreddit)

        if autor != "" and autor != "[deleted]" and post_id != "":
            if autor not in posts_por_usuario:
                posts_por_usuario[autor] = 0
            if posts_por_usuario[autor] < MAX_POSTS_POR_USUARIO:
                texto = title + " " + selftext + " " + body
                texto = limpiar_texto(texto)
                if texto != "" and texto != "[deleted]" and texto != "[removed]":
                    if len(texto) > 350:
                        texto = texto[:350]
                    posts.append((post_id, autor, texto, score))
                    id_a_autor[post_id] = autor
                    posts_por_usuario[autor] = posts_por_usuario[autor] + 1

                    if autor not in usuarios:
                        usuarios[autor] = 0
                    usuarios[autor] = usuarios[autor] + score

                    # Relación real por respuesta si el padre ya fue leído.
                    parent_limpio = parent_id
                    if "_" in parent_limpio:
                        parent_limpio = parent_limpio.split("_")[-1]
                    if parent_limpio in id_a_autor and id_a_autor[parent_limpio] != autor:
                        relaciones[autor + "->" + id_a_autor[parent_limpio]] = True

                    # Alternativa menos fuerte: co-participación dentro del mismo subreddit.
                    if subreddit != "":
                        if subreddit in ultimo_autor_por_subreddit:
                            otro = ultimo_autor_por_subreddit[subreddit]
                            if otro != autor:
                                relaciones[autor + "->" + otro] = True
                        ultimo_autor_por_subreddit[subreddit] = autor

        linea = archivo.readline()

    archivo.close()

    escribir_usuarios(usuarios)
    escribir_posts(posts)
    escribir_relaciones(relaciones)

    print("Usuarios generados:", len(usuarios))
    print("Posts generados:", len(posts))
    print("Relaciones generadas:", len(relaciones))
    print("Listo. Ahora ejecuta: python red_social.py")


if __name__ == "__main__":
    preprocesar()
