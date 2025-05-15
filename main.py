# main.py

from src.precios import descargar_precios
from src.noticias import obtener_noticias
from src.procesamiento import analizar_sentimiento

def ejecutar_pipeline():
    print("Descargando precios...")
    precios = descargar_precios()
    print("Precios descargados.")

    print("Descargando noticias...")
    noticias = obtener_noticias()
    print("Noticias descargadas.")

if __name__ == "__main__":
    ejecutar_pipeline()

noticias = obtener_noticias()
noticias_analizadas = analizar_sentimiento(noticias)

# Imprimir resumen
for n in noticias_analizadas[:5]:
    print(f"[{n['sentimiento'].upper()}] {n['titulo']} ({n['score']})")