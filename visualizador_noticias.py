
import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime
import os

from src.noticias import obtener_noticias
from src.procesamiento import analizar_sentimiento
from src.visualizacion import visualizar_precio_vs_noticias
from src.senales import generar_senal
from config import NOTICIAS_DIR

from src.scraper_investing import obtener_titulares_investing

st.set_page_config(layout="wide")
st.title("🧠 Análisis de Sentimiento y Precios Intradía")
st.write("Visualización de noticias relevantes y su impacto en activos financieros.")

# --- Obtener Obtener noticias desde NewsAPI
noticias_newsapi = obtener_noticias()
# Obtener noticias desde Investing.com
noticias_investing = obtener_titulares_investing()
# Combinar ambas
noticias = noticias_newsapi + noticias_investing
# Analizar noticias
noticias = analizar_sentimiento(noticias)

# --- Asociar noticias con activos ---
def identificar_activo(texto):
    texto = texto.lower()
    if "gold" in texto:
        return "oro"
    elif "euro" in texto:
        return "eurusd"
    elif "spain" in texto:
        return "ibex35"
    else:
        return None

for noticia in noticias:
    texto_completo = noticia["titulo"] + " " + (noticia["descripcion"] or "")
    noticia["activo"] = identificar_activo(texto_completo)

# --- Descargar precios por activo ---
activos = {
    "oro": {"nombre": "Oro", "ticker": "GC=F", "keyword": "gold"},
    "eurusd": {"nombre": "EUR/USD", "ticker": "EURUSD=X", "keyword": "euro"},
    "ibex35": {"nombre": "IBEX 35", "ticker": "^IBEX", "keyword": "spain"}
}

precios_map = {}
senal_map = {}

for clave, activo in activos.items():
    df = yf.download(activo["ticker"], period="5d", interval="15m")
    df.index = pd.to_datetime(df.index)
    precios_map[clave] = df
    noticias_filtradas = [n for n in noticias if n["activo"] == clave]
    senal_map[clave] = generar_senal(df, noticias_filtradas)

# --- Asignar señal a cada noticia ---
for noticia in noticias:
    activo = noticia.get("activo")
    noticia["senal"] = senal_map.get(activo, "HOLD")

# --- Guardar CSV final con sentimiento + activo + señal ---
df_final = pd.DataFrame(noticias)
os.makedirs(NOTICIAS_DIR, exist_ok=True)
fecha = datetime.now().strftime("%Y%m%d_%H%M")
df_final.to_csv(f"{NOTICIAS_DIR}/noticias_procesadas_{fecha}.csv", index=False)

# --- Mostrar interfaz Streamlit ---
tabs = st.tabs(["🟡 Oro", "💶 EUR/USD", "📈 IBEX 35"])

for i, clave in enumerate(activos.keys()):
    activo = activos[clave]
    with tabs[i]:
        st.subheader(f"📊 Precio de {activo['nombre']} vs Noticias")

        df_precios = precios_map[clave]
        noticias_filtradas = [n for n in noticias if n["activo"] == clave]

        if noticias_filtradas:
            fig = visualizar_precio_vs_noticias(df_precios, noticias_filtradas)
            st.plotly_chart(fig, use_container_width=True)

            senal = senal_map[clave]
            st.markdown(f"📍 Señal de trading actual: **:blue[{senal}]**")
            st.markdown(f"🔍 Noticias analizadas: **{len(noticias_filtradas)}**")
        else:
            st.info(f"No hay noticias relevantes para '{activo['nombre']}' en este momento.")
