# src/procesamiento.py

from textblob import TextBlob

def analizar_sentimiento(noticias):
    """
    Recibe una lista de diccionarios con noticias.
    Devuelve una nueva lista con el campo 'sentimiento'.
    """
    noticias_procesadas = []

    for noticia in noticias:
        texto = f"{noticia['titulo']} {noticia['descripcion'] or ''}"
        sentimiento = TextBlob(texto).sentiment.polarity

        if sentimiento > 0.1:
            categoria = "positivo"
        elif sentimiento < -0.1:
            categoria = "negativo"
        else:
            categoria = "neutro"

        noticia["sentimiento"] = categoria
        noticia["score"] = round(sentimiento, 3)
        noticias_procesadas.append(noticia)

    return noticias_procesadas
