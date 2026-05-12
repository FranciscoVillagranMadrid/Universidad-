# indice.py
# Construye tres índices invertidos:
#   1. subreddit → posts   (buscar posts de un subreddit)
#   2. username  → posts   (buscar posts de un autor)
#   3. username  → relaciones salientes (buscar con quién interactuó)

from cargar import ListaEnlazada
from stopwords import filtrar


class IndiceInvertido:
    """
    dict de Python (mapa/diccionario) cuyas claves son strings
    y cuyos valores son ListaEnlazada implementadas por nosotros.

        clave (str)  →  ListaEnlazada<T>
    """

    def __init__(self):
        self._mapa = {}

    def insertar(self, clave: str, dato):
        """Agrega 'dato' a la posting list de 'clave'. Crea la lista si no existe."""
        if clave not in self._mapa:
            self._mapa[clave] = ListaEnlazada()
        self._mapa[clave].insertar(dato)

    def buscar(self, clave: str):
        """Devuelve ListaEnlazada de 'clave', o None si no existe."""
        return self._mapa.get(clave, None)

    def eliminar(self, clave: str) -> bool:
        """Elimina la clave y su posting list completa. Devuelve True si existía."""
        if clave in self._mapa:
            del self._mapa[clave]
            return True
        return False

    def total_claves(self) -> int:
        return len(self._mapa)

    def __repr__(self):
        return f"IndiceInvertido({self.total_claves()} claves)"


# ── Constructores de índices ─────────────────────────────────────────

def construir_indice_subreddits(posts: list, stopwords: set) -> IndiceInvertido:
    """
    Índice: subreddit → posts que pertenecen a ese subreddit.
    El subreddit se trata como término (se filtra stopwords por si acaso).
    """
    indice = IndiceInvertido()
    for post in posts:
        terminos = filtrar([post.subreddit.lower()], stopwords)
        for t in terminos:
            indice.insertar(t, post)
    print(f"[indice] Subreddits indexados  : {indice.total_claves()}")
    return indice


def construir_indice_autores(posts: list) -> IndiceInvertido:
    """
    Índice: username → posts publicados por ese usuario.
    """
    indice = IndiceInvertido()
    for post in posts:
        indice.insertar(post.autor.username, post)
    print(f"[indice] Autores indexados     : {indice.total_claves()}")
    return indice


def construir_indice_relaciones(relaciones: list) -> IndiceInvertido:
    """
    Índice: username → relaciones (Relacion) donde ese usuario es el ORIGEN.
    Permite consultar rápidamente con quién interactuó un usuario.
    """
    indice = IndiceInvertido()
    for rel in relaciones:
        indice.insertar(rel.origen.username, rel)
    print(f"[indice] Usuarios con relaciones: {indice.total_claves()}")
    return indice
