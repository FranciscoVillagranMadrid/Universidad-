# main.py
# Punto de entrada del programa.
#
# Archivos necesarios en la misma carpeta:
#   submission.csv      → posts de Reddit
#   user.csv            → lista de usuarios
#   user_relations.csv  → relaciones entre usuarios
#   stopwords.txt       → una stopword por línea

from stopwords import cargar_stopwords
from cargar    import cargar_usuarios, cargar_submissions, cargar_relaciones
from indice    import (construir_indice_subreddits,
                       construir_indice_autores,
                       construir_indice_relaciones)
from buscar    import (buscar_por_subreddit,
                       buscar_posts_de_autor,
                       buscar_relaciones,
                       buscar_camino)

# ── Rutas de archivos (edita si tus archivos tienen otro nombre) ─────
RUTA_STOPWORDS   = "stopwords.txt"
RUTA_USERS       = "users.csv"
RUTA_SUBMISSIONS = "submissions.csv"
RUTA_RELATIONS   = "user_relations.csv"
# ────────────────────────────────────────────────────────────────────

def main():

    # 1. Stopwords
    print("\n[1] Cargando stopwords...")
    stopwords = cargar_stopwords(RUTA_STOPWORDS)

    # 2. Usuarios base
    print("\n[2] Cargando usuarios...")
    usuarios = cargar_usuarios(RUTA_USERS)

    # 3. Posts (submissions)
    print("\n[3] Cargando submissions...")
    posts = cargar_submissions(RUTA_SUBMISSIONS, usuarios)

    # 4. Relaciones
    print("\n[4] Cargando relaciones...")
    relaciones = cargar_relaciones(RUTA_RELATIONS, usuarios)

    # 5. Construcción de índices
    print("\n[5] Construyendo índices...")
    indice_sub  = construir_indice_subreddits(posts, stopwords)
    indice_aut  = construir_indice_autores(posts)
    indice_rel  = construir_indice_relaciones(relaciones)

    # 6. Menú
    while True:
        print("\n" + "=" * 50)
        print("  PUSHSHIFT REDDIT — ÍNDICE INVERTIDO")
        print("=" * 50)
        print("  [1] Buscar posts por subreddit")
        print("  [2] Ver posts de un usuario")
        print("  [3] Ver relaciones de un usuario")
        print("  [4] Verificar relación entre dos usuarios")
        print("  [0] Salir")
        print("=" * 50)

        opcion = input("  Opción: ").strip()

        if opcion == "1":
            q = input("\n  Subreddit(s) separados por espacio: ").strip()
            buscar_por_subreddit(indice_sub, q.split(), stopwords)

        elif opcion == "2":
            u = input("\n  Nombre de usuario: ").strip()
            buscar_posts_de_autor(indice_aut, u)

        elif opcion == "3":
            u = input("\n  Nombre de usuario: ").strip()
            buscar_relaciones(indice_rel, u)

        elif opcion == "4":
            a = input("\n  Usuario A: ").strip()
            b = input("  Usuario B: ").strip()
            buscar_camino(indice_rel, a, b)

        elif opcion == "0":
            print("\n  Saliendo...\n")
            break

        else:
            print("  [!] Opción inválida.")


if __name__ == "__main__":
    main()
