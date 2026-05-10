# red_social.py
# Persona 1: carga de archivos y sistema principal.
# Ejecutar con: python red_social.py

from listas import ListaUsuarios, ListaLikes, ListaTerminos
from indices import FiltroStopwords, IndiceInvertidoPosts, IndiceInvertidoUsuarios

SEPARADOR = "|"


class Usuario:
    def __init__(self, user_id, username, karma):
        self.user_id = user_id
        self.username = username
        self.karma = karma
        self.contactos = ListaUsuarios()


    def __repr__(self):
        return "Usuario(" + self.username + ", karma=" + str(self.karma) + ")"


class Post:
    def __init__(self, post_id, username, texto, score):
        self.post_id = post_id
        self.username = username
        self.texto = texto
        self.score = score
        self.terminos = ListaTerminos()
        self.likes = ListaLikes()
        self.cargar_likes_simbolicos()

    def cargar_likes_simbolicos(self):
        # Reddit entrega score total, no la identidad de quienes votaron.
        cantidad = self.score
        if cantidad < 0:
            cantidad = 0
        if cantidad > ListaLikes.MAX_LIKES:
            cantidad = ListaLikes.MAX_LIKES
        i = 1
        while i <= cantidad:
            self.likes.insertar("like_" + str(i))
            i = i + 1

    def __repr__(self):
        texto = self.texto
        if len(texto) > 45:
            texto = texto[:45] + "..."
        return "Post(" + self.post_id + ", @" + self.username + ", score=" + str(self.score) + ", '" + texto + "')"


class SistemaRedSocial:
    def __init__(self):
        self.usuarios = {}
        self.posts = {}
        self.filtro = FiltroStopwords()
        self.indice_posts = IndiceInvertidoPosts()
        self.indice_usuarios = IndiceInvertidoUsuarios()
        self.total_relaciones = 0

    def numero(self, texto):
        texto = texto.strip()
        if texto == "":
            return 0
        try:
            return int(texto)
        except ValueError:
            return 0

    def cargar_stopwords(self, ruta):
        archivo = open(ruta, "r", encoding="utf-8")
        linea = archivo.readline()
        while linea != "":
            palabra = linea.strip().lower()
            if palabra != "" and not palabra.startswith("#"):
                self.filtro.agregar(palabra)
            linea = archivo.readline()
        archivo.close()

    def cargar_usuarios(self, ruta):
        archivo = open(ruta, "r", encoding="utf-8")
        archivo.readline()
        linea = archivo.readline()
        while linea != "":
            linea = linea.strip()
            if linea != "":
                partes = linea.split(SEPARADOR)
                if len(partes) >= 3:
                    user_id = partes[0].strip()
                    username = partes[1].strip()
                    karma = self.numero(partes[2])
                    if username != "" and username not in self.usuarios:
                        self.usuarios[username] = Usuario(user_id, username, karma)
                        self.indice_usuarios.registrar_usuario(username)
            linea = archivo.readline()
        archivo.close()

    def cargar_posts(self, ruta):
        archivo = open(ruta, "r", encoding="utf-8")
        archivo.readline()
        linea = archivo.readline()
        while linea != "":
            linea = linea.strip()
            if linea != "":
                partes = linea.split(SEPARADOR)
                if len(partes) >= 4:
                    post_id = partes[0].strip()
                    username = partes[1].strip()
                    texto = partes[2].strip()
                    score = self.numero(partes[3])

                    if post_id != "" and username != "" and texto != "" and post_id not in self.posts:
                        if username not in self.usuarios:
                            self.usuarios[username] = Usuario(username, username, 0)
                            self.indice_usuarios.registrar_usuario(username)
                        self.posts[post_id] = Post(post_id, username, texto, score)
            linea = archivo.readline()
        archivo.close()

    def cargar_relaciones(self, ruta):
        archivo = open(ruta, "r", encoding="utf-8")
        archivo.readline()
        linea = archivo.readline()
        while linea != "":
            linea = linea.strip()
            if linea != "":
                partes = linea.split(SEPARADOR)
                if len(partes) >= 2:
                    origen = partes[0].strip()
                    contacto = partes[1].strip()
                    if origen != "" and contacto != "" and origen != contacto:
                        if origen not in self.usuarios:
                            self.usuarios[origen] = Usuario(origen, origen, 0)
                            self.indice_usuarios.registrar_usuario(origen)
                        if contacto not in self.usuarios:
                            self.usuarios[contacto] = Usuario(contacto, contacto, 0)
                            self.indice_usuarios.registrar_usuario(contacto)

                        antes = self.usuarios[origen].contactos.contar()
                        self.usuarios[origen].contactos.insertar(contacto)
                        self.indice_usuarios.agregar_contacto(origen, contacto)
                        despues = self.usuarios[origen].contactos.contar()
                        if despues > antes:
                            self.total_relaciones = self.total_relaciones + 1
            linea = archivo.readline()
        archivo.close()

    def construir_indices(self):
        self.indice_posts.construir(self.posts, self.filtro)

    def buscar_posts(self, termino):
        termino = self.filtro.limpiar_palabra(termino)
        if termino == "" or self.filtro.es_stopword(termino):
            return []
        lista = self.indice_posts.buscar(termino)
        if lista is None:
            return []
        return lista.recorrer()

    def buscar_contactos(self, username):
        lista = self.indice_usuarios.obtener_contactos(username)
        if lista is None:
            return []
        return lista.recorrer()

    def mostrar_resumen(self):
        print("Usuarios cargados:", len(self.usuarios))
        print("Posts cargados:", len(self.posts))
        print("Relaciones cargadas:", self.total_relaciones)
        print("Stopwords cargadas:", self.filtro.total())
        print("Términos indexados:", self.indice_posts.total_terminos())


def mostrar_posts(posts, maximo):
    if len(posts) == 0:
        print("No se encontraron posts.")
        return
    i = 0
    while i < len(posts) and i < maximo:
        print("-", posts[i])
        i = i + 1


def mostrar_contactos(contactos, maximo):
    if len(contactos) == 0:
        print("No se encontraron contactos.")
        return
    i = 0
    while i < len(contactos) and i < maximo:
        print("-", contactos[i])
        i = i + 1


def main():
    sistema = SistemaRedSocial()
    sistema.cargar_stopwords("stopwords.txt")
    sistema.cargar_usuarios("usuarios.csv")
    sistema.cargar_posts("posts.csv")
    sistema.cargar_relaciones("relaciones.csv")
    sistema.construir_indices()

    print("\nResumen de carga")
    sistema.mostrar_resumen()

    print("\nBúsqueda de posts por término: python")
    posts = sistema.buscar_posts("python")
    mostrar_posts(posts, 5)

    usuario_prueba = ""
    for username in sistema.usuarios:
        usuario_prueba = username
        break

    print("\nContactos de usuario:", usuario_prueba)
    contactos = sistema.buscar_contactos(usuario_prueba)
    mostrar_contactos(contactos, 8)


if __name__ == "__main__":
    main()
