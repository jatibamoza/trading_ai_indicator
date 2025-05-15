
import plotly.graph_objects as go
import pandas as pd

def visualizar_precio_vs_noticias(df_precios, noticias, nombre_activo, unidad):
    fig = go.Figure()

    # Asegurar que el índice es datetime
    df_precios.index = pd.to_datetime(df_precios.index)

    # Añadir línea de precios
    fig.add_trace(go.Scatter(
        x=df_precios.index,
        y=df_precios["Close"],
        mode="lines",
        name=f"Precio {nombre_activo}",
        line=dict(width=2),
    ))

    # Colores por sentimiento
    colores = {
        "positivo": "green",
        "negativo": "red",
        "neutro": "gray"
    }

    # Añadir puntos de noticias con sentimiento
    for noticia in noticias:
        try:
            fecha = pd.to_datetime(noticia["fecha"])
        except Exception:
            continue  # Saltar noticias con fecha inválida

        sentimiento = noticia.get("sentimiento", "neutro")
        titulo = noticia.get("titulo", "")
        color = colores.get(sentimiento, "gray")

        try:
            if fecha in df_precios.index:
                precio_cercano = df_precios.loc[fecha]["Close"]
            else:
                fecha_mas_cercana = df_precios.index.get_indexer([fecha], method="nearest")[0]
                precio_cercano = df_precios.iloc[fecha_mas_cercana]["Close"]
        except Exception:
            continue  # Si no se encuentra fecha cercana, saltar

        fig.add_trace(go.Scatter(
            x=[fecha],
            y=[precio_cercano],
            mode="markers+text",
            marker=dict(size=10, color=color, symbol="star"),
            name=f"{sentimiento.capitalize()}",
            text=[titulo],
            textposition="top center",
            showlegend=False
        ))

    fig.update_layout(
        title=f"Precio de {nombre_activo} vs Noticias con Sentimiento",
        xaxis_title="Fecha y Hora",
        yaxis_title=f"Precio {nombre_activo} ({unidad})",
        height=500
    )

    return fig
