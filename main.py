# main.py

from src.precios import descargar_precios
from src.noticias import obtener_noticias

def ejecutar_pipeline():
    print("Descargando precios...")
    precios = descargar_precios()
    print("Precios descargados.")

    print("Descargando noticias...")
    noticias = obtener_noticias()
    print("Noticias descargadas.")

if __name__ == "__main__":
    ejecutar_pipeline()
