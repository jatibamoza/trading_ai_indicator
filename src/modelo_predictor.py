
import os
import joblib
import pandas as pd

MODELOS_DIR = os.path.join("data", "modelos")

def cargar_modelo_y_etiquetas(activo):
    modelo_path = os.path.join(MODELOS_DIR, f"{activo}_modelo.pkl")
    etiquetas_path = os.path.join(MODELOS_DIR, f"{activo}_etiquetas.pkl")

    if not os.path.exists(modelo_path) or not os.path.exists(etiquetas_path):
        print(f"⚠️ No hay modelo entrenado para {activo}.")
        return None, None

    modelo = joblib.load(modelo_path)
    etiquetas = joblib.load(etiquetas_path)
    return modelo, etiquetas

def predecir_senal(modelo, etiquetas, score, sentimiento):
    sentimiento_encoded = {"positivo": 1, "neutro": 0, "negativo": -1}.get(sentimiento, 0)
    df = pd.DataFrame([[score, sentimiento_encoded]], columns=["score", "sentimiento_encoded"])
    pred = modelo.predict(df)[0]
    return etiquetas[pred]
