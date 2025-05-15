# src/visualizacion.py

import pandas as pd
import plotly.graph_objects as go
import numpy as np

def visualizar_precio_vs_noticias(df_precios, noticias):
    fig = go.Figure()

    # Gráfico de línea de precios
    fig.add_trace(go.Scatter(
        x=df_precios.index,
        y=df_precios['Close'],
        mode='lines',
        name='Precio Oro',
        line=dict(color='gold')
    ))

    # Agregar noticias como puntos
    for noticia in noticias:
        fecha = pd.to_datetime(noticia['fecha'])
        sentimiento = noticia['sentimiento']
        titulo = noticia['titulo']
        score = noticia['score']

        # Elegir color según sentimiento
        color = {'positivo': 'green', 'negativo': 'red', 'neutro': 'gray'}.get(sentimiento, 'blue')

        # Buscar precio más cercano a la hora de la noticia
        # precio_cercano = df_precios.iloc[(df_precios.index - fecha).abs().argsort()[:1]]['Close'].values[0]
        precio_cercano = df_precios.iloc[np.abs(df_precios.index - fecha).argmin()]["Close"]

        fig.add_trace(go.Scatter(
            x=[fecha],
            y=[precio_cercano],
            mode='markers',
            name=f"{sentimiento.capitalize()}",
            marker=dict(size=10, color=color),
            hovertext=titulo,
            showlegend=False
        ))

    fig.update_layout(
        title="Precio del Oro vs Noticias con Sentimiento",
        xaxis_title="Fecha y Hora",
        yaxis_title="Precio Oro (USD)",
        template="plotly_white"
    )

    return fig
