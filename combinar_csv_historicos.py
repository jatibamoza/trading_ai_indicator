
import os
import pandas as pd
from config import NOTICIAS_DIR

def combinar_csv_historicos():
    archivos = [f for f in os.listdir(NOTICIAS_DIR) if f.startswith("newsapi_") and f.endswith(".csv")]
    archivos.sort()

    dfs = []
    for archivo in archivos:
        path = os.path.join(NOTICIAS_DIR, archivo)
        df = pd.read_csv(path)
        df["origen_archivo"] = archivo
        dfs.append(df)

    if dfs:
        df_final = pd.concat(dfs, ignore_index=True)
        archivo_salida = os.path.join(NOTICIAS_DIR, "noticias_historicas_combinadas.csv")
        df_final.to_csv(archivo_salida, index=False)
        print(f"✅ Archivo combinado generado: {archivo_salida} ({len(df_final)} filas)")
    else:
        print("⚠️ No se encontraron archivos CSV históricos.")

if __name__ == "__main__":
    combinar_csv_historicos()
