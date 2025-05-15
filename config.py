# config.py

TICKERS = {
    "oro": "GC=F",
    "eurusd": "EURUSD=X",
    "ibex35": "^IBEX"
}

NEWSAPI_KEY = "bf7c167d66ca4eef93579061bf4a98f0"  # Reemplázala o usa dotenv para cargar desde .env

NOTICIAS_QUERY = "gold OR euro OR ECB OR dollar OR Spain OR IBEX OR Bolsa OR Banco Central" #gold OR EUR/USD OR IBEX
NOTICIAS_LENGUAJE = "en"

DATA_DIR = "data"
PRECIOS_DIR = f"{DATA_DIR}/precios"
NOTICIAS_DIR = f"{DATA_DIR}/noticias"
