from datetime import datetime

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


NUMERO_DE_SEMANAS = 43
URL = "https://raw.githubusercontent.com/globaldothealth/monkeypox/main/timeseries-confirmed.csv"


def main():

    conf_df = pd.read_csv(URL, parse_dates=["Date"], index_col="Date")

    conf_titulo = f"{conf_df['Cumulative_cases'][-1]:,.0f} casos confirmados totales<br>+{conf_df['Cases'][-1]:,.0f} el {conf_df.index[-1]:%d-%m-%Y}"

    conf_df = conf_df.resample("W").sum()
    conf_df = conf_df[-NUMERO_DE_SEMANAS:]

    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1)

    fig.add_trace(
        go.Scatter(x=conf_df.index,
                   y=conf_df["Cases"],
                   mode="lines",
                   line_color="#c6ff00",
                   line_width=5,
                   fill="tozeroy"), col=1, row=1)

    fig.update_xaxes(
        tickformat="%d-%m<br>'%y",
        ticks="outside",
        ticklen=10,
        zeroline=False,
        tickcolor="#FFFFFF",
        linewidth=2,
        gridwidth=0.5,
        showline=True,
        mirror=True,
        nticks=10
    )

    fig.update_yaxes(
        ticks="outside",
        ticklen=10,
        tickcolor="#FFFFFF",
        linewidth=2,
        gridwidth=0.5,
        showline=True,
        mirror=True,
        nticks=14
    )

    fig.update_yaxes(title="Casos confirmados semanales", row=1, col=1)
    fig.update_yaxes(title="Defunciones reportadas semanales", row=1, col=2)

    fig.update_layout(
        showlegend=False,
        width=1280,
        height=500,
        font_color="white",
        font_size=14,
        margin_t=120,
        margin_l=110,
        margin_r=40,
        margin_b=120,
        title_text="Casos confirmados de viruela símica en el Mundo",
        title_x=0.5,
        title_y=0.95,
        title_font_size=24,
        paper_bgcolor="#1E1E1E",
        plot_bgcolor="#20252f",
        annotations=[
            dict(
                x=0.23,
                y=1.08,
                xanchor="center",
                yanchor="top",
                xref="paper",
                yref="paper",
                text=conf_titulo
            ),            
            dict(
                x=0.5,
                y=-0.4,
                xanchor="center",
                yanchor="top",
                xref="paper",
                yref="paper",
                text=f"Actualizado el {datetime.now():%d-%m-%Y}"
            )
        ]
    )

    fig.write_image("./2.png")


if __name__ == "__main__":

    main()
