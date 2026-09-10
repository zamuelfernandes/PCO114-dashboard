"""Módulo de carregamento, cache e filtragem de dados oficiais PBEV / Inmetro."""

from pathlib import Path
import pandas as pd
import streamlit as st


def _get_file_signature(csv_path: Path) -> tuple[float, int]:
    """Retorna (mtime, size) do arquivo para invalidar o cache automaticamente quando o arquivo mudar no disco."""
    if not csv_path.exists():
        return (0.0, 0)
    try:
        stat = csv_path.stat()
        return (stat.st_mtime, stat.st_size)
    except OSError:
        return (0.0, 0)


@st.cache_data
def _load_data_cached(csv_path: Path, file_signature: tuple[float, int]) -> pd.DataFrame:
    """Lê o arquivo CSV oficial em cache, usando o signature (mtime, size) como chave de invalidação."""
    df = pd.read_csv(csv_path)
    colunas_numericas = [
        "autonomia_inmetro_km",
        "consumo_energetico_mj_km",
        "km_l_equivalente_cidade",
        "km_l_equivalente_estrada",
        "emissao_co2_g_km",
    ]
    for col in colunas_numericas:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def load_data(csv_path: Path) -> pd.DataFrame | None:
    """Carrega o arquivo CSV oficial de forma segura.

    Retorna None se o arquivo não existir ou estiver vazio (sem armazenar None no cache).
    """
    sig = _get_file_signature(csv_path)
    if sig[1] == 0:
        return None

    try:
        df = _load_data_cached(csv_path, sig)
        if df is None or df.empty or len(df.columns) == 0:
            return None
        return df
    except (pd.errors.EmptyDataError, FileNotFoundError, Exception):
        return None


def filter_data(df_raw: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """Aplica os filtros selecionados na barra lateral sobre o DataFrame bruto."""
    df = df_raw.copy()

    # 1. Filtro por marca
    if "marcas" in filters and filters["marcas"]:
        df = df[df["marca"].isin(filters["marcas"])]

    # 2. Filtro por categoria
    if "categorias" in filters and filters["categorias"]:
        df = df[df["categoria"].isin(filters["categorias"])]

    # 3. Filtro por consumo energético máximo (MJ/km)
    if "consumo_max" in filters and filters["consumo_max"] is not None:
        df = df[df["consumo_energetico_mj_km"] <= filters["consumo_max"]]

    # 4. Filtro por autonomia mínima (km)
    if "auto_min" in filters and filters["auto_min"] is not None:
        df = df[df["autonomia_inmetro_km"] >= filters["auto_min"]]

    return df
