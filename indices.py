# indices.py
# Persona 3: stopwords e índices invertidos.

from listas import ListaPosts, ListaUsuarios, ListaTerminos


class FiltroStopwords:
    def __init__(self):
        self.palabras = {}

    def agregar(self, palabra):
        palabra = palabra.strip().lower()
        if palabra != "":
            self.palabras[palabra] = True

    def es_stopword(self, palabra):
        return palabra.lower() in self.palabras

    def total(self):
        return len(self.palabras)

    def limpiar_palabra(self, palabra):
        limpia = ""
        i = 0
        while i < len(palabra):
            c = palabra[i].lower()
            if (c >= "a" and c <= "z") or (c >= "0" and c <= "9") or c == "_":
                limpia = limpia + c
            i = i + 1
        return limpia

    def agregar_si_sirve(self, terminos, palabra):
        palabra = self.limpiar_palabra(palabra)
        if palabra != "" and len(palabra) > 2 and not palabra.isdigit():
            if not self.es_stopword(palabra):
                terminos.insertar(palabra)

    def filtrar_texto(self, texto):
        # Recorre caracter a caracter para que signos como coma o punto
        # separen palabras, en vez de pegarlas.
        terminos = ListaTerminos()
        palabra = ""
        i = 0
        while i < len(texto):
            c = texto[i]
            if c.isalnum() or c == "_":
                palabra = palabra + c
            else:
                self.agregar_si_sirve(terminos, palabra)
                palabra = ""
            i = i + 1
        self.agregar_si_sirve(terminos, palabra)
        return terminos


class IndiceInvertidoPosts:
    def __init__(self):
        self.vocabulario = {}

    def insertar(self, termino, post):
        termino = termino.lower().strip()
        if termino == "":
            return
        if termino not in self.vocabulario:
            self.vocabulario[termino] = ListaPosts()
        self.vocabulario[termino].insertar(post)

    def construir(self, posts, filtro):
        for post_id in posts:
            post = posts[post_id]
            post.terminos = filtro.filtrar_texto(post.texto)
            actual = post.terminos.cabeza
            while actual is not None:
                self.insertar(actual.dato, post)
                actual = actual.siguiente

    def buscar(self, termino):
        termino = termino.lower().strip()
        if termino in self.vocabulario:
            return self.vocabulario[termino]
        return None

    def buscar_varios(self, texto):
        # Búsqueda simple AND: un post debe aparecer en todos los términos.
        palabras = texto.split()
        resultado = ListaPosts()
        primera_lista = None
        cantidad_terminos = 0

        i = 0
        while i < len(palabras):
            termino = palabras[i].lower().strip()
            lista = self.buscar(termino)
            if lista is not None:
                cantidad_terminos = cantidad_terminos + 1
                if primera_lista is None or lista.contar() < primera_lista.contar():
                    primera_lista = lista
            i = i + 1

        if primera_lista is None:
            return resultado

        actual = primera_lista.cabeza
        while actual is not None:
            post = actual.post
            aparece_en_todos = True
            j = 0
            while j < len(palabras):
                termino = palabras[j].lower().strip()
                lista = self.buscar(termino)
                if lista is not None and not lista.contiene_id(post.post_id):
                    aparece_en_todos = False
                j = j + 1
            if aparece_en_todos and cantidad_terminos > 0:
                resultado.insertar(post)
            actual = actual.siguiente
        return resultado

    def total_terminos(self):
        return len(self.vocabulario)


class IndiceInvertidoUsuarios:
    def __init__(self):
        self.mapa = {}

    def registrar_usuario(self, username):
        if username != "" and username not in self.mapa:
            self.mapa[username] = ListaUsuarios()

    def agregar_contacto(self, username, contacto):
        if username == "" or contacto == "" or username == contacto:
            return
        self.registrar_usuario(username)
        self.mapa[username].insertar(contacto)

    def obtener_contactos(self, username):
        if username in self.mapa:
            return self.mapa[username]
        return None

    def total_usuarios(self):
        return len(self.mapa)
