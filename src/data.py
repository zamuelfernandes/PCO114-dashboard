"""
Módulo de carregamento, cache e filtragem de dados.
"""

from pathlib import Path
import pandas as pd
import streamlit as st


@st.cache_data
def load_data(csv_path: Path) -> pd.DataFrame:
    """Carrega o arquivo CSV e ajusta tipos de dados para análise."""
    df = pd.read_csv(csv_path)
    df["preco_estimado_brl"] = df["preco_estimado_brl"].astype(float)
    df["autonomia_inmetro_km"] = df["autonomia_inmetro_km"].astype(int)
    df["potencia_cv"] = df["potencia_cv"].astype(int)
    df["capacidade_bateria_kwh"] = df["capacidade_bateria_kwh"].astype(float)
    return df


def filter_data(df_raw: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """Aplica os filtros selecionados na barra lateral sobre o DataFrame bruto."""
    return df_raw[
        (df_raw["marca"].isin(filters["marcas"]))
        & (df_raw["categoria"].isin(filters["categorias"]))
        & (df_raw["preco_estimado_brl"] <= filters["preco_max"])
        & (df_raw["autonomia_inmetro_km"] >= filters["auto_min"])
    ]
