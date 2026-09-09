#!/usr/bin/env python3
"""Orquestrador Geral do Pipeline de Dados PBEV / Inmetro.

Executa as três etapas sequenciais de forma modular e auditável:
1. 01_download_inmetro.py: Download do PDF oficial da tabela do Inmetro.
2. 02_extract_raw_tables.py: Extração tabular completa de todas as páginas.
3. 03_process_and_standardize.py: Padronização, limpeza e exportação final.

Exemplo de uso:
    uv run python scripts/run_pipeline.py
    uv run python scripts/run_pipeline.py --skip-download
    uv run python scripts/run_pipeline.py --only process
"""

import argparse
import logging
import subprocess
import sys
import time
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("pipeline")


def run_stage(script_name: str, args: list[str] | None = None) -> bool:
    """Executa um script de estágio filho repassando logs e capturando código de saída."""
    script_path = Path(__file__).parent / script_name
    if not script_path.exists():
        logger.error(f"Script de estágio não encontrado: {script_path}")
        return False

    cmd = [sys.executable, str(script_path)] + (args or [])
    stage_name = script_name.replace(".py", "")
    logger.info(f"===> [Início] Estágio: {stage_name}")
    start = time.time()

    res = subprocess.run(cmd)
    elapsed = time.time() - start

    if res.returncode != 0:
        logger.error(f"[Falha] Estágio {stage_name} encerrou com erro (código {res.returncode}).")
        return False

    logger.info(f"<=== [Concluído] Estágio: {stage_name} em {elapsed:.1f}s\n")
    return True


def main():
    parser = argparse.ArgumentParser(description="Pipeline completo de atualização de dados de carros elétricos (Inmetro PBEV).")
    parser.add_argument(
        "--skip-download",
        action="store_true",
        help="Ignora a etapa 01 de download caso o PDF já esteja presente em data/raw/.",
    )
    parser.add_argument(
        "--force-download",
        action="store_true",
        help="Força novo download do PDF mesmo se já existir.",
    )
    parser.add_argument(
        "--only",
        choices=["download", "extract", "process"],
        help="Executa isoladamente apenas uma das etapas do pipeline.",
    )
    args = parser.parse_args()

    total_start = time.time()
    logger.info("=================================================================")
    logger.info("  INICIANDO PIPELINE DE DADOS: PBE VEICULAR / INMETRO BRASIL     ")
    logger.info("=================================================================")

    # Execução isolada se solicitada
    if args.only:
        stage_map = {
            "download": "01_download_inmetro.py",
            "extract": "02_extract_raw_tables.py",
            "process": "03_process_and_standardize.py",
        }
        success = run_stage(stage_map[args.only])
        if not success:
            sys.exit(1)
        logger.info(f"Etapa '{args.only}' concluída com sucesso.")
        return

    # Etapa 1: Download
    pdf_path = Path("data/raw/tabela_pbev_inmetro.pdf")
    if args.skip_download and pdf_path.exists():
        logger.info("[Etapa 1/3] Ignorando download: PDF já existe em data/raw/tabela_pbev_inmetro.pdf")
    else:
        dl_args = ["--force"] if args.force_download else []
        if not run_stage("01_download_inmetro.py", dl_args):
            logger.error("Interrompendo pipeline devido a falha no download.")
            sys.exit(1)

    # Etapa 2: Extração
    if not run_stage("02_extract_raw_tables.py"):
        logger.error("Interrompendo pipeline devido a falha na extração tabular.")
        sys.exit(1)

    # Etapa 3: Processamento e Padronização
    if not run_stage("03_process_and_standardize.py"):
        logger.error("Interrompendo pipeline devido a falha na padronização dos dados.")
        sys.exit(1)

    total_elapsed = time.time() - total_start
    logger.info("=================================================================")
    logger.info(f"  PIPELINE EXECUTADO COM SUCESSO EM {total_elapsed:.1f}s! ")
    logger.info("  Arquivo final pronto: data/carros_eletricos_brasil.csv          ")
    logger.info("=================================================================")


if __name__ == "__main__":
    main()
