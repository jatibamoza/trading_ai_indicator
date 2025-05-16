
import os
from newsapi import NewsApiClient
from newsapi.newsapi_exception import NewsAPIException
from config import NEWSAPI_KEY, NOTICIAS_QUERY, NOTICIAS_LENGUAJE, NOTICIAS_DIR
from datetime import datetime
import pandas as pd


def obtener_noticias():
    noticias = []
    try:
        newsapi = NewsApiClient(api_key=NEWSAPI_KEY)
        respuesta = newsapi.get_everything(
            q=NOTICIAS_QUERY,
            language=NOTICIAS_LENGUAJE,
            sort_by="publishedAt",
            page_size=100
        )
        for a in respuesta.get("articles", []):
            noticias.append({
                "fecha": a["publishedAt"],
                "titulo": a["title"],
                "descripcion": a.get("description", ""),
                "fuente": a["source"]["name"],
                "url": a["url"]
            })
        # Guardar CSV
        os.makedirs(NOTICIAS_DIR, exist_ok=True)
        fecha = datetime.now().strftime("%Y%m%d_%H%M")
        df = pd.DataFrame(noticias)
        df.to_csv(f"{NOTICIAS_DIR}/noticias_{fecha}.csv", index=False)
    except NewsAPIException as e:
        print(f"⚠️ Error al obtener noticias desde NewsAPI: {e}")
    except Exception as e:
        print(f"⚠️ Error inesperado al obtener noticias: {e}")
    return noticias
