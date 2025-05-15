
import os
import pandas as pd
from src.procesamiento import analizar_sentimiento
from src.senales import generar_senal
from config import NOTICIAS_DIR

# Cargar archivo combinado sin procesar
ruta = os.path.join(NOTICIAS_DIR, "noticias_historicas_combinadas.csv")
if not os.path.exists(ruta):
    raise FileNotFoundError("No se encontró el archivo combinado de noticias.")

df = pd.read_csv(ruta)

# Analizar sentimiento
noticias = df.to_dict(orient="records")
noticias_procesadas = analizar_sentimiento(noticias)

# Asignar activo a cada noticia
def identificar_activo(texto):
    texto = texto.lower()
    if "gold" in texto:
        return "oro"
    elif "euro" in texto or "ecb" in texto:
        return "eurusd"
    elif "spain" in texto or "ibex" in texto:
        return "ibex35"
    else:
        return None

for noticia in noticias_procesadas:
    titulo = str(noticia.get("titulo", ""))
    descripcion = str(noticia.get("descripcion", ""))
    texto_completo = titulo + " " + descripcion
    noticia["activo"] = identificar_activo(texto_completo)

# Asignar señal heurística basada en sentimiento + score
for noticia in noticias_procesadas:
    score = noticia.get("score", 0)
    if score > 0.2:
        noticia["senal"] = "BUY"
    elif score < -0.2:
        noticia["senal"] = "SELL"
    else:
        noticia["senal"] = "HOLD"

# Convertir y guardar nuevo archivo
df_final = pd.DataFrame(noticias_procesadas)
salida = os.path.join(NOTICIAS_DIR, "noticias_historicas_procesadas.csv")
df_final.to_csv(salida, index=False)
print(f"✅ Noticias procesadas guardadas en: {salida}")
