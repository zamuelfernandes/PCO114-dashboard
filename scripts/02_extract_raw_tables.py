"""
Etapa 02: Extração tabular do PDF oficial do Inmetro PBEV.
Lê data/raw/tabela_pbev_inmetro.pdf, desmembra células empilhadas e gera data/interim/pbev_bruto_extraido.csv.
"""

import argparse
import logging
from pathlib import Path
import sys
import time

import pandas as pd
import pdfplumber

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("02_extract")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_PDF = PROJECT_ROOT / "data" / "raw" / "tabela_pbev_inmetro.pdf"
INTERIM_DIR = PROJECT_ROOT / "data" / "interim"
DEFAULT_OUTPUT_CSV = INTERIM_DIR / "pbev_bruto_extraido.csv"


def clean_cell_str(val) -> str:
    """Higieniza quebras de linha e espaços excedentes em células de texto."""
    if not val:
        return ""
    return " ".join(str(val).strip().split())


def classify_propulsion_rough(text: str) -> str:
    """Classifica se a linha é eletrificada (Elétrico, Híbrido Plug-in ou Híbrido)."""
    t = text.lower()
    if "plug" in t:
        return "Híbrido Plug-in"
    elif "elétr" in t or "bev" in t:
        return "100% Elétrico"
    elif "híbr" in t or "hibr" in t or "hev" in t:
        return "Híbrido"
    elif "combust" in t:
        return "Combustão"
    return "Desconhecido"


