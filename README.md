
# 📈 trading_ai_indicator

**Indicador de trading intradía con inteligencia artificial** para activos como **oro (Gold), EUR/USD e IBEX 35**, integrando análisis de precios y noticias geopolíticas y económicas en tiempo real.

---

## 🚀 Funcionalidades (fase actual)
- ✅ Descarga de precios intradía cada 15 minutos desde Yahoo Finance (`yfinance`)
- ✅ Recolección de noticias relevantes vía `NewsAPI`
- 🔄 Guardado automático en CSV para histórico y backtesting
- 🧠 Preparado para integración de IA (análisis de sentimiento y predicción)

---

## 📁 Estructura del proyecto

```
trading_ai_indicator/
├── main.py
├── config.py
├── requirements.txt
├── data/
│   ├── precios/
│   └── noticias/
├── src/
│   ├── precios.py
│   ├── noticias.py
│   └── ...
```

---

## ⚙️ Requisitos

```bash
pip install -r requirements.txt
```

Asegúrate de tener una API Key de [https://newsapi.org](https://newsapi.org) y agregarla en `config.py`.

---

## ▶️ Ejecución

```bash
python main.py
```

Esto descargará:
- Datos intradía de Oro, EUR/USD e IBEX 35 (últimos 30 días)
- Noticias recientes relacionadas con dichos activos

---

## 🧠 Próximas funcionalidades

- Análisis de sentimiento en titulares (NLP con spaCy/NLTK)
- Modelo de predicción basado en ML (Random Forest / LSTM)
- Generador de señales de compra/venta
- Dashboard visual con Streamlit

---

## 🔐 Notas de seguridad

Agrega un archivo `.env` si deseas ocultar tu API Key:

```bash
NEWSAPI_KEY=tu_clave
```

Y carga con `python-dotenv`.

---

## 📄 Licencia

MIT © 2025 - Javier Tibamoza
