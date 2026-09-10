"""Componente de exibição de cartões de métricas (KPIs) oficiais do Inmetro."""

import pandas as pd
import streamlit as st


from src.config import CATEGORY_COLOR_MAP


def render_category_legend(df_filtrado: pd.DataFrame):
    """Renderiza a barra fixa de legenda global de categorias do Inmetro presente na base filtrada."""
    categorias_presentes = [
        cat for cat in CATEGORY_COLOR_MAP.keys()
        if cat in df_filtrado["categoria"].values
    ]
    if not categorias_presentes:
        return

    items_html = []
    for cat in categorias_presentes:
        cor = CATEGORY_COLOR_MAP[cat]
        items_html.append(
            f'<span style="display: inline-flex; align-items: center; margin-right: 18px; margin-top: 3px; margin-bottom: 3px; font-size: 0.82rem; color: #1e293b; font-weight: 600;">'
            f'<span style="display: inline-block; width: 11px; height: 11px; border-radius: 50%; background-color: {cor}; margin-right: 6px; box-shadow: 0 1px 2px rgba(0,0,0,0.15);"></span>'
            f'{cat}'
            f'</span>'
        )

    legend_html = f"""
    <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 8px 14px; margin-top: 10px; display: flex; flex-wrap: wrap; align-items: center;">
        <span style="font-size: 0.76rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; margin-right: 14px;">
            Cores por Categoria:
        </span>
        {''.join(items_html)}
    </div>
    """
    st.markdown(legend_html, unsafe_allow_html=True)


def render_kpis(df_filtrado: pd.DataFrame):
    """Renderiza os 4 cartões principais de métricas com dados reais homologados pelo Inmetro e a legenda global de categorias."""
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

    # Legenda global de cores por categoria (visível em todas as abas)
    render_category_legend(df_filtrado)
