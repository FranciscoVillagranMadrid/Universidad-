# cargar.py
# Lee los tres CSV del dataset Pushshift Reddit:
#   - submission.csv      → posts   (post_id, author, subreddit, score)
#   - user.csv            → usuarios conocidos (username)
#   - user_relations.csv  → relaciones (source_author, target_author,
#                                       sentiment_sum, interaction_count)

import csv

# ════════════════════════════════════════════════════════════════════
#  ESTRUCTURAS BASE: Nodo y ListaEnlazada
# ════════════════════════════════════════════════════════════════════

class Nodo:
    """Unidad básica de la lista enlazada."""
    def __init__(self, dato):
        self.dato      = dato
        self.siguiente = None


class ListaEnlazada:
    """Lista enlazada simple implementada manualmente."""

    def __init__(self):
        self.cabeza  = None
        self.tamanio = 0

    def insertar(self, dato):
        """Inserta al final. No duplica (compara por id si existe, si no por ==)."""
        if self._existe(dato):
            return
        nuevo = Nodo(dato)
        if self.cabeza is None:
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo
        self.tamanio += 1

    def _existe(self, dato) -> bool:
        actual = self.cabeza
        while actual:
            a, b = actual.dato, dato
            if hasattr(a, 'id') and hasattr(b, 'id'):
                if a.id == b.id:
                    return True
            elif a == b:
                return True
            actual = actual.siguiente
        return False

    def __len__(self):
        return self.tamanio

    def __repr__(self):
        partes, actual = [], self.cabeza
        while actual:
            partes.append(str(actual.dato))
            actual = actual.siguiente
        return " -> ".join(partes)


# ════════════════════════════════════════════════════════════════════
#  MODELOS
# ════════════════════════════════════════════════════════════════════

class Usuario:
    """Perfil de usuario de Reddit."""

    def __init__(self, username: str):
        self.username   = username
        self.relaciones = ListaEnlazada()   # lista de objetos Relacion

    def __eq__(self, otro):
        return isinstance(otro, Usuario) and self.username == otro.username

    def __repr__(self):
        return f"@{self.username}"


class Post:
    """
    Publicación de Reddit.
    Campos disponibles en Pushshift: post_id, author, subreddit, score.
    El campo 'texto' para indexar es el subreddit (no hay título/cuerpo).
    """

    def __init__(self, post_id: str, autor: Usuario, subreddit: str, score: int):
        self.id        = post_id
        self.autor     = autor
        self.subreddit = subreddit
        self.score     = score
        self.texto     = subreddit   # campo que se indexa por términos

    def __eq__(self, otro):
        return isinstance(otro, Post) and self.id == otro.id

    def __repr__(self):
        return f"Post(id={self.id}, autor={self.autor}, r/{self.subreddit}, score={self.score})"


class Relacion:
    """Relación dirigida entre dos usuarios."""

    def __init__(self, origen: Usuario, destino: Usuario,
                 sentiment: float, interacciones: int):
        self.origen        = origen
        self.destino       = destino
        self.sentiment     = sentiment      # sentiment_sum  (puede ser negativo)
        self.interacciones = interacciones  # interaction_count

    def __repr__(self):
        signo = "+" if self.sentiment >= 0 else ""
        return (f"Relacion({self.origen} → {self.destino} | "
                f"sentiment={signo}{self.sentiment:.4f}, "
                f"interacciones={self.interacciones})")


# ════════════════════════════════════════════════════════════════════
#  FUNCIONES DE CARGA
# ════════════════════════════════════════════════════════════════════

def cargar_usuarios(ruta: str) -> dict:
    """
    Lee user.csv  →  columna: username
    Devuelve dict  username (str) → Usuario
    """
    usuarios = {}
    with open(ruta, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            u = fila.get("username", "").strip()
            if u and u not in usuarios:
                usuarios[u] = Usuario(u)

    print(f"[cargar] Usuarios          : {len(usuarios)}")
    return usuarios


def cargar_submissions(ruta: str, usuarios: dict) -> list:
    """
    Lee submission.csv  →  columnas: post_id, author, subreddit, score
    Si el autor no estaba en user.csv lo crea en el momento.
    Devuelve lista de objetos Post.
    """
    posts, ids_vistos = [], set()

    with open(ruta, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        print(f"[cargar] Columnas submission: {reader.fieldnames}")

        for fila in reader:
            post_id   = fila.get("post_id",   "").strip()
            username  = fila.get("author",    "").strip()
            subreddit = fila.get("subreddit", "").strip()
            score_raw = fila.get("score",     "0").strip()

            if not post_id or not username or not subreddit:
                continue
            if username in ("[deleted]", "[removed]"):
                continue
            if post_id in ids_vistos:
                continue
            ids_vistos.add(post_id)

            try:
                score = int(float(score_raw))
            except ValueError:
                score = 0

            if username not in usuarios:
                usuarios[username] = Usuario(username)

            posts.append(Post(post_id, usuarios[username], subreddit, score))

    print(f"[cargar] Posts             : {len(posts)}")
    return posts


def cargar_relaciones(ruta: str, usuarios: dict) -> list:
    """
    Lee user_relations.csv
    Columnas: source_author, target_author, sentiment_sum, interaction_count
    Vincula cada Relacion a la lista enlazada del usuario origen.
    Devuelve lista de objetos Relacion.
    """
    relaciones = []

    with open(ruta, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        print(f"[cargar] Columnas relations : {reader.fieldnames}")

        for fila in reader:
            src   = fila.get("source_author",    "").strip()
            dst   = fila.get("target_author",    "").strip()
            sent  = fila.get("sentiment_sum",    "0").strip()
            inter = fila.get("interaction_count","0").strip()

            if not src or not dst:
                continue

            if src not in usuarios:
                usuarios[src] = Usuario(src)
            if dst not in usuarios:
                usuarios[dst] = Usuario(dst)

            try:
                sentiment     = float(sent)
                interacciones = int(float(inter))
            except ValueError:
                sentiment, interacciones = 0.0, 0

            rel = Relacion(usuarios[src], usuarios[dst], sentiment, interacciones)
            usuarios[src].relaciones.insertar(rel)
            relaciones.append(rel)

    print(f"[cargar] Relaciones        : {len(relaciones)}")
    return relaciones
