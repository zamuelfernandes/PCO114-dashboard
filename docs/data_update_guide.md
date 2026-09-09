# Guia Operacional: Atualização da Base de Dados (PBEV / Inmetro)

Este documento descreve o procedimento operacional padrão (SOP) para atualizar, extrair, padronizar e publicar novos dados de veículos eletrificados no dashboard **Carros Elétricos e Híbridos no Brasil**.

---

## 1. Arquitetura da Esteira de Dados (Pipeline ETL)

A esteira de dados é 100% automatizada, auditável e modular, dividida em três estágios sequenciais:

```
                  [gov.br/inmetro - Tabela PBEV PDF]
                                  │
                                  ▼
               ┌─────────────────────────────────────┐
               │     01_download_inmetro.py          │
               │  Download oficial automatizado      │
               └─────────────────────────────────────┘
                                  │
                                  ▼
                    [data/raw/tabela_pbev_inmetro.pdf]
                                  │
                                  ▼
               ┌─────────────────────────────────────┐
               │    02_extract_raw_tables.py         │
               │  Extração tabular de todas páginas  │
               └─────────────────────────────────────┘
                                  │
                                  ▼
               [data/interim/pbev_bruto_extraido.csv]
                                  │
                                  ▼
               ┌─────────────────────────────────────┐
               │  03_process_and_standardize.py      │
               │  Filtro de eletrificados e limpeza  │
               └─────────────────────────────────────┘
                                  │
                                  ▼
               [data/carros_eletricos_brasil.csv]
                                  │
                                  ▼
                     [Streamlit Dashboard / Cloud]
```

---

## 2. Como Executar a Atualização

### Opção 1: Execução Completa Automatizada (Recomendado)

O script `run_pipeline.py` orquestra automaticamente as três etapas com cronometragem e registro estruturado de logs:

```bash
uv run python scripts/run_pipeline.py
```

### Opção 2: Pular o Download (Reprocessamento Rápido)

Se o PDF oficial já estiver baixado em `data/raw/tabela_pbev_inmetro.pdf`, você pode pular a etapa de rede e reprocessar as extrações em menos de 15 segundos:

```bash
uv run python scripts/run_pipeline.py --skip-download
```

### Opção 3: Executar Estágios Individuais Isoladamente

Você pode acionar qualquer uma das etapas de forma independente:

```bash
# Executa apenas o download:
uv run python scripts/run_pipeline.py --only download

# Executa apenas a extração do PDF para CSV intermediário:
uv run python scripts/run_pipeline.py --only extract

# Executa apenas a padronização e geração do CSV final:
uv run python scripts/run_pipeline.py --only process
```

---

## 3. Detalhamento dos Estágios

### Estágio 01: Download Automatizado (`scripts/01_download_inmetro.py`)
- Conecta diretamente aos servidores oficiais do governo federal (`https://www.gov.br/inmetro/...`).
- Utiliza headers HTTP padrão de navegador para garantir estabilidade e evitar bloqueios.
- Salva o arquivo binário em `data/raw/tabela_pbev_inmetro.pdf`.
- Valida o tamanho do arquivo baixado (> 1 MB) antes de prosseguir.

### Estágio 02: Extração Tabular Bruta (`scripts/02_extract_raw_tables.py`)
- Inspeciona todas as 9 páginas do documento PDF oficial utilizando `pdfplumber`.
- Trata células compostas com quebras de linha (`\n`), desmembrando até 3 versões empilhadas por linha física na tabela.
- Captura métricas de consumo urbano e rodoviário tanto para o modo elétrico quanto para combustão/híbrido.
- Gera o arquivo intermediário `data/interim/pbev_bruto_extraido.csv` com mais de 390 registros brutos.

### Estágio 03: Processamento e Padronização (`scripts/03_process_and_standardize.py`)
- Filtra estritamente veículos com propulsão eletrificada:
  - `100% Elétrico` (BEV)
  - `Híbrido Plug-in` (PHEV)
  - `Híbrido` (HEV convencional)
- Normaliza nomes de montadoras (ex: `BYD`, `Audi`, `BMW`, `Volvo`, `GWM`, `Porsche`, `Mercedes-Benz`, etc.).
- Mapeia as categorias para a nomenclatura oficial do Inmetro (`Sub Compacto`, `Compacto`, `Médio`, `Grande`, `Extra Grande`, `Utilitário Esportivo Compacto`, `Utilitário Esportivo Grande`, `Fora de Estrada Grande`, `Esportivo`, `Comercial`, `Picape`).
- Converte strings numéricas brasileiras para floats utilizáveis em cálculos analíticos.
- Garante emissão de $CO_2$ igual a $0.0\text{ g/km}$ para todos os modelos 100% elétricos a bateria.
- Salva o dataset final pronto para uso em `data/carros_eletricos_brasil.csv`.

---

## 4. Validação e Controle de Qualidade (QA)

Após rodar o pipeline, verifique o resumo analítico exibido no terminal:

```
[INFO] Dataset oficial final salvo com sucesso em: data/carros_eletricos_brasil.csv
[INFO] Total de modelos únicos padronizados: 384
[INFO] --- Resumo Analítico por Propulsão ---
[INFO]   - 100% Elétrico: 172 veículos
[INFO]   - Híbrido Plug-in: 108 veículos
[INFO]   - Híbrido: 104 veículos
[INFO] Veículos 100% Elétricos: Autonomia média = 341.3 km (Min: 156 km, Max: 570 km)
[INFO] Consumo Energético médio (BEVs): 0.62 MJ/km (Melhor: 0.39 MJ/km)
```

Para inspecionar a base de dados no Streamlit:
```bash
uv run streamlit run app.py
```
