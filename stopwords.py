# stopwords.py
# Lee stopwords desde un archivo .txt (una palabra por línea).
# Las líneas que empiezan con # son comentarios y se ignoran.

def cargar_stopwords(ruta_txt: str) -> set:
    """
    Lee el .txt y devuelve un set de stopwords.
    Búsqueda O(1) gracias al set.
    """
    stopwords = set()
    with open(ruta_txt, encoding="utf-8") as f:
        for linea in f:
            palabra = linea.strip().lower()
            if palabra and not palabra.startswith("#"):
                stopwords.add(palabra)
    print(f"[stopwords] {len(stopwords)} palabras cargadas desde '{ruta_txt}'")
    return stopwords


def filtrar(terminos: list, stopwords: set) -> list:
    """
    Devuelve los términos que NO son stopwords, NO son vacíos,
    tienen más de 1 carácter y no son puramente numéricos.
    También limpia puntuación básica alrededor del token.
    """
    resultado = []
    for t in terminos:
        limpio = t.strip(".,!?;:\"'()[]{}#@\n\r\t/\\").lower()
        if len(limpio) <= 1:
            continue
        if limpio in stopwords:
            continue
        if limpio.isnumeric():
            continue
        resultado.append(limpio)
    return resultado
