
import os
import pandas as pd
import numpy as np
from glob import glob
from datetime import datetime

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

from config import NOTICIAS_DIR

def cargar_csv_mas_reciente():
    archivos = sorted(glob(f"{NOTICIAS_DIR}/noticias_procesadas_*.csv"))
    if not archivos:
        raise FileNotFoundError("No se encontraron archivos CSV de noticias procesadas.")
    return archivos[-1]

def entrenar_modelo_por_activo(df, activo):
    df_activo = df[df["activo"] == activo].copy()

    if df_activo.empty or len(df_activo["senal"].unique()) < 2:
        print(f"[{activo.upper()}] No hay suficientes datos o clases para entrenar.")
        return

    # Features simples: score y sentimiento
    df_activo["sentimiento_encoded"] = df_activo["sentimiento"].map({"positivo": 1, "neutro": 0, "negativo": -1})
    X = df_activo[["score", "sentimiento_encoded"]]
    y = df_activo["senal"]

    # Codificar etiquetas
    y_encoded = y.astype("category").cat.codes
    etiquetas = dict(enumerate(y.astype("category").cat.categories))

    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.3, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print(f"\n📊 Resultados para {activo.upper()}:")
    print(classification_report(y_test, y_pred, target_names=etiquetas.values()))

    # Matriz de confusión
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(5,4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=etiquetas.values(), yticklabels=etiquetas.values())
    plt.title(f"Matriz de confusión: {activo.upper()}")
    plt.xlabel("Predicho")
    plt.ylabel("Real")
    plt.tight_layout()
    plt.show()

def main():
    archivo = cargar_csv_mas_reciente()
    print(f"📂 Usando archivo: {archivo}")
    df = pd.read_csv(archivo)

    for activo in ["oro", "eurusd", "ibex35"]:
        entrenar_modelo_por_activo(df, activo)

if __name__ == "__main__":
    main()
