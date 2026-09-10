#!/usr/bin/env python3
"""Etapa 03: Processamento e Padronização dos Dados de Veículos 100% Elétricos (Inmetro PBEV).

Lê o CSV bruto extraído da etapa 02, filtra veículos 100% elétricos (BEV),
padroniza nomes de montadoras, categorias oficiais do Inmetro, converte métricas
numéricas (autonomia, consumo MJ/km, km/l equivalente, emissões CO2) e salva o
dataset final em data/carros_eletricos_brasil.csv.
"""

import argparse
import logging
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# Mapeamento e padronização oficial de marcas
BRAND_MAP = {
    "AUDI": "Audi",
    "BMW": "BMW",
    "BYD": "BYD",
    "CAOA CHANGAN": "CAOA Changan",
    "CAOACHANGAN": "CAOA Changan",
    "CAOA CHERY": "CAOA Chery",
    "CHEVROLET": "Chevrolet",
    "CITROEN": "Citroën",
    "DENZA": "Denza",
    "FARIZON": "Farizon",
    "FERRARI": "Ferrari",
    "FIAT": "Fiat",
    "FORD": "Ford",
    "FOTON": "Foton",
    "GAC": "GAC",
    "GEELY": "Geely",
    "Geely": "Geely",
    "GWM": "GWM",
    "HONDA": "Honda",
    "HYUNDAI": "Hyundai",
    "Hyundai": "Hyundai",
    "JAC": "JAC",
    "JAECOO": "Jaecoo",
    "JEEP": "Jeep",
    "JETOUR": "Jetour",
    "KIA": "Kia",
    "LAND ROVER": "Land Rover",
    "LEAPMOTOR": "Leapmotor",
    "LEXUS": "Lexus",
    "MCLAREN": "McLaren",
    "MERCEDES-BENZ": "Mercedes-Benz",
    "Mercedes-Benz": "Mercedes-Benz",
    "MG": "MG",
    "MINI": "Mini",
    "Mitsubishi": "Mitsubishi",
    "OMODA": "Omoda",
    "PEUGEOT": "Peugeot",
    "PORSCHE": "Porsche",
    "RENAULT": "Renault",
    "SUZUKI": "Suzuki",
    "TOYOTA": "Toyota",
    "VOLVO": "Volvo",
    "ZEEKR": "Zeekr",
}

# Mapeamento oficial de categorias Inmetro
CATEGORY_MAP = {
    "Sub Compacto": "Sub Compacto",
    "Compacto": "Compacto",
    "Médio": "Médio",
    "Grande": "Grande",
    "Extra Grande": "Extra Grande",
    "Utilitário Esportivo Compacto": "Utilitário Esportivo Compacto",
    "Utilitário Esportivo Compacto 4x4": "Utilitário Esportivo Compacto",
    "Utilitário Esportivo Grande": "Utilitário Esportivo Grande",
    "Utilitário Esportivo Grande 4x4": "Utilitário Esportivo Grande",
    "Fora de Estrada Grande": "Fora de Estrada Grande",
    "Esportivo": "Esportivo",
    "Comercial": "Comercial",
    "Picape": "Picape",
    "Minivan": "Minivan",
}


def parse_numeric(val) -> float:
    """Converte strings brasileiras (ex: '0,41', '1.200,5', '-') em float."""
    if pd.isna(val):
        return np.nan
    s = str(val).strip().replace("\\", "").replace("-", "")
    if not s:
        return np.nan
    # Remove pontos de milhar e substitui vírgula decimal
    s = s.replace(".", "").replace(",", ".")
    try:
        return float(s)
    except (ValueError, TypeError):
        return np.nan


def clean_text_field(val: str, default: str = "") -> str:
    """Remove caracteres residuais de formatação e espaços extras."""
    if pd.isna(val):
        return default
    s = re.sub(r"\s+", " ", str(val)).strip()
    if s in ["-", "--", "\\", "\\\\"]:
        return default
    return s


