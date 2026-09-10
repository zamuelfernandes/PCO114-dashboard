# Guia de Desenvolvimento Local

Este guia orienta qualquer desenvolvedor ou colaborador da equipe a configurar o ambiente e executar o projeto **Carros 100% Elétricos no Brasil** localmente.

---

## Pré-requisitos

- **Python 3.11** ou **Python 3.12** instalado na máquina.
- Git instalado (para versionamento).
- Gerenciador de pacotes: **uv** (altamente recomendado pela velocidade) ou o tradicional **pip**.

---

## Como Executar o Projeto

Entre na pasta do projeto no seu terminal:

```bash
cd carros-eletricos-dashboard
```

Escolha uma das duas opções abaixo para configurar seu ambiente:

---

### Opção 1: Usando `uv` (Recomendado)

O [uv](https://github.com/astral-sh/uv) é um gerenciador de pacotes e ambientes virtuais em Rust extremamente rápido.

#### 1. Instalar o `uv` (caso ainda não possua)

- **Linux / macOS:**
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- **Windows (PowerShell):**
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
- Ou via `pip`:
  ```bash
  pip install uv
  ```

#### 2. Criar o ambiente virtual e instalar dependências

```bash
# Cria o ambiente virtual (.venv) usando Python 3.12
uv venv

# Instala as dependências a partir do requirements.txt
uv pip install -r requirements.txt
```

#### 3. Executar o Streamlit com o `uv`

```bash
uv run streamlit run app.py
```

O dashboard abrirá automaticamente no seu navegador no endereço: `http://localhost:8501`.

---

### Opção 2: Usando `venv` e `pip` Tradicional

Caso prefira o fluxo clássico do Python sem instalar ferramentas adicionais:

#### 1. Criar o ambiente virtual

- **Linux / macOS:**
  ```bash
  python3 -m venv .venv
  ```
- **Windows:**
  ```powershell
  python -m venv .venv
  ```

#### 2. Ativar o ambiente virtual

- **Linux / macOS:**
  ```bash
  source .venv/bin/activate
  ```
- **Windows (PowerShell):**
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
- **Windows (Prompt de Comando - CMD):**
  ```cmd
  .venv\Scripts\activate.bat
  ```

#### 3. Instalar dependências e rodar

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## Estrutura do Projeto

```
carros-eletricos-dashboard/
├── app.py                         # Ponto de entrada e orquestrador principal do dashboard
├── src/
│   ├── config.py                  # Configurações de página, tema, cores e estilos CSS
│   ├── data.py                    # Carga (@st.cache_data) e filtros interativos
│   └── components/                # Componentes visuais modulares
│       ├── highlights.py          # Destaques do mercado (Rankings populares e treemap)
│       ├── charts.py              # Gráficos Plotly de autonomia e eficiência
│       ├── kpis.py                # Cartões de métricas e legenda global de categorias
│       ├── table.py               # Tabela oficial completa e botão de download CSV
│       ├── study_guide.py         # Guia explicativo com público, demanda e perguntas
│       ├── sidebar.py             # Filtros interativos na barra lateral
│       └── footer.py              # Rodapé com atribuição ao PBEV / Inmetro
├── data/
│   └── carros_eletricos_brasil.csv # Base oficial de dados padronizada (380+ veículos)
├── scripts/                       # Pipeline ETL modular
│   ├── 01_download_inmetro.py     # Download automatizado do PDF oficial no gov.br/inmetro
│   ├── 02_extract_raw_tables.py   # Extração tabular com pdfplumber de todas as páginas
│   ├── 03_process_and_standardize.py # Limpeza, filtros de propulsão e padronização
│   └── run_pipeline.py            # Orquestrador geral da esteira de dados
└── docs/
    ├── development_guide.md       # Este guia
    └── data_update_guide.md       # Procedimento operacional detalhado de atualização
```

---

## Como Atualizar a Base de Dados (Pipeline ETL)

O projeto possui uma esteira 100% automatizada e auditável para baixar a tabela oficial do Inmetro, extrair todas as páginas tabulares e padronizar o CSV final.

```bash
# Executa a esteira completa (Download -> Extração Tabular -> Padronização)
uv run python scripts/run_pipeline.py

# Se o PDF já foi baixado previamente:
uv run python scripts/run_pipeline.py --skip-download

# Executa apenas uma etapa específica:
uv run python scripts/run_pipeline.py --only process
```

Consulte o [**Guia de Atualização da Base de Dados**](data_update_guide.md) para detalhes operacionais e arquiteturais completos.

---

## Dicionário de Dados do CSV (`carros_eletricos_brasil.csv`)

O arquivo oficial final contém 18 colunas normatizadas:

| Coluna | Tipo | Exemplo | Descrição |
|---|---|---|---|
| `marca` | Texto | `BYD` | Fabricante / Montadora padronizada |
| `modelo` | Texto | `Dolphin Mini` | Nome comercial do modelo |
| `versao` | Texto | `GS 5 EV` | Versão de acabamento |
| `categoria` | Texto | `Sub Compacto` | Categoria oficial normatizada pelo Inmetro |
| `propulsao` | Texto | `100% Elétrico` | `100% Elétrico` |
| `combustivel` | Texto | `Elétrico` | Combustível utilizado (`Elétrico`, `Gasolina`, `Flex`) |
| `motor` | Texto | `Elétrico` | Especificação do motor |
| `cambio` | Texto | `Automática (1 marcha)` | Tipo de transmissão |
| `autonomia_inmetro_km` | Float | `280.0` | Autonomia elétrica oficial homologada (km) |
| `consumo_energetico_mj_km` | Float | `0.41` | Consumo energético em Megajoules por km ($MJ/km$) |
| `km_l_equivalente_cidade` | Float | `58.6` | Rendimento equivalente ou consumo urbano ($km/l$) |
| `km_l_equivalente_estrada` | Float | `41.9` | Rendimento equivalente ou consumo rodoviário ($km/l$) |
| `emissao_co2_g_km` | Float | `0.0` | Emissão fóssil direta de $CO_2$ no escapamento ($g/km$) |
| `classificacao_categoria` | Texto | `A` | Nota de eficiência na categoria (A a E) |
| `classificacao_geral` | Texto | `A` | Nota de eficiência na classificação geral (A a E) |
| `selo_conpet` | Texto | `Sim` | Premiação com o Selo CONPET de Alta Eficiência |
| `ar_condicionado` | Texto | `Sim` | Presença de ar-condicionado de série |
| `direcao` | Texto | `Elétrica` | Tipo de assistência de direção |

---

## Dicas de Desenvolvimento com Streamlit

- **Hot Reload (Atualização Automática):** O Streamlit detecta alterações nos scripts automaticamente. Você pode marcar a opção "Always rerun" no canto superior direito do navegador.
- **Porta personalizada:** Se a porta padrão `8501` estiver ocupada, use:
  ```bash
  streamlit run app.py --server.port 8502
  ```
- **Modo sem telemetria:** Para desativar mensagens de estatísticas na inicialização:
  ```bash
  streamlit run app.py --browser.gatherUsageStats false
  ```
