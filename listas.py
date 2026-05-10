# listas.py
# Persona 2: nodos y listas enlazadas hechas a mano.

class NodoStr:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class NodoPost:
    def __init__(self, post):
        self.post = post
        self.siguiente = None


class NodoUsuario:
    def __init__(self, username):
        self.username = username
        self.siguiente = None


class NodoLike:
    def __init__(self, username):
        self.username = username
        self.siguiente = None


class ListaTerminos:
    def __init__(self):
        self.cabeza = None
        self.tamanio = 0

    def insertar(self, termino):
        if termino == "" or self.contiene(termino):
            return
        nuevo = NodoStr(termino)
        nuevo.siguiente = self.cabeza
        self.cabeza = nuevo
        self.tamanio = self.tamanio + 1

    def contiene(self, termino):
        actual = self.cabeza
        while actual is not None:
            if actual.dato == termino:
                return True
            actual = actual.siguiente
        return False

    def recorrer(self):
        datos = []
        actual = self.cabeza
        while actual is not None:
            datos.append(actual.dato)
            actual = actual.siguiente
        return datos

    def contar(self):
        return self.tamanio


class ListaPosts:
    def __init__(self):
        self.cabeza = None
        self.tamanio = 0

    def insertar(self, post):
        if post is None or self.contiene_id(post.post_id):
            return
        nuevo = NodoPost(post)
        nuevo.siguiente = self.cabeza
        self.cabeza = nuevo
        self.tamanio = self.tamanio + 1

    def contiene_id(self, post_id):
        actual = self.cabeza
        while actual is not None:
            if actual.post.post_id == post_id:
                return True
            actual = actual.siguiente
        return False

    def recorrer(self):
        datos = []
        actual = self.cabeza
        while actual is not None:
            datos.append(actual.post)
            actual = actual.siguiente
        return datos

    def contar(self):
        return self.tamanio


class ListaUsuarios:
    def __init__(self):
        self.cabeza = None
        self.tamanio = 0

    def insertar(self, username):
        if username == "" or self.contiene(username):
            return
        nuevo = NodoUsuario(username)
        nuevo.siguiente = self.cabeza
        self.cabeza = nuevo
        self.tamanio = self.tamanio + 1

    def contiene(self, username):
        actual = self.cabeza
        while actual is not None:
            if actual.username == username:
                return True
            actual = actual.siguiente
        return False

    def recorrer(self):
        datos = []
        actual = self.cabeza
        while actual is not None:
            datos.append(actual.username)
            actual = actual.siguiente
        return datos

    def contar(self):
        return self.tamanio


class ListaLikes:
    # El dataset tiene score total, no usuarios reales que votaron.
    # Se limita para no crear miles de nodos por un post muy popular.
    MAX_LIKES = 30

    def __init__(self):
        self.cabeza = None
        self.tamanio = 0

    def insertar(self, username):
        if username == "" or self.contiene(username):
            return
        if self.tamanio >= ListaLikes.MAX_LIKES:
            return
        nuevo = NodoLike(username)
        nuevo.siguiente = self.cabeza
        self.cabeza = nuevo
        self.tamanio = self.tamanio + 1

    def contiene(self, username):
        actual = self.cabeza
        while actual is not None:
            if actual.username == username:
                return True
            actual = actual.siguiente
        return False

    def recorrer(self):
        datos = []
        actual = self.cabeza
        while actual is not None:
            datos.append(actual.username)
            actual = actual.siguiente
        return datos

    def contar(self):
        return self.tamanio
