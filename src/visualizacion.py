
import pandas as pd
import plotly.graph_objects as go

def visualizar_precio_vs_noticias(df_precios, noticias, nombre_activo="Activo", unidad="USD"):
    fig = go.Figure()

    # Gráfico de línea de precios
    fig.add_trace(go.Scatter(
        x=df_precios.index,
        y=df_precios['Close'],
        mode='lines',
        name=f'Precio {nombre_activo}',
        line=dict(color='gold')
    ))

    # Agregar puntos de noticias
    for noticia in noticias:
        fecha = pd.to_datetime(noticia['fecha'])
        sentimiento = noticia['sentimiento']
        titulo = noticia['titulo']
        score = noticia.get('score', 0.0)

        color = {'positivo': 'green', 'negativo': 'red', 'neutro': 'gray'}.get(sentimiento, 'blue')

        # Buscar precio más cercano
        if not df_precios.empty:
            precio_cercano = df_precios.iloc[(df_precios.index - fecha).abs().argsort()[:1]]['Close'].values[0]

            fig.add_trace(go.Scatter(
                x=[fecha],
                y=[precio_cercano],
                mode='markers',
                name=f'{sentimiento.capitalize()}',
                marker=dict(size=10, color=color),
                hovertext=f'{titulo}<br>Score: {score:.2f}',
                showlegend=False
            ))

    fig.update_layout(
        title=f"Precio de {nombre_activo} vs Noticias con Sentimiento",
        xaxis_title="Fecha y Hora",
        yaxis_title=f"Precio {nombre_activo} ({unidad})",
        template="plotly_white"
    )

    return fig
