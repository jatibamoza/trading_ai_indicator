
import os
import time
import requests
import pandas as pd
from datetime import datetime, timedelta
from config import NEWSAPI_KEY, NOTICIAS_DIR, NOTICIAS_QUERY, NOTICIAS_LENGUAJE

def obtener_noticias_por_dia(fecha: str):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": NOTICIAS_QUERY,
        "from": fecha,
        "to": fecha,
        "language": NOTICIAS_LENGUAJE,
        "sortBy": "publishedAt",
        "apiKey": NEWSAPI_KEY,
        "pageSize": 100,
        "page": 1
    }

    all_articles = []
    while True:
        resp = requests.get(url, params=params)
        if resp.status_code != 200:
            print(f"Error {resp.status_code}: {resp.text}")
            break

        data = resp.json()
        articles = data.get("articles", [])
        if not articles:
            break

        for a in articles:
            all_articles.append({
                "fecha": a["publishedAt"],
                "titulo": a["title"],
                "descripcion": a.get("description", ""),
                "fuente": a["source"]["name"],
                "url": a["url"]
            })

        if len(articles) < 100 or params["page"] >= 5:
            break

        params["page"] += 1
        time.sleep(1)  # evitar rate limit

    return all_articles

def descargar_noticias_historicas(dias_atras=30):
    hoy = datetime.utcnow().date()
    os.makedirs(NOTICIAS_DIR, exist_ok=True)

    for i in range(dias_atras):
        dia = hoy - timedelta(days=i)
        fecha_str = dia.isoformat()
        print(f"📅 Descargando noticias para: {fecha_str}")
        noticias = obtener_noticias_por_dia(fecha_str)

        if noticias:
            df = pd.DataFrame(noticias)
            archivo = os.path.join(NOTICIAS_DIR, f"newsapi_{fecha_str}.csv")
            df.to_csv(archivo, index=False)
            print(f"✅ Guardadas: {archivo} ({len(noticias)} noticias)")
        else:
            print("⚠️  No se encontraron noticias.")

if __name__ == "__main__":
    descargar_noticias_historicas(dias_atras=30)
