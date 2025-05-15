# procesar_csv_antiguo.py

import pandas as pd
from src.procesamiento import analizar_sentimiento

# Carga el CSV antiguo sin análisis
archivo_original = "data/noticias/noticias_20250515_1024.csv"
df = pd.read_csv(archivo_original)

# Asegúrate de tener 'titulo' y 'descripcion' en las columnas
noticias = df.to_dict(orient="records")

# Aplica el análisis de sentimiento
noticias_procesadas = analizar_sentimiento(noticias)

# Guarda el nuevo archivo con score y sentimiento
archivo_nuevo = archivo_original.replace(".csv", "_con_sentimiento.csv")
pd.DataFrame(noticias_procesadas).to_csv(archivo_nuevo, index=False)

print(f"Archivo guardado: {archivo_nuevo}")
