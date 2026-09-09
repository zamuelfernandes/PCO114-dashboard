"""
Componente da barra lateral para controles e filtros interativos.
"""

import pandas as pd
import streamlit as st


def render_sidebar(df_raw: pd.DataFrame) -> dict:
    """Renderiza os controles de filtro na barra lateral e retorna as opções selecionadas."""
    st.sidebar.title(":material/tune: Filtros")
    st.sidebar.markdown("Refine os veículos exibidos no dashboard:")

    # Filtro por Marca
    marcas_disponiveis = sorted(df_raw["marca"].unique())
    marcas_selecionadas = st.sidebar.multiselect(
        "Marca:",
        options=marcas_disponiveis,
        default=marcas_disponiveis,
        help="Selecione uma ou mais fabricantes para comparar",
    )

    # Filtro por Categoria
    categorias_disponiveis = sorted(df_raw["categoria"].unique())
    categorias_selecionadas = st.sidebar.multiselect(
        "Categoria da Carroceria:",
        options=categorias_disponiveis,
        default=categorias_disponiveis,
        help="Selecione os tipos de carroceria (Hatchback, SUV, Sedan, Subcompacto)",
    )

    # Filtro por Faixa de Preço
    preco_min = float(df_raw["preco_estimado_brl"].min())
    preco_max = float(df_raw["preco_estimado_brl"].max())
    preco_limite = st.sidebar.slider(
        "Preço Máximo Estimado (R$):",
        min_value=preco_min,
        max_value=preco_max,
        value=preco_max,
        step=10000.0,
        format="R$ %'.,.0f",
        help="Filtra veículos com preço de tabela até o valor estipulado",
    )

    # Filtro por Autonomia Mínima
    auto_min = int(df_raw["autonomia_inmetro_km"].min())
    auto_max = int(df_raw["autonomia_inmetro_km"].max())
    auto_limite = st.sidebar.slider(
        "Autonomia Mínima Inmetro (km):",
        min_value=auto_min,
        max_value=auto_max,
        value=auto_min,
        step=10,
        format="%d km",
        help="Filtra veículos com autonomia homologada igual ou superior à selecionada",
    )

    return {
        "marcas": marcas_selecionadas,
        "categorias": categorias_selecionadas,
        "preco_max": preco_limite,
        "auto_min": auto_limite,
    }
