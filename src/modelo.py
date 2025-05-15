
import os
import sys
import pandas as pd
import numpy as np
import joblib
from glob import glob
from datetime import datetime

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Añadir raíz del proyecto al path para importar config
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)

from config import NOTICIAS_DIR

MODELOS_DIR = os.path.join("data", "modelos")
os.makedirs(MODELOS_DIR, exist_ok=True)

def cargar_csv_procesado():
    archivo_procesado = os.path.join(NOTICIAS_DIR, "noticias_historicas_procesadas.csv")
    if os.path.exists(archivo_procesado):
        print(f"📂 Usando archivo procesado: {archivo_procesado}")
        return archivo_procesado

    archivo_combinado = os.path.join(NOTICIAS_DIR, "noticias_historicas_combinadas.csv")
    if os.path.exists(archivo_combinado):
        print(f"📂 Advertencia: usando archivo no procesado: {archivo_combinado}")
        return archivo_combinado

    archivos = sorted(glob(f"{NOTICIAS_DIR}/noticias_procesadas_*.csv"))
    if archivos:
        print(f"📂 Usando archivo reciente: {archivos[-1]}")
        return archivos[-1]

    raise FileNotFoundError("❌ No se encontraron archivos CSV de noticias.")

def entrenar_modelo_por_activo(df, activo):
    df_activo = df[df["activo"] == activo].copy()

    if df_activo.empty or len(df_activo["senal"].unique()) < 2:
        print(f"[{activo.upper()}] No hay suficientes datos o clases para entrenar.")
        return

    df_activo["sentimiento_encoded"] = df_activo["sentimiento"].map({"positivo": 1, "neutro": 0, "negativo": -1})
    X = df_activo[["score", "sentimiento_encoded"]]
    y = df_activo["senal"]

    y_encoded = y.astype("category").cat.codes
    etiquetas = dict(enumerate(y.astype("category").cat.categories))

    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.3, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    # Ajustar target_names a las clases presentes en y_test
    etiquetas_filtradas = {k: v for k, v in etiquetas.items() if k in np.unique(y_test)}
    target_names = [etiquetas_filtradas[k] for k in sorted(etiquetas_filtradas)]

    print(f"\n📊 Resultados para {activo.upper()}:")
    print(classification_report(y_test, y_pred, target_names=target_names))

    modelo_path = os.path.join(MODELOS_DIR, f"{activo}_modelo.pkl")
    etiquetas_path = os.path.join(MODELOS_DIR, f"{activo}_etiquetas.pkl")
    joblib.dump(model, modelo_path)
    joblib.dump(etiquetas, etiquetas_path)
    print(f"💾 Modelo guardado en: {modelo_path}")

    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=target_names, yticklabels=target_names)
    plt.title(f"Matriz de confusión: {activo.upper()}")
    plt.xlabel("Predicho")
    plt.ylabel("Real")
    plt.tight_layout()
    plt.show()

def main():
    archivo = cargar_csv_procesado()
    df = pd.read_csv(archivo)

    if "activo" not in df.columns or "senal" not in df.columns:
        print("⚠️ El archivo no contiene columnas 'activo' y 'senal'. Asegúrate de haber ejecutado el análisis previo.")
        return

    for activo in ["oro", "eurusd", "ibex35"]:
        entrenar_modelo_por_activo(df, activo)

if __name__ == "__main__":
    main()
