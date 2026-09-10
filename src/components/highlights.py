"""Componente da aba de Destaques do Mercado (Overview Popular).

Apresenta rankings simples, intuitivos e populares para fácil entendimento
pelos alunos e público geral, aplicando conceitos centrais de Visualização de Informação.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.config import CATEGORY_COLOR_MAP, PLOTLY_CONFIG_MINIMAL, PLOTLY_CONFIG_PT_BR


def render_top_autonomy(df_filtrado: pd.DataFrame):
    """Renderiza o ranking dos 10 carros elétricos com maior autonomia homologada."""
    st.subheader(
        "Quem vai mais longe? (Top 10 Autonomia)",
        help="Os 10 modelos de carros elétricos que percorrem a maior distância com uma única carga completa (Inmetro).",
    )

    df_top = (
        df_filtrado.dropna(subset=["autonomia_inmetro_km"])
        .sort_values(by="autonomia_inmetro_km", ascending=False)
        .head(10)
        .copy()
    )

    if df_top.empty:
        st.info("Nenhum dado disponível para o ranking de autonomia.")
        return

    # Cria rótulo amigável combinando Marca, Modelo e Versão
    df_top["carro"] = df_top["marca"] + " " + df_top["modelo"] + " (" + df_top["versao"] + ")"
    # Ordena ascendente para a barra maior ficar no topo do gráfico horizontal
    df_top = df_top.sort_values(by="autonomia_inmetro_km", ascending=True)

    fig = px.bar(
        df_top,
        x="autonomia_inmetro_km",
        y="carro",
        orientation="h",
        color="categoria",
        color_discrete_map=CATEGORY_COLOR_MAP,
        labels={"autonomia_inmetro_km": "Autonomia Oficial (km)", "carro": "", "categoria": "Categoria"},
        template="plotly_white",
    )

    max_auto = df_top["autonomia_inmetro_km"].max()

    fig.update_traces(
        cliponaxis=False,
        text=df_top["autonomia_inmetro_km"].apply(lambda v: f"<b>{v:.0f} km</b>"),
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Autonomia: <b>%{x:.0f} km</b><br>Categoria: %{fullData.name}<extra></extra>",
    )

    fig.update_layout(
        height=420,
        margin=dict(l=10, r=60, t=35, b=30),
        showlegend=False,
        xaxis=dict(
            title="Autonomia Homologada (km)",
            ticksuffix=" km",
            range=[0, max_auto * 1.20],
            gridcolor="#f1f5f9",
        ),
        yaxis=dict(title="", tickfont=dict(size=11, color="#0f172a")),
        separators=",.",
    )

    st.plotly_chart(fig, width="stretch", config=PLOTLY_CONFIG_MINIMAL)


def render_top_efficiency(df_filtrado: pd.DataFrame):
    """Renderiza o ranking dos 10 carros mais econômicos na cidade em km/l equivalente."""
    st.subheader(
        "Quem gasta menos? (Top 10 Eficiência Urbana)",
        help="Os 10 modelos que mais rendem na cidade, convertidos para a métrica popular de km/l equivalente.",
    )

    df_top = (
        df_filtrado.dropna(subset=["km_l_equivalente_cidade"])
        .sort_values(by="km_l_equivalente_cidade", ascending=False)
        .head(10)
        .copy()
    )

    if df_top.empty:
        st.info("Nenhum dado disponível para o ranking de eficiência.")
        return

    df_top["carro"] = df_top["marca"] + " " + df_top["modelo"] + " (" + df_top["versao"] + ")"
    df_top = df_top.sort_values(by="km_l_equivalente_cidade", ascending=True)

    fig = px.bar(
        df_top,
        x="km_l_equivalente_cidade",
        y="carro",
        orientation="h",
        color="categoria",
        color_discrete_map=CATEGORY_COLOR_MAP,
        labels={"km_l_equivalente_cidade": "Rendimento Cidade (km/l equiv.)", "carro": "", "categoria": "Categoria"},
        template="plotly_white",
    )

    max_eff = df_top["km_l_equivalente_cidade"].max()

    fig.update_traces(
        cliponaxis=False,
        text=df_top["km_l_equivalente_cidade"].apply(lambda v: f"<b>{v:.1f} km/l</b>"),
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Rendimento Cidade: <b>%{x:.1f} km/l</b><br>Consumo: <b>%{customdata[0]:.2f} MJ/km</b><extra></extra>",
        customdata=df_top[["consumo_energetico_mj_km"]].values,
    )

    fig.update_layout(
        height=420,
        margin=dict(l=10, r=60, t=35, b=30),
        showlegend=False,
        xaxis=dict(
            title="Rendimento Equivalente na Cidade (km/l)",
            ticksuffix=" km/l",
            range=[0, max_eff * 1.20],
            gridcolor="#f1f5f9",
        ),
        yaxis=dict(title="", tickfont=dict(size=11, color="#0f172a")),
        separators=",.",
    )

    st.plotly_chart(fig, width="stretch", config=PLOTLY_CONFIG_MINIMAL)


def render_category_treemap(df_filtrado: pd.DataFrame):
    """Renderiza a composição do mercado por categoria oficial (Treemap Parte-Todo)."""
    st.subheader(
        "Que tipo de elétrico o brasileiro encontra?",
        help="Proporção da oferta de carros elétricos por categoria oficial (SUVs, compactos, sedãs, comerciais).",
    )

    cat_counts = df_filtrado["categoria"].value_counts().reset_index()
    cat_counts.columns = ["categoria", "quantidade"]

    if cat_counts.empty:
        st.info("Nenhum dado de categoria disponível.")
        return

    fig = px.treemap(
        cat_counts,
        path=["categoria"],
        values="quantidade",
        color="categoria",
        color_discrete_map=CATEGORY_COLOR_MAP,
        template="plotly_white",
    )

    fig.update_traces(
        textinfo="label+value+percent root",
        hovertemplate="<b>%{label}</b><br>Modelos homologados: <b>%{value}</b> (%{percentRoot:.1%})<extra></extra>",
        textfont=dict(size=13),
    )

    fig.update_layout(
        height=380,
        margin=dict(t=30, b=10, l=10, r=10),
    )

    st.plotly_chart(fig, width="stretch", config=PLOTLY_CONFIG_MINIMAL)


def render_popular_city_vs_road(df_filtrado: pd.DataFrame):
    """Renderiza a quebra de expectativa: comparativo Cidade vs. Estrada nos modelos mais eficientes."""
    st.subheader(
        "O Paradoxo Elétrico: Cidade vs. Estrada",
        help="Ao contrário dos carros a gasolina, os elétricos rendem muito mais na cidade graças à regeneração de energia nas frenagens.",
    )

    # Seleciona modelos únicos mais eficientes presentes no filtro ativo
    df_pop = (
        df_filtrado.dropna(subset=["km_l_equivalente_cidade", "km_l_equivalente_estrada"])
        .sort_values(by="km_l_equivalente_cidade", ascending=False)
        .drop_duplicates(subset=["modelo"])
        .head(6)
        .copy()
    )

    if df_pop.empty:
        st.info("Nenhum dado disponível para o comparativo de ciclo.")
        return

    df_pop["carro_curto"] = df_pop["marca"] + " " + df_pop["modelo"]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            name="Cidade (Urbano)",
            x=df_pop["carro_curto"],
            y=df_pop["km_l_equivalente_cidade"],
            marker_color="#00CC96",
            text=df_pop["km_l_equivalente_cidade"].apply(lambda v: f"{v:.1f}"),
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>Cidade: <b>%{y:.1f} km/l</b><extra></extra>",
        )
    )

    fig.add_trace(
        go.Bar(
            name="Estrada (Rodoviário)",
            x=df_pop["carro_curto"],
            y=df_pop["km_l_equivalente_estrada"],
            marker_color="#636EFA",
            text=df_pop["km_l_equivalente_estrada"].apply(lambda v: f"{v:.1f}"),
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>Estrada: <b>%{y:.1f} km/l</b><extra></extra>",
        )
    )

    max_y = max(df_pop["km_l_equivalente_cidade"].max(), df_pop["km_l_equivalente_estrada"].max())

    fig.update_layout(
        height=380,
        barmode="group",
        template="plotly_white",
        margin=dict(t=35, b=30, l=10, r=10),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.04,
            xanchor="left",
            x=0,
        ),
        yaxis=dict(
            title="Rendimento (km/l equiv.)",
            ticksuffix=" km/l",
            range=[0, max_y * 1.15],
            gridcolor="#f1f5f9",
        ),
        xaxis=dict(title="", tickfont=dict(size=11, color="#0f172a")),
        separators=",.",
    )

    st.plotly_chart(fig, width="stretch", config=PLOTLY_CONFIG_MINIMAL)


def render_highlights_tab(df_filtrado: pd.DataFrame):
    """Renderiza a aba inicial completa de Destaques do Mercado."""
    st.subheader(
        "Destaques do Mercado de Carros 100% Elétricos",
        help="Visão geral e rankings populares para entender rapidamente o cenário dos elétricos no Brasil.",
    )
    st.markdown(
        "Uma introdução rápida, simples e direta aos dados oficiais do **Inmetro**: "
        "descubra quem anda mais com uma única carga, quem gasta menos na tomada e como o mercado brasileiro está dividido."
    )

    # Linha 1: Rankings Top 10 lado a lado
    col1, col2 = st.columns(2)
    with col1:
        render_top_autonomy(df_filtrado)
    with col2:
        render_top_efficiency(df_filtrado)

    st.markdown("---")

    # Linha 2: Treemap de Categorias e Comparativo Urbano vs Rodoviário
    col3, col4 = st.columns(2)
    with col3:
        render_category_treemap(df_filtrado)
    with col4:
        render_popular_city_vs_road(df_filtrado)
