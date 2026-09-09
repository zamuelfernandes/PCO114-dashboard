"""
Etapa 01: Download da tabela oficial do PBEV diretamente do portal do Inmetro.
Salva o arquivo PDF bruto em data/raw/tabela_pbev_inmetro.pdf.
"""

import argparse
import logging
from pathlib import Path
import sys
import time

import requests

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("01_download")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
DEFAULT_PDF_PATH = RAW_DIR / "tabela_pbev_inmetro.pdf"

# URLs oficiais do Inmetro (Tabela PBEV Veículos Leves)
URL_PBEV_2026 = (
    "https://www.gov.br/inmetro/pt-br/assuntos/regulamentacao/avaliacao-da-conformidade/"
    "programa-brasileiro-de-etiquetagem/tabelas-de-eficiencia-energetica/"
    "veiculos-automotivos-pbe-veicular/mascara-pbev-2026_19_jan-rev01.pdf/@@download/file"
)
URL_PBEV_2025 = (
    "https://www.gov.br/inmetro/pt-br/assuntos/regulamentacao/avaliacao-da-conformidade/"
    "programa-brasileiro-de-etiquetagem/tabelas-de-eficiencia-energetica/"
    "veiculos-automotivos-pbe-veicular/mascara-pbev-2025-mar-11.pdf/@@download/file"
)


def download_pbev(dest_path: Path = DEFAULT_PDF_PATH, force: bool = False) -> Path:
    """Executa o download do arquivo PDF oficial do Inmetro."""
    if dest_path.exists() and not force and dest_path.stat().st_size > 500000:
        tamanho_mb = dest_path.stat().st_size / (1024 * 1024)
        logger.info(f"Arquivo oficial já existe localmente: {dest_path} ({tamanho_mb:.2f} MB)")
        logger.info("Use --force para forçar um novo download.")
        return dest_path

    dest_path.parent.mkdir(parents=True, exist_ok=True)
    logger.info("Iniciando download da tabela oficial do PBEV / Inmetro...")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    urls = [URL_PBEV_2026, URL_PBEV_2025]
    start_time = time.time()

    for url in urls:
        try:
            logger.info(f"Conectando ao portal do Inmetro: {url}")
            response = requests.get(url, headers=headers, stream=True, timeout=45)
            if response.status_code == 200 and "pdf" in response.headers.get("Content-Type", "").lower():
                total_bytes = 0
                with open(dest_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=65536):
                        if chunk:
                            f.write(chunk)
                            total_bytes += len(chunk)

                elapsed = time.time() - start_time
                tamanho_mb = total_bytes / (1024 * 1024)
                logger.info(f"Download concluído com sucesso em {elapsed:.1f}s!")
                logger.info(f"Arquivo salvo em: {dest_path} ({tamanho_mb:.2f} MB)")
                return dest_path
            else:
                logger.warning(
                    f"Servidor retornou status {response.status_code} para {url}. Tentando próxima URL..."
                )
        except Exception as e:
            logger.warning(f"Erro ao tentar baixar de {url}: {e}. Tentando alternativa...")

    logger.error("Falha ao baixar a tabela do Inmetro de todas as URLs oficiais.")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Etapa 1: Download da tabela oficial do Inmetro PBEV.")
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=DEFAULT_PDF_PATH,
        help=f"Caminho de destino do PDF (padrão: {DEFAULT_PDF_PATH}).",
    )
    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Força o download mesmo se o arquivo já existir localmente.",
    )
    args = parser.parse_args()

    download_pbev(args.output, force=args.force)


if __name__ == "__main__":
    main()
