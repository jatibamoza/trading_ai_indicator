# src/precios.py

import os
import yfinance as yf
from config import TICKERS, PRECIOS_DIR
from datetime import datetime

def descargar_precios():
    datos = {}
    for nombre, ticker in TICKERS.items():
        df = yf.download(ticker, period="30d", interval="15m")
        datos[nombre] = df

        # Guardar como CSV
        os.makedirs(PRECIOS_DIR, exist_ok=True)
        fecha = datetime.now().strftime("%Y%m%d_%H%M")
        df.to_csv(f"{PRECIOS_DIR}/{nombre}_{fecha}.csv")

    return datos