def extract_tables(pdf_path: Path, output_csv: Path) -> Path:
    """Extrai todas as linhas de veículos eletrificados do PDF oficial."""
    if not pdf_path.exists():
        logger.error(f"Arquivo PDF não encontrado: {pdf_path}")
        logger.error("Execute primeiro a etapa 01: python scripts/01_download_inmetro.py")
        sys.exit(1)

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    logger.info(f"Iniciando extração tabular do PDF oficial: {pdf_path.name}")
    start_time = time.time()

    records = []
    total_tabelas = 0

    with pdfplumber.open(pdf_path) as pdf:
        total_paginas = len(pdf.pages)
        logger.info(f"O documento contém {total_paginas} páginas para análise.")

        for num_pag, pagina in enumerate(pdf.pages, 1):
            tabelas = pagina.extract_tables()
            for tabela in tabelas:
                total_tabelas += 1
                # Ignora cabeçalhos principais (linhas 0 e 1)
                for row in tabela[2:]:
                    if len(row) < 30:
                        continue

                    # Identifica se a linha possui motorização ou propulsão eletrificada
                    prop_cell = row[5] or ""
                    mot_cell = row[4] or ""
                    row_check = (prop_cell + " " + mot_cell).lower()

                    if not any(k in row_check for k in ["elétr", "híbr", "hibr", "plug", "bev"]):
                        continue

                    # Desmembra células que contêm múltiplos veículos empilhados via quebra de linha
                    props = prop_cell.split("\n")
                    marcas = (row[1] or "").split("\n")
                    modelos = (row[2] or "").split("\n")
                    versoes = (row[3] or "").split("\n")
                    motores = mot_cell.split("\n")
                    cambios = (row[6] or "").split("\n")
                    ar_conds = (row[7] or "").split("\n")
                    direcoes = (row[8] or "").split("\n")
                    combustiveis = (row[9] or "").split("\n")
                    emissao_co2 = (row[15] or "").split("\n")
                    km_l_gasolina_cidade = (row[21] or "").split("\n")
                    km_l_gasolina_estrada = (row[22] or "").split("\n")
                    km_l_cidade = (row[24] or "").split("\n")
                    km_l_estrada = (row[25] or "").split("\n")
                    consumos_mj = (row[28] or "").split("\n")
                    autonomias = (row[29] or "").split("\n")
                    class_cat = (row[30] or "").split("\n")
                    class_geral = (row[31] or "").split("\n")
                    selos_conpet = (row[32] or "").split("\n")
                    categorias = (row[0] or "").split("\n")

                    n = max(len(props), len(marcas), len(modelos))
                    for i in range(n):
                        p_val = props[i] if i < len(props) else (props[-1] if props else "")
                        p_tipo = classify_propulsion_rough(p_val)
                        if p_tipo == "Combustão":
                            continue

                        m_val = clean_cell_str(marcas[i] if i < len(marcas) else marcas[-1])
                        mod_val = clean_cell_str(modelos[i] if i < len(modelos) else modelos[-1])
                        ver_val = clean_cell_str(versoes[i] if i < len(versoes) else "")
                        cat_val = clean_cell_str(categorias[i] if i < len(categorias) else (categorias[-1] if categorias else ""))

                        # Desconsidera cabeçalhos residuais
                        if not m_val or m_val.lower().startswith("marca") or not mod_val:
                            continue

                        # Se km/l eletrico for vazio/barra mas for híbrido, usa km/l gasolina
                        cidade_val = clean_cell_str(km_l_cidade[i] if i < len(km_l_cidade) else "")
                        estrada_val = clean_cell_str(km_l_estrada[i] if i < len(km_l_estrada) else "")
                        gas_cid_val = clean_cell_str(km_l_gasolina_cidade[i] if i < len(km_l_gasolina_cidade) else "")
                        gas_est_val = clean_cell_str(km_l_gasolina_estrada[i] if i < len(km_l_gasolina_estrada) else "")

                        if (not cidade_val or cidade_val in ["-", "\\"]) and gas_cid_val and gas_cid_val not in ["-", "\\"]:
                            cidade_val = gas_cid_val
                        if (not estrada_val or estrada_val in ["-", "\\"]) and gas_est_val and gas_est_val not in ["-", "\\"]:
                            estrada_val = gas_est_val

                        record = {
                            "pagina": num_pag,
                            "categoria_raw": cat_val,
                            "marca_raw": m_val,
                            "modelo_raw": mod_val,
                            "versao_raw": ver_val,
                            "motor_raw": clean_cell_str(motores[i] if i < len(motores) else ""),
                            "propulsao_raw": p_val.strip(),
                            "propulsao_tipo": p_tipo,
                            "cambio_raw": clean_cell_str(cambios[i] if i < len(cambios) else ""),
                            "ar_condicionado_raw": clean_cell_str(ar_conds[i] if i < len(ar_conds) else ""),
                            "direcao_raw": clean_cell_str(direcoes[i] if i < len(direcoes) else ""),
                            "combustivel_raw": clean_cell_str(combustiveis[i] if i < len(combustiveis) else ""),
                            "emissao_co2_raw": clean_cell_str(emissao_co2[i] if i < len(emissao_co2) else ""),
                            "km_l_cidade_raw": cidade_val,
                            "km_l_estrada_raw": estrada_val,
                            "consumo_mj_km_raw": clean_cell_str(consumos_mj[i] if i < len(consumos_mj) else ""),
                            "autonomia_km_raw": clean_cell_str(autonomias[i] if i < len(autonomias) else ""),
                            "classificacao_categoria_raw": clean_cell_str(class_cat[i] if i < len(class_cat) else ""),
                            "classificacao_geral_raw": clean_cell_str(class_geral[i] if i < len(class_geral) else ""),
                            "selo_conpet_raw": clean_cell_str(selos_conpet[i] if i < len(selos_conpet) else ""),
                        }
                        records.append(record)

    df_raw = pd.DataFrame(records)
    df_raw.to_csv(output_csv, index=False)
    elapsed = time.time() - start_time
    logger.info(f"Extração concluída em {elapsed:.1f}s!")
    logger.info(f"Total de registros brutos extraídos: {len(df_raw)} salvos em: {output_csv}")
    return output_csv


def main():
    parser = argparse.ArgumentParser(description="Etapa 2: Extração tabular do PDF oficial do Inmetro.")
    parser.add_argument(
        "--input",
        "-i",
        type=Path,
        default=RAW_PDF,
        help=f"Caminho do PDF oficial (padrão: {RAW_PDF}).",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=DEFAULT_OUTPUT_CSV,
        help=f"Caminho de saída do CSV intermediário (padrão: {DEFAULT_OUTPUT_CSV}).",
    )
    args = parser.parse_args()

    extract_tables(args.input, args.output)


if __name__ == "__main__":
    main()
