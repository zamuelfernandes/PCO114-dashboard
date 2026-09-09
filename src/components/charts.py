"""
Componente de geração e renderização dos gráficos analíticos Plotly.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.config import CATEGORY_COLOR_MAP, PLOTLY_CONFIG_PT_BR


def render_scatter_chart(df_filtrado: pd.DataFrame):
    """Renderiza o gráfico de dispersão: Preço vs. Autonomia."""
    st.subheader(
        "Relação Preço vs. Autonomia (Inmetro)",
        help=(
            "Analisa a eficiência de custo por alcance: o eixo horizontal mostra a autonomia oficial (Inmetro) "
            "e o vertical o preço estimado de tabela. O tamanho de cada bolha representa a potência do motor (cv). "
            "Passe o mouse sobre os veículos para visualizar a ficha técnica detalhada."
        ),
    )

    fig_scatter = px.scatter(
        df_filtrado,
        x="autonomia_inmetro_km",
        y="preco_estimado_brl",
        color="categoria",
        color_discrete_map=CATEGORY_COLOR_MAP,
        size="potencia_cv",
        custom_data=[
            "marca",
            "modelo",
            "versao",
            "categoria",
            "potencia_cv",
            "capacidade_bateria_kwh",
            "tempo_recarga_rapida_min",
            "tipo_conector",
            "tracao",
        ],
        labels={
            "autonomia_inmetro_km": "Autonomia Inmetro",
            "preco_estimado_brl": "Preço Estimado",
            "categoria": "Categoria",
        },
        title="Preço vs. Autonomia (Tamanho da bolha = Potência)",
        template="plotly_white",
    )

    fig_scatter.update_traces(
        hovertemplate=(
            "<b>%{customdata[0]} %{customdata[1]}</b><br>"
            "<b>Versão:</b> %{customdata[2]}<br>"
            "<b>Categoria:</b> %{customdata[3]}<br>"
            "<br>"
            "<b>Preço Estimado:</b> R$ %{y:,.2f}<br>"
            "<b>Autonomia Inmetro:</b> %{x} km<br>"
            "<b>Potência:</b> %{customdata[4]} cv<br>"
            "<b>Bateria:</b> %{customdata[5]} kWh<br>"
            "<b>Recarga Rápida:</b> %{customdata[6]} min<br>"
            "<b>Conector:</b> %{customdata[7]} | <b>Tração:</b> %{customdata[8]}"
            "<extra></extra>"
        )
    )

    fig_scatter.update_layout(
        height=520,
        separators=",.",
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="sans-serif",
            bordercolor="#cbd5e1",
        ),
        xaxis=dict(
            title="Autonomia Homologada Inmetro",
            ticksuffix=" km",
            gridcolor="#f1f5f9",
        ),
        yaxis=dict(
            title="Preço Estimado",
            tickprefix="R$ ",
            tickformat=",.0f",
            gridcolor="#f1f5f9",
        ),
        legend=dict(
            title_text="Categoria",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
    )

    st.plotly_chart(fig_scatter, width="stretch", config=PLOTLY_CONFIG_PT_BR)


def render_bar_chart(df_filtrado: pd.DataFrame, altura: int):
    """Renderiza o gráfico de barras: Quantidade de modelos por fabricante com cores por categoria."""
    st.subheader(
        "Modelos por Marca",
        help=(
            "Ranking de fabricantes pela quantidade total de modelos 100% elétricos comercializados no Brasil. "
            "As cores dos segmentos correspondem às categorias dos veículos (Subcompacto, Hatchback, SUV e Sedan), "
            "e os números na ponta de cada barra indicam o total de veículos por marca."
        ),
    )

    # Segmentação por marca e categoria para correlação de cores
    modelos_por_marca_cat = (
        df_filtrado.groupby(["marca", "categoria"])
        .size()
        .reset_index(name="quantidade")
    )

    # Ordenação das marcas pelo total de veículos em ordem crescente
    total_por_marca = (
        df_filtrado.groupby("marca")
        .size()
        .sort_values(ascending=True)
    )
    ordem_marcas = total_por_marca.index.tolist()
    max_qtd = int(total_por_marca.max()) if not total_por_marca.empty else 5

    fig_bar = px.bar(
        modelos_por_marca_cat,
        x="quantidade",
        y="marca",
        color="categoria",
        color_discrete_map=CATEGORY_COLOR_MAP,
        orientation="h",
        labels={"quantidade": "Qtd. de Modelos", "marca": "Fabricante", "categoria": "Categoria"},
        title="Quantidade de Modelos por Fabricante",
        template="plotly_white",
        category_orders={"marca": ordem_marcas},
    )

    fig_bar.update_traces(
        cliponaxis=False,
        hovertemplate="<b>%{y}</b><br>Categoria: <b>%{fullData.name}</b><br>Modelos nesta categoria: <b>%{x}</b><extra></extra>",
    )

    # Rótulo com o total geral fixado na ponta de cada barra
    for marca, total in total_por_marca.items():
        fig_bar.add_annotation(
            x=total + 0.12,
            y=marca,
            text=str(total),
            showarrow=False,
            xanchor="left",
            yanchor="middle",
            font=dict(size=12, color="#0f172a"),
        )

    fig_bar.update_layout(
        height=altura,
        showlegend=False,
        margin=dict(l=10, r=35, t=40, b=30),
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="sans-serif",
            bordercolor="#cbd5e1",
        ),
        xaxis=dict(
            title="Número de Modelos",
            dtick=1,
            range=[0, max_qtd + 0.8],
            gridcolor="#f1f5f9",
        ),
        yaxis=dict(title="", tickfont=dict(size=12, color="#0f172a")),
    )

    st.plotly_chart(fig_bar, width="stretch", config=PLOTLY_CONFIG_PT_BR)


def render_box_chart(df_filtrado: pd.DataFrame, altura: int):
    """Renderiza o gráfico de distribuição de preços por categoria com estilo nativo e rótulos em português."""
    st.subheader(
        "Faixa de Preço por Categoria",
        help=(
            "Distribuição e amplitude de preços por carroceria (Subcompacto, Hatchback, SUV e Sedan). "
            "A caixa representa o intervalo interquartil (Q1 a Q3), a linha central indica a mediana, "
            "e as hastes mostram os limites inferior e superior de preços."
        ),
    )

    fig_box = px.box(
        df_filtrado,
        x="categoria",
        y="preco_estimado_brl",
        color="categoria",
        color_discrete_map=CATEGORY_COLOR_MAP,
        points="outliers",
        labels={
            "categoria": "Categoria",
            "preco_estimado_brl": "Preço Estimado",
        },
        title="Distribuição de Preços por Categoria",
        template="plotly_white",
    )

    fig_box.update_layout(
        height=altura,
        showlegend=False,
        separators=",.",
        yaxis=dict(
            title="Preço Estimado",
            tickprefix="R$ ",
            tickformat=",.0f",
            gridcolor="#f1f5f9",
        ),
        xaxis=dict(title=""),
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="sans-serif",
            bordercolor="#cbd5e1",
        ),
    )

    st.plotly_chart(fig_box, width="stretch", config=PLOTLY_CONFIG_PT_BR)


def render_charts(df_filtrado: pd.DataFrame):
    """Renderiza a seção completa de visualizações analíticas em gráficos."""
    render_scatter_chart(df_filtrado)

    # Gráficos complementares em 2 colunas com altura harmonizada
    col_g1, col_g2 = st.columns(2)
    qtd_marcas = df_filtrado["marca"].nunique()
    altura_graficos = max(420, qtd_marcas * 32 + 60)

    with col_g1:
        render_bar_chart(df_filtrado, altura_graficos)

    with col_g2:
        render_box_chart(df_filtrado, altura_graficos)
