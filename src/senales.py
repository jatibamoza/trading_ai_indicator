# src/senales.py

import numpy as np
import pandas as pd

def calcular_score_sentimiento(noticias):
    """
    Calcula un score promedio de sentimiento basado en las últimas N noticias.
    """
    if not noticias:
        return 0.0
    scores = [n["score"] for n in noticias if "score" in n and isinstance(n["score"], (int, float))]
    return np.mean(scores) if scores else 0.0

def generar_senal(df_precios, noticias, n_ultimas=5):
    """
    Genera una señal de trading combinando la variación reciente de precio
    con el sentimiento medio de las últimas noticias.
    """
    # Validaciones mínimas
    if "Close" not in df_precios.columns:
        return "HOLD"
    
    precios = df_precios["Close"].dropna()
    
    if len(precios) < 6:
        return "HOLD"

    # Obtener precios actuales y anteriores
    precio_ahora = precios.iloc[-1]
    precio_antes = precios.iloc[-6]
    variacion_pct = (precio_ahora - precio_antes) / precio_antes

    # Calcular sentimiento promedio
    ultimas_n = sorted(noticias, key=lambda x: x["fecha"], reverse=True)[:n_ultimas]
    score_sentimiento = calcular_score_sentimiento(ultimas_n)

    # Debug opcional:
    # print(f"Variación: {variacion_pct:.3f}, Sentimiento: {score_sentimiento:.2f}")

    # Lógica de decisión
    if score_sentimiento > 0.2 and variacion_pct < -0.005:
        return "BUY"
    elif score_sentimiento < -0.2 and variacion_pct > 0.005:
        return "SELL"
    else:
        return "HOLD"