def standardize_dataset(input_csv: Path, output_csv: Path) -> pd.DataFrame:
    """Executa todas as transformações e padronizações dos dados brutos."""
    if not input_csv.exists():
        logger.error(f"Arquivo de entrada não encontrado: {input_csv}")
        logger.error("Execute primeiro a etapa 02: python scripts/02_extract_raw_tables.py")
        sys.exit(1)

    logger.info(f"Lendo dados brutos extraídos: {input_csv}")
    df_raw = pd.read_csv(input_csv)

    # 1. Filtra veículos exclusivamente 100% elétricos (BEV)
    valid_propulsions = ["100% Elétrico"]
    df = df_raw[df_raw["propulsao_tipo"].isin(valid_propulsions)].copy()
    logger.info(f"Veículos 100% elétricos filtrados: {len(df)} registros.")

    # 2. Padronização de Marcas
    df["marca"] = df["marca_raw"].apply(lambda m: BRAND_MAP.get(clean_text_field(m), clean_text_field(m).title()))

    # 3. Limpeza de Modelo e Versão
    df["modelo"] = df["modelo_raw"].apply(lambda m: clean_text_field(m))
    df["versao"] = df["versao_raw"].apply(lambda v: clean_text_field(v, default="Única"))

    # Remove linha corrompida por sobreposição do PDF (Kia e- e-JS4)
    df = df[df["modelo"] != "e-"].copy()

    # 4. Padronização de Categoria Inmetro
    df["categoria"] = df["categoria_raw"].apply(
        lambda c: CATEGORY_MAP.get(clean_text_field(c), clean_text_field(c).title())
    )

    # 5. Propulsão
    df["propulsao"] = df["propulsao_tipo"].str.strip()

    # 6. Motor e Câmbio
    df["motor"] = df["motor_raw"].apply(lambda m: clean_text_field(m, default="Elétrico"))
    cambio_mapping = {
        "A-1": "Automática (1 marcha)",
        "A": "Automática",
        "N.A.": "Direta / Elétrica",
        "CVT-7": "CVT (7 marchas simuladas)",
        "CVT": "CVT",
        "DCT-6": "Dupla Embreagem (6 marchas)",
        "DCT-7": "Dupla Embreagem (7 marchas)",
        "DCT-8": "Dupla Embreagem (8 marchas)",
    }
    df["cambio"] = df["cambio_raw"].apply(
        lambda c: cambio_mapping.get(clean_text_field(c), clean_text_field(c, default="Automática"))
    )

    # 7. Combustível
    combustivel_mapping = {
        "E": "Elétrico",
        "G": "Gasolina",
        "F": "Flex (Etanol/Gasolina)",
        "D": "Diesel",
    }
    df["combustivel"] = df["combustivel_raw"].apply(
        lambda cb: combustivel_mapping.get(clean_text_field(cb), clean_text_field(cb, default="Elétrico"))
    )

    # 8. Conversão de Métricas Numéricas
    df["autonomia_inmetro_km"] = df["autonomia_km_raw"].apply(parse_numeric)
    df["consumo_energetico_mj_km"] = df["consumo_mj_km_raw"].apply(parse_numeric)
    df["km_l_equivalente_cidade"] = df["km_l_cidade_raw"].apply(parse_numeric)
    df["km_l_equivalente_estrada"] = df["km_l_estrada_raw"].apply(parse_numeric)
    df["emissao_co2_g_km"] = df["emissao_co2_raw"].apply(parse_numeric)

    # Para 100% Elétrico, emissão de CO2 fóssil pelo escapamento é estritamente 0.0
    df.loc[df["propulsao"] == "100% Elétrico", "emissao_co2_g_km"] = 0.0

    # Imputa consumo se faltante por média do mesmo modelo
    df["consumo_energetico_mj_km"] = df.groupby(["marca", "modelo"])["consumo_energetico_mj_km"].transform(
        lambda x: x.fillna(x.mean())
    )

    # 9. Classificações e Selos
    df["classificacao_categoria"] = df["classificacao_categoria_raw"].apply(
        lambda c: clean_text_field(c, default="-").upper()
    )
    df["classificacao_geral"] = df["classificacao_geral_raw"].apply(
        lambda c: clean_text_field(c, default="-").upper()
    )
    df["selo_conpet"] = df["selo_conpet_raw"].apply(
        lambda s: "Sim" if "sim" in str(s).lower() else "Não"
    )

    # 10. Conforto & Direção
    df["ar_condicionado"] = df["ar_condicionado_raw"].apply(
        lambda a: "Sim" if str(a).strip().upper() == "S" else "Não"
    )
    direcao_map = {
        "E": "Elétrica",
        "H": "Hidráulica",
        "EH": "Eletro-hidráulica",
        "M": "Mecânica",
    }
    df["direcao"] = df["direcao_raw"].apply(
        lambda d: direcao_map.get(str(d).strip().upper(), "Elétrica")
    )

    # 11. Seleção e ordenação de colunas finais
    final_cols = [
        "marca",
        "modelo",
        "versao",
        "categoria",
        "propulsao",
        "combustivel",
        "motor",
        "cambio",
        "autonomia_inmetro_km",
        "consumo_energetico_mj_km",
        "km_l_equivalente_cidade",
        "km_l_equivalente_estrada",
        "emissao_co2_g_km",
        "classificacao_categoria",
        "classificacao_geral",
        "selo_conpet",
        "ar_condicionado",
        "direcao",
    ]

    df_final = df[final_cols].drop_duplicates().sort_values(by=["marca", "modelo", "versao"]).reset_index(drop=True)

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    df_final.to_csv(output_csv, index=False)
    logger.info(f"Dataset oficial final salvo com sucesso em: {output_csv}")
    logger.info(f"Total de modelos únicos padronizados: {len(df_final)}")

    # Log de resumo analítico
    logger.info("--- Resumo Analítico por Propulsão ---")
    for prop, count in df_final["propulsao"].value_counts().items():
        logger.info(f"  - {prop}: {count} veículos")

    bev_df = df_final[df_final["propulsao"] == "100% Elétrico"]
    logger.info(
        f"Veículos 100% Elétricos: Autonomia média = {bev_df['autonomia_inmetro_km'].mean():.1f} km "
        f"(Min: {bev_df['autonomia_inmetro_km'].min():.0f} km, Max: {bev_df['autonomia_inmetro_km'].max():.0f} km)"
    )
    logger.info(
        f"Consumo Energético médio (BEVs): {bev_df['consumo_energetico_mj_km'].mean():.2f} MJ/km "
        f"(Melhor: {bev_df['consumo_energetico_mj_km'].min():.2f} MJ/km)"
    )

    return df_final


def main():
    parser = argparse.ArgumentParser(description="Padroniza e exporta dados oficiais do Inmetro PBEV.")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/interim/pbev_bruto_extraido.csv"),
        help="Caminho do CSV intermediário extraído.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/carros_eletricos_brasil.csv"),
        help="Caminho do CSV final processado.",
    )
    args = parser.parse_args()

    standardize_dataset(args.input, args.output)


if __name__ == "__main__":
    main()
