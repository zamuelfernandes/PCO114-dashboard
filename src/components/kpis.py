"""Componente de exibição de cartões de métricas (KPIs) oficiais do Inmetro."""

import pandas as pd
import streamlit as st


def render_kpis(df_filtrado: pd.DataFrame):
    """Renderiza os 4 cartões principais de métricas com dados reais homologados pelo Inmetro."""
    col1, col2, col3, col4 = st.columns(4)

    total_modelos = len(df_filtrado)

    autonomia_media = df_filtrado["autonomia_inmetro_km"].mean()
    autonomia_media_val = f"{autonomia_media:.0f} km" if pd.notna(autonomia_media) else "N/A"

    best_auto_row = df_filtrado.loc[df_filtrado["autonomia_inmetro_km"].idxmax()]
    melhor_autonomia_val = f"{best_auto_row['autonomia_inmetro_km']:.0f} km"
    melhor_autonomia_help = (
        f"Veículo com maior alcance no filtro: {best_auto_row['marca']} {best_auto_row['modelo']} "
        f"({best_auto_row['versao']})."
    )

    consumo_medio = df_filtrado["consumo_energetico_mj_km"].mean()
    consumo_medio_val = f"{consumo_medio:.2f} MJ/km" if pd.notna(consumo_medio) else "N/A"

    with col1:
        st.metric(
            label="Modelos Elétricos",
            value=f"{total_modelos}",
            help="Total de veículos 100% elétricos homologados no PBEV / Inmetro que atendem aos filtros ativos.",
        )

    with col2:
        st.metric(
            label="Autonomia Média",
            value=autonomia_media_val,
            help="Alcance médio oficial homologado pelo Inmetro para os veículos 100% elétricos selecionados.",
        )

    with col3:
        st.metric(
            label="Consumo Médio",
            value=consumo_medio_val,
            help="Consumo energético médio oficial em Megajoules por quilômetro (MJ/km). Quanto menor o número, maior a eficiência energética.",
        )

    with col4:
        st.metric(
            label="Maior Autonomia",
            value=melhor_autonomia_val,
            help=melhor_autonomia_help,
        )
