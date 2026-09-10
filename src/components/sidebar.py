"""Componente da barra lateral para controles e filtros interativos com base nos dados do Inmetro."""

import pandas as pd
import streamlit as st


def render_sidebar(df_raw: pd.DataFrame) -> dict:
    """Renderiza os controles de filtro na barra lateral e retorna as opções selecionadas."""
    st.sidebar.title(":material/tune: Filtros")
    st.sidebar.markdown("Refine os veículos 100% elétricos homologados no PBEV:")

    # 1. Filtro por Marca (inicia com as 5 principais marcas por volume de modelos elétricos)
    marcas_disponiveis = sorted(df_raw["marca"].unique())
    top_5_marcas = df_raw["marca"].value_counts().head(5).index.tolist()
    default_marcas = [m for m in marcas_disponiveis if m in top_5_marcas]

    marcas_selecionadas = st.sidebar.multiselect(
        "Marca / Montadora:",
        options=marcas_disponiveis,
        default=default_marcas,
        help="Selecione uma ou mais fabricantes para comparar (inicia pré-selecionado com as 5 principais marcas).",
    )

    # 2. Filtro por Categoria Oficial Inmetro (inicia com as 5 principais categorias)
    categorias_disponiveis = sorted(df_raw["categoria"].unique())
    top_5_categorias = df_raw["categoria"].value_counts().head(5).index.tolist()
    default_categorias = [c for c in categorias_disponiveis if c in top_5_categorias]

    categorias_selecionadas = st.sidebar.multiselect(
        "Categoria Oficial (Inmetro):",
        options=categorias_disponiveis,
        default=default_categorias,
        help="Categorias normatizadas pelo PBEV (inicia pré-selecionado com as 5 principais categorias).",
    )

    # 3. Filtro por Autonomia Mínima Inmetro (km)
    auto_min_raw = int(df_raw["autonomia_inmetro_km"].min())
    auto_max_raw = int(df_raw["autonomia_inmetro_km"].max())
    auto_limite = st.sidebar.slider(
        "Autonomia Mínima (km):",
        min_value=auto_min_raw,
        max_value=auto_max_raw,
        value=auto_min_raw,
        step=10,
        format="%d km",
        help="Filtra veículos com alcance homologado pelo Inmetro igual ou superior ao estipulado.",
    )

    # 4. Filtro por Consumo Energético Máximo (MJ/km)
    consumo_min = float(df_raw["consumo_energetico_mj_km"].min())
    consumo_max = float(df_raw["consumo_energetico_mj_km"].max())
    consumo_limite = st.sidebar.slider(
        "Consumo Energético Máximo (MJ/km):",
        min_value=round(consumo_min, 2),
        max_value=round(consumo_max, 2),
        value=round(consumo_max, 2),
        step=0.01,
        format="%.2f MJ/km",
        help="Quanto menor o valor em MJ/km, mais eficiente é o veículo elétrico.",
    )

    return {
        "marcas": marcas_selecionadas,
        "categorias": categorias_selecionadas,
        "auto_min": auto_limite,
        "consumo_max": consumo_limite,
    }
