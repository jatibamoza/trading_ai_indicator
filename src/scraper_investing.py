
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def obtener_titulares_investing(url="https://www.investing.com/news/stock-market-news"):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    r = requests.get(url, headers=headers)
    #soup = BeautifulSoup(r.content, "lxml")
    soup = BeautifulSoup(r.content, "html.parser")

    articulos = soup.find_all("article", class_="js-article-item")
    noticias = []

    for art in articulos:
        try:
            titulo = art.find("a", class_="title").get_text(strip=True)
            link = "https://www.investing.com" + art.find("a")["href"]
            fecha = datetime.now().isoformat()
            noticias.append({
                "titulo": titulo,
                "descripcion": "",
                "fuente": "Investing",
                "fecha": fecha,
                "url": link
            })
        except Exception:
            continue

    return noticias
