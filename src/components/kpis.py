"""
Componente de exibição de cartões de métricas (KPIs).
"""

import pandas as pd
import streamlit as st


def render_kpis(df_filtrado: pd.DataFrame):
    """Renderiza os 4 cartões principais de métricas com question tags informativas."""
    col1, col2, col3, col4 = st.columns(4)

    total_modelos = len(df_filtrado)
    preco_medio = df_filtrado["preco_estimado_brl"].mean()
    autonomia_media = df_filtrado["autonomia_inmetro_km"].mean()
    melhor_autonomia_row = df_filtrado.loc[df_filtrado["autonomia_inmetro_km"].idxmax()]

    with col1:
        st.metric(
            label="Modelos Filtrados",
            value=f"{total_modelos}",
            help="Total de veículos elétricos que atendem aos filtros selecionados na barra lateral.",
        )

    with col2:
        st.metric(
            label="Preço Médio",
            value=f"R$ {preco_medio:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            help="Média aritmética do preço estimado de tabela dos veículos filtrados.",
        )

    with col3:
        st.metric(
            label="Autonomia Média",
            value=f"{autonomia_media:.0f} km",
            help="Alcance médio oficial homologado pelo Programa Brasileiro de Etiquetagem Veicular (PBEV / Inmetro).",
        )

    with col4:
        st.metric(
            label="Maior Autonomia",
            value=f"{melhor_autonomia_row['autonomia_inmetro_km']} km",
            help=f"Veículo com maior autonomia no filtro: {melhor_autonomia_row['marca']} {melhor_autonomia_row['modelo']} ({melhor_autonomia_row['versao']}).",
        )
