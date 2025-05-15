# src/noticias.py

import os
from newsapi import NewsApiClient
from config import NEWSAPI_KEY, NOTICIAS_QUERY, NOTICIAS_LENGUAJE, NOTICIAS_DIR
from datetime import datetime
import pandas as pd

def obtener_noticias():
    newsapi = NewsApiClient(api_key=NEWSAPI_KEY)
    all_articles = newsapi.get_everything(q=NOTICIAS_QUERY,
                                          language=NOTICIAS_LENGUAJE,
                                          sort_by='publishedAt',
                                          page_size=100)

    noticias = [
        {
            "fecha": art["publishedAt"],
            "titulo": art["title"],
            "descripcion": art["description"],
            "fuente": art["source"]["name"]
        }
        for art in all_articles["articles"]
    ]

    # Guardar CSV
    os.makedirs(NOTICIAS_DIR, exist_ok=True)
    fecha = datetime.now().strftime("%Y%m%d_%H%M")
    df = pd.DataFrame(noticias)
    df.to_csv(f"{NOTICIAS_DIR}/noticias_{fecha}.csv", index=False)

    return noticias
