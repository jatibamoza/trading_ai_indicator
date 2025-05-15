# config.py

TICKERS = {
    "oro": "GC=F",
    "eurusd": "EURUSD=X",
    "ibex35": "^IBEX"
}

NEWSAPI_KEY = "TU_API_KEY_AQUI"  # Reemplázala o usa dotenv para cargar desde .env

NOTICIAS_QUERY = "gold OR EUR/USD OR IBEX"
NOTICIAS_LENGUAJE = "en"

DATA_DIR = "data"
PRECIOS_DIR = f"{DATA_DIR}/precios"
NOTICIAS_DIR = f"{DATA_DIR}/noticias"
