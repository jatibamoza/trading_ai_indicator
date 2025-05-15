
# 📈 Proyecto: Predicción de Señales de Trading con IA + Sentimiento

Este proyecto utiliza **noticias económicas** y su **análisis de sentimiento** para predecir señales de trading (BUY / SELL / HOLD) para tres activos clave:

- **Oro (`GC=F`)**
- **EUR/USD (`EURUSD=X`)**
- **IBEX 35 (`^IBEX`)**

---

## 🧠 ¿Qué hace?

1. Descarga noticias recientes desde NewsAPI + Investing.com
2. Analiza el sentimiento con `TextBlob` (`positivo`, `negativo`, `neutro`)
3. Asocia noticias a activos específicos
4. Obtiene precios históricos con `yfinance`
5. Entrena modelos de Machine Learning (Random Forest) por activo
6. Usa los modelos entrenados para predecir señales de trading en tiempo real
7. Muestra gráficos y métricas en un dashboard con Streamlit

---

## 🚀 Cómo usar

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Configura tu API key en `config.py`

```python
NEWSAPI_KEY = "TU_CLAVE_AQUI"
```

### 3. Descargar noticias históricas (últimos 30 días)

```bash
python noticias_historicas.py
```

### 4. Combinar en un solo archivo

```bash
python combinar_csv_historicos.py
```

### 5. Procesar noticias y entrenar el modelo

```bash
python modelo.py
```

Esto guardará los modelos `.pkl` en `data/modelos/`.

---

### 6. Ejecutar la app en Streamlit

```bash
streamlit run visualizador_noticias.py
```

---

## 🧩 Estructura del proyecto

```
src/
├── noticias.py              # Obtener noticias actuales
├── scraper_investing.py    # Scraper básico para Investing.com
├── procesamiento.py        # Análisis de sentimiento
├── senales.py              # Métricas heurísticas
├── modelo_predictor.py     # Predicción en tiempo real con modelos .pkl
├── visualizacion.py        # Generar gráficos con Plotly
config.py                   # API keys y rutas
visualizador_noticias.py    # Interfaz principal Streamlit
modelo.py                   # Entrenamiento de modelos IA
noticias_historicas.py      # Obtener noticias antiguas de NewsAPI
combinar_csv_historicos.py  # Combinar noticias por día en un CSV único
```

---

## 📌 Requisitos

- Python 3.8+
- Clave válida de [newsapi.org](https://newsapi.org/)
- Cuenta en [Streamlit Cloud](https://streamlit.io/cloud) (opcional para desplegar online)

---

## ✅ Roadmap (siguientes pasos)

- Añadir scraping histórico completo desde Investing
- Entrenar con noticias traducidas multilingües
- Exportar señales como API REST o alertas por email
- Entrenar modelos más avanzados (XGBoost, LSTM...)

---

## 📬 Autor

Desarrollado por Javier Tibamoza con integración de análisis financiero y técnicas de IA.
