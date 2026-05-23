# indices.py

#importa la lista de post, usuarios y terminos desde el archivo de listas
from listas import ListaPosts, ListaUsuarios, ListaTerminos

#se crea una clase auxiliar que filtra y guarda las stopwords
#incluye funciones para filtrar stopwords y guardar terminos validos
class FiltroStopwords:
    
    #se inicializa el diccionario que guarda las stopwords
    def __init__(self):
        self.palabras = {}

    #agrega las stopwords al diccionario
    def agregar(self, palabra):
        palabra = palabra.strip().lower() #cada stopword está en minuscula y sin espacios en blanco
        
        if palabra != "": #si la palabra no esta vacia se guarda en el diccionario
            self.palabras[palabra] = True #guarda la stopword en el diccionario
    
    #verifica si una palabra es stopword
    def es_stopword(self, palabra):
        return palabra.lower() in self.palabras #retorna True si está en el diccionario y False si no

    #muestra el total de stopwords guardadas
    def total(self):
        return len(self.palabras)

    #funcion para limpiar una palabra y quitar caracteres que no sirven
    def limpiar_palabra(self, palabra):
        limpia = "" #variable temporal donde se va armando la palabra limpia
        i = 0 #indice para recorrer la palabra
        
        while i < len(palabra): #mientras el indice sea más corto que el largo de la palabra sigue el ciclo
            c = palabra[i].lower() #guarda el caracter actual de la palabra en minuscula
            
            if (c >= "a" and c <= "z") or (c >= "0" and c <= "9") or c == "_": #si c es letra, numero o guion bajo
                limpia = limpia + c #el caracter se agrega a la palabra limpia
            i = i + 1 #aumenta el indice para seguir recorriendo
            
        return limpia #devuelve la palabra almacenada en la variable temporal (limpia)

   #funcion que revisa si una palabra sirve antes de guardarla como termino
    def agregar_termino_si_valido(self, terminos, palabra):
        palabra = self.limpiar_palabra(palabra) #usa la funcion de limpiar la palabra primero
        
        if palabra != "" and len(palabra) > 2 and not palabra.isdigit(): #si la palabra existe, es mayor a 2 en su largo y no es un número sigue 
            
            if not self.es_stopword(palabra): #si no sale en el diccionario de las stopwords sigue 
                terminos.insertar(palabra) #inserta la palabra en la lista de terminos

    #funcion para obtener los terminos validos dentro de un texto
    def filtrar_texto(self, texto): 
        # Se arma palabra por palabra. Los signos cortan la palabra
        terminos = ListaTerminos() #se crea la lista enlazada de terminos (su estructura está importada)
        palabra = "" #se define palabra como una palabra vacia
        i = 0 #se define el indice que va a recorrer el texto
        
        while i < len(texto): #mientras i sea menor que el largo del texto sigue el bucle
            c = texto[i] #c es cada caracter que va recorriendo i
            
            if c.isalnum() or c == "_": #comprueba si el caracter es letra, numero o "_"
                palabra = palabra + c #se va armando la palabra caracter por caracter
                
            else: #en caso de no cumplir alguna condición
                self.agregar_termino_si_valido(terminos, palabra) #verifica si es un termino válido con la funcion ya creada 
                palabra = "" #reinicia la palabra para empezar otra
            i = i + 1 #agrega 1 al indice para seguir recorriendo
            
        self.agregar_termino_si_valido(terminos, palabra) #revisa la ultima palabra del texto
        return terminos #devuelve la lista enlazada con los terminos

#se crea el indice invertido de los post con sus terminos
class IndiceInvertidoPosts:
    
    #se inicializa como diccionario vacio
    def __init__(self):
        self.vocabulario = {}

    #funcion que insterta los terminos
    def insertar(self, termino, post):
        termino = termino.lower().strip() #los terminos estan en minusculas y limpios
        if termino == "": #si el termino está vacio no se guarda
            return
        
        if termino not in self.vocabulario: #si el termino no está en el diccionario de vocabulario
            self.vocabulario[termino] = ListaPosts() #lo agrega al vocabulario y crea una lista para guardar los post relacionados
        self.vocabulario[termino].insertar(post) #enlaza el termino con el post correspondiente

    #IMPORTANTE
    #funcion que construye el indice invertido con los terminos de cada post
    def construir(self, posts, filtro):
        for post_id in posts: #recorre los id de los posts
            post = posts[post_id] #obtiene el post usando su id
            post.terminos = filtro.filtrar_texto(post.texto) #filtra los terminos del post con la funcion creada previamente               
            actual = post.terminos.head #variable que recorre los terminos, inicia desde el primer nodo
            
            while actual is not None: #mientras existan terminos en el post sigue el ciclo
                self.insertar(actual.dato, post) #relaciona el termino con el post en el indice
                actual = actual.siguiente #avanza al siguiente termino

    #funcion para buscar posts por un termino
    def buscar(self, termino): 
        termino = termino.lower().strip() #se limpia el termino y se pone en minuscula
        
        if termino in self.vocabulario: #si el termino está en el diccionario de terminos 
            return self.vocabulario[termino] #retorna lo que está asociado a ese termino (lista de posts) 
          
        return None #si no encuentra nada en el diccionario retorna None
    
    #funcion que muestra la cantidad de terminos guardados
    def total_terminos(self):
        return len(self.vocabulario)

#se crea el indice invertido de usuarios con sus contactos
class IndiceInvertidoUsuarios:
    
    #se inicializa el diccionario donde se guardan los username de cada usuario
    def __init__(self):
        self.mapa = {}

    #funcion que registra un usuario en el diccionario y le crea una lista de contactos
    def registrar_usuario(self, username):
        if username != "" and username not in self.mapa: #si el usuario existe y no está en el diccionario
            self.mapa[username] = ListaUsuarios() #se crea una lista de contactos para ese usuario

    #funcion que guarda y asocia los contactos con el username (funcion que hace el trabajo de amigos en una red social)
    def agregar_contacto(self, username, contacto):
        if username == "" or contacto == "" or username == contacto: #si el usuario o contacto están vacios, o si son el mismo, no sigue
            return #sale sin agregar nada

        self.registrar_usuario(username) #registra el usuario si todavia no existe
        self.mapa[username].insertar(contacto) #registra el contacto ligado al username

    #funcion que muestra los contactos de un usuario
    def obtener_contactos(self, username):
        if username in self.mapa: #si el username del usuario esta en el diccionario
            return self.mapa[username] #retorna la lista de contactos del usuario
        
        return None #si el usuario no está registrado retorna None

    #funcion que muestra la cantidad de usuarios que hay en el diccionario
    def total_usuarios(self):
        return len(self.mapa)
