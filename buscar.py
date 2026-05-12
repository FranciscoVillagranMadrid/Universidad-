# buscar.py
# Funciones de búsqueda sobre los tres índices.
#
#   buscar_por_subreddit   → posts de uno o varios subreddits
#   buscar_posts_de_autor  → posts publicados por un usuario
#   buscar_relaciones      → con quién interactuó un usuario
#   buscar_camino          → si hay relación directa entre dos usuarios

from cargar import ListaEnlazada
from stopwords import filtrar


# ── 1. Buscar posts por subreddit(s) ────────────────────────────────

def buscar_por_subreddit(indice_sub, terminos: list, stopwords: set):
    """
    Busca posts que pertenezcan a alguno de los subreddits indicados.
    Acepta uno o varios términos (unión de resultados).

    Parámetros:
        indice_sub : IndiceInvertido subreddit → posts
        terminos   : lista de strings ingresados por el usuario
        stopwords  : set de stopwords para limpiar la consulta
    """
    limpios = filtrar([t.lower() for t in terminos], stopwords)
    if not limpios:
        print("  [!] Consulta vacía tras filtrar stopwords.")
        return

    print(f"\n  Buscando en subreddit(s): {limpios}")
    print("  " + "-" * 48)

    resultados = ListaEnlazada()

    for termino in limpios:
        posting = indice_sub.buscar(termino)
        if posting is None:
            print(f"  [!] Subreddit '{termino}' no encontrado.")
            continue
        nodo = posting.cabeza
        while nodo:
            resultados.insertar(nodo.dato)
            nodo = nodo.siguiente

    total = len(resultados)
    if total == 0:
        print("  Sin resultados.")
        return

    print(f"  {total} post(s) encontrado(s):\n")
    nodo = resultados.cabeza
    i = 1
    while nodo:
        p = nodo.dato
        print(f"  [{i}] post_id={p.id}  autor={p.autor}  "
              f"r/{p.subreddit}  score={p.score}")
        nodo = nodo.siguiente
        i += 1


# ── 2. Buscar posts de un autor ──────────────────────────────────────

def buscar_posts_de_autor(indice_autores, username: str):
    """
    Muestra todos los posts publicados por un usuario.

    Parámetros:
        indice_autores : IndiceInvertido username → posts
        username       : autor a consultar
    """
    print(f"\n  Posts de @{username}")
    print("  " + "-" * 48)

    posting = indice_autores.buscar(username)
    if posting is None or len(posting) == 0:
        print(f"  Usuario '@{username}' no tiene posts indexados.")
        return

    print(f"  {len(posting)} post(s):\n")
    nodo = posting.cabeza
    i = 1
    while nodo:
        p = nodo.dato
        print(f"  [{i}] post_id={p.id}  r/{p.subreddit}  score={p.score}")
        nodo = nodo.siguiente
        i += 1


# ── 3. Buscar relaciones de un usuario ──────────────────────────────

def buscar_relaciones(indice_rel, username: str):
    """
    Muestra con quién interactuó un usuario (relaciones salientes),
    ordenadas por interaction_count descendente.

    Parámetros:
        indice_rel : IndiceInvertido username → relaciones
        username   : usuario a analizar
    """
    print(f"\n  Relaciones de @{username}")
    print("  " + "-" * 48)

    posting = indice_rel.buscar(username)
    if posting is None or len(posting) == 0:
        print(f"  No se encontraron relaciones para '@{username}'.")
        return

    # Recopilar en lista Python para ordenar
    rels = []
    nodo = posting.cabeza
    while nodo:
        rels.append(nodo.dato)
        nodo = nodo.siguiente

    # Ordenar por interacciones descendente
    rels.sort(key=lambda r: r.interacciones, reverse=True)

    print(f"  {len(rels)} relación(es):\n")
    for i, rel in enumerate(rels, 1):
        signo = "+" if rel.sentiment >= 0 else ""
        print(f"  [{i}] → {rel.destino}  "
              f"interacciones={rel.interacciones}  "
              f"sentiment={signo}{rel.sentiment:.4f}")


# ── 4. Verificar relación directa entre dos usuarios ────────────────

def buscar_camino(indice_rel, usuario_a: str, usuario_b: str):
    """
    Verifica si existe relación directa A → B y/o B → A.

    Parámetros:
        indice_rel : IndiceInvertido username → relaciones
        usuario_a  : primer usuario
        usuario_b  : segundo usuario
    """
    print(f"\n  Relación directa entre @{usuario_a} y @{usuario_b}")
    print("  " + "-" * 48)

    encontrado = False

    for src, dst in [(usuario_a, usuario_b), (usuario_b, usuario_a)]:
        posting = indice_rel.buscar(src)
        if posting is None:
            continue
        nodo = posting.cabeza
        while nodo:
            rel = nodo.dato
            if rel.destino.username == dst:
                signo = "+" if rel.sentiment >= 0 else ""
                print(f"  {rel.origen} → {rel.destino}  "
                      f"interacciones={rel.interacciones}  "
                      f"sentiment={signo}{rel.sentiment:.4f}")
                encontrado = True
            nodo = nodo.siguiente

    if not encontrado:
        print(f"  No existe relación directa entre @{usuario_a} y @{usuario_b}.")
