# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime
import os
import joblib

from src.noticias import obtener_noticias
from src.scraper_investing import obtener_titulares_investing
from src.procesamiento import analizar_sentimiento
from src.visualizacion import visualizar_precio_vs_noticias
from src.senales import calcular_score_sentimiento
from src.modelo_predictor import cargar_modelo_y_etiquetas, predecir_senal
from config import NOTICIAS_DIR

st.set_page_config(layout="wide")
st.title("Análisis de Sentimiento y Predicción de Señales con IA")

intervalo = st.sidebar.selectbox("Intervalo de precios", ["1h", "4h", "1d", "1mo"])
fecha_inicio = st.sidebar.date_input("Desde", datetime(2024, 11, 1))
fecha_fin = st.sidebar.date_input("Hasta", datetime.today())

noticias_newsapi = obtener_noticias()
noticias_investing = obtener_titulares_investing()
noticias = noticias_newsapi + noticias_investing
noticias = analizar_sentimiento(noticias)

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

activos = {
    "oro": {"nombre": "Oro", "ticker": "GC=F", "unidad": "USD"},
    "eurusd": {"nombre": "EUR/USD", "ticker": "EURUSD=X", "unidad": "USD"},
    "ibex35": {"nombre": "IBEX 35", "ticker": "^IBEX", "unidad": "Puntos"}
}

precios_map = {}
score_map = {}
prediccion_map = {}

for clave, activo in activos.items():
    df = yf.download(activo["ticker"], start=fecha_inicio, end=fecha_fin, interval=intervalo)
    df.index = pd.to_datetime(df.index)
    precios_map[clave] = df
    noticias_filtradas = [n for n in noticias if n["activo"] == clave]
    score_map[clave] = calcular_score_sentimiento(noticias_filtradas)

    modelo, etiquetas = cargar_modelo_y_etiquetas(clave)
    if modelo:
        score_medio = score_map[clave]
        sentimiento_dominante = max(set([n["sentimiento"] for n in noticias_filtradas]), key=[n["sentimiento"] for n in noticias_filtradas].count)
        prediccion = predecir_senal(modelo, etiquetas, score_medio, sentimiento_dominante)
        prediccion_map[clave] = prediccion
    else:
        prediccion_map[clave] = "N/A"

# --- Tabs con una adicional para métricas ---
tabs = st.tabs(["Oro", "EUR/USD", "IBEX 35", "Métricas del Modelo"])

for i, clave in enumerate(activos.keys()):
    activo = activos[clave]
    with tabs[i]:
        st.subheader(f"Precio de {activo['nombre']} vs Noticias")
        df_precios = precios_map[clave]
        noticias_filtradas = [n for n in noticias if n["activo"] == clave]

        if noticias_filtradas and not df_precios.empty:
            fig = visualizar_precio_vs_noticias(df_precios, noticias_filtradas, activo["nombre"], activo["unidad"])
            st.plotly_chart(fig, use_container_width=True)

            df_view = pd.DataFrame(noticias_filtradas)[["fecha", "titulo", "fuente", "sentimiento", "score"]]
            st.dataframe(df_view, use_container_width=True, height=200)

            try:
                ultimo_precio = float(df_precios["Close"].iloc[-1])
                precio_pasado = float(df_precios["Close"].iloc[-6])
                variacion = ((ultimo_precio - precio_pasado) / precio_pasado) * 100
                st.markdown(f"Predicción IA: **:blue[{prediccion_map[clave]}]**")
                st.markdown(f"Sentimiento promedio: **{score_map[clave]:.2f}**")
                st.markdown(f"Variación de precio reciente: **{variacion:.2f}%**")
            except Exception:
                st.warning("No se pudo calcular la variación de precio.")

            st.markdown(f"Noticias analizadas: **{len(noticias_filtradas)}**")
        else:
            st.info(f"No hay suficientes datos para mostrar el análisis de '{activo['nombre']}'.")

# --- Pestaña de métricas del modelo ---
with tabs[3]:
    st.subheader("📊 Métricas de los Modelos Entrenados")
    for clave in activos.keys():
        modelo_path = os.path.join("data", "modelos", f"{clave}_modelo.pkl")
        etiquetas_path = os.path.join("data", "modelos", f"{clave}_etiquetas.pkl")
        if os.path.exists(modelo_path) and os.path.exists(etiquetas_path):
            modelo = joblib.load(modelo_path)
            etiquetas = joblib.load(etiquetas_path)
            st.markdown(f"**Modelo entrenado para {clave.upper()}**")
            st.text(f"Número de árboles: {modelo.n_estimators}")
            st.text(f"Etiquetas: {list(etiquetas.values())}")
        else:
            st.markdown(f"⚠️ No hay modelo entrenado disponible para **{clave.upper()}**")
