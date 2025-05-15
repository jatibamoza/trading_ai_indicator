# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime
import os

from src.noticias import obtener_noticias
from src.scraper_investing import obtener_titulares_investing
from src.procesamiento import analizar_sentimiento
from src.visualizacion import visualizar_precio_vs_noticias
from src.senales import generar_senal, calcular_score_sentimiento
from config import NOTICIAS_DIR

st.set_page_config(layout="wide")
st.title("Análisis de Sentimiento y Precios Intradía")
st.write("Visualización de noticias relevantes y su impacto en activos financieros.")

# --- Selección de intervalo e historial ---
intervalo = st.sidebar.selectbox("Intervalo de precios", ["1h", "4h", "1d", "1mo"])
fecha_inicio = st.sidebar.date_input("Desde", datetime(2024, 11, 1))
fecha_fin = st.sidebar.date_input("Hasta", datetime.today())

# --- Obtener y analizar noticias ---
noticias_newsapi = obtener_noticias()
noticias_investing = obtener_titulares_investing()
noticias = noticias_newsapi + noticias_investing
noticias = analizar_sentimiento(noticias)

# --- Asociar noticias con activos ---
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

for noticia in noticias:
    texto_completo = noticia["titulo"] + " " + (noticia["descripcion"] or "")
    noticia["activo"] = identificar_activo(texto_completo)

# --- Descargar precios por activo ---
activos = {
    "oro": {"nombre": "Oro", "ticker": "GC=F", "unidad": "USD"},
    "eurusd": {"nombre": "EUR/USD", "ticker": "EURUSD=X", "unidad": "USD"},
    "ibex35": {"nombre": "IBEX 35", "ticker": "^IBEX", "unidad": "Puntos"}
}

precios_map = {}
senal_map = {}
score_map = {}

for clave, activo in activos.items():
    df = yf.download(
        activo["ticker"],
        start=fecha_inicio,
        end=fecha_fin,
        interval=intervalo
    )
    df.index = pd.to_datetime(df.index)
    precios_map[clave] = df
    noticias_filtradas = [n for n in noticias if n["activo"] == clave]
    senal_map[clave] = generar_senal(df, noticias_filtradas)
    score_map[clave] = calcular_score_sentimiento(noticias_filtradas)

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
tabs = st.tabs(["Oro", "EUR/USD", "IBEX 35"])

for i, clave in enumerate(activos.keys()):
    activo = activos[clave]
    with tabs[i]:
        st.subheader(f"Precio de {activo['nombre']} vs Noticias")

        df_precios = precios_map[clave]
        noticias_filtradas = [n for n in noticias if n["activo"] == clave]

        if noticias_filtradas and not df_precios.empty:
            # Mostrar gráfico
            fig = visualizar_precio_vs_noticias(df_precios, noticias_filtradas, activo["nombre"], activo["unidad"])
            st.plotly_chart(fig, use_container_width=True)

            # Mostrar tabla de noticias
            df_view = pd.DataFrame(noticias_filtradas)[["fecha", "titulo", "fuente", "sentimiento", "score"]]
            st.dataframe(df_view, use_container_width=True, height=200)

            # Mostrar señal con explicación
            senal = senal_map[clave]
            score_promedio = score_map[clave]

            try:
                ultimo_precio = float(df_precios["Close"].iloc[-1])
                precio_pasado = float(df_precios["Close"].iloc[-6])
                variacion = ((ultimo_precio - precio_pasado) / precio_pasado) * 100
                st.markdown(f"Señal de trading actual: **{senal}**")
                st.markdown(f"Sentimiento promedio: **{score_promedio:.2f}**")
                st.markdown(f"Variación de precio reciente: **{variacion:.2f}%**")
            except Exception:
                st.warning("No se pudo calcular la variación de precio.")

            st.markdown(f"Noticias analizadas: **{len(noticias_filtradas)}**")
        else:
            st.info(f"No hay suficientes datos para mostrar el análisis de '{activo['nombre']}'.")
