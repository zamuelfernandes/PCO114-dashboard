# Carros Elétricos e Híbridos no Brasil — Dashboard PBEV / Inmetro

Painel analítico interativo e moderno desenvolvido com **Streamlit**, **Pandas** e **Plotly** para exploração dos dados oficiais do **Programa Brasileiro de Etiquetagem Veicular (PBEV / Inmetro)** sobre veículos eletrificados no Brasil.

O repositório possui uma esteira completa e automatizada de dados (ETL) que extrai, padroniza e analisa mais de **380 versões** de veículos **100% elétricos (BEV)**, **híbridos plug-in (PHEV)** e **híbridos convencionais (HEV)** comercializados e homologados pelas montadoras no país.

---

## Principais Recursos

- **Filtro de Propulsão Multisseleção:** Permite isolar unicamente veículos 100% elétricos (BEV), híbridos plug-in (PHEV) ou híbridos convencionais (HEV).
- **Início Otimizado com Top 5:** O painel inicializa pré-selecionado com as 5 principais marcas e 5 categorias por volume, mantendo o carregamento ágil e a barra lateral compacta.
- **Categorias Oficiais do Inmetro:** Padronização rigorosa segundo as categorias normatizadas do PBEV (`Sub Compacto`, `Compacto`, `Médio`, `Grande`, `Extra Grande`, `Utilitário Esportivo Compacto`, `Utilitário Esportivo Grande`, `Fora de Estrada Grande`, `Esportivo`, `Comercial`, `Picape`).
- **Métricas Oficiais de Engenharia & Consumo:**
  - Consumo Energético oficial em Megajoules por quilômetro ($MJ/km$).
  - Autonomia elétrica homologada pelo Inmetro ($km$).
  - Rendimento equivalente cidade e estrada ($km/l$).
  - Emissões diretas de $CO_2$ fóssil no escapamento ($g/km$).
- **Abas Analíticas Dedicadas:**
  - **Autonomia & Eficiência:** Dispersão interativa (Autonomia vs. Consumo $MJ/km$), ranking de modelos por montadora e dispersão por categoria.
  - **Selo CONPET & Classificação PBE:** Proporção de veículos certificados com o Selo CONPET de alta eficiência, distribuição de notas A–E e emissões de $CO_2$.
  - **Tabela Oficial Homologada:** Planilha pesquisável completa com botão para download em CSV.
- **Pipeline de Dados Modular em 3 Estágios:** Download oficial online, extração tabular com `pdfplumber` e padronização com `run_pipeline.py`.
- **Zero Emojis:** Estilização visual exclusivamente com **Google Material Symbols** (`:material/icon_name:`).

---

## Início Rápido (Quickstart)

Entre na pasta do projeto:

```bash
cd carros-eletricos-dashboard
```

### Com `uv` (Recomendado):
```bash
# 1. Cria o ambiente virtual e instala dependências
uv venv
uv pip install -r requirements.txt

# 2. Executa a aplicação Streamlit
uv run streamlit run app.py
```

### Com `venv` + `pip` Tradicional:
```bash
# 1. Cria e ativa o ambiente virtual
python3 -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate

# 2. Instala as dependências e executa
pip install -r requirements.txt
streamlit run app.py
```

O dashboard estará disponível em: `http://localhost:8501`.

---

## Pipeline de Atualização de Dados (PBEV / Inmetro)

Para atualizar a base de dados a partir da tabela oficial publicada no portal do Inmetro:

```bash
# Executa o pipeline completo (Download -> Extração Tabular -> Padronização)
uv run python scripts/run_pipeline.py

# Se o PDF já foi baixado e deseja apenas reprocessar:
uv run python scripts/run_pipeline.py --skip-download
```

---

## Documentação para a Equipe

Na pasta [`docs/`](docs/) você encontra guias detalhados:

- [**Guia de Desenvolvimento Local**](docs/development_guide.md): Configuração de ambiente, arquitetura de pastas e dicas de desenvolvimento com Streamlit.
- [**Guia de Atualização da Base de Dados**](docs/data_update_guide.md): Detalhamento do pipeline modular (`01_download`, `02_extract`, `03_process` e `run_pipeline.py`).
- [**Diretrizes para Agentes de IA**](Agents.md): Padrões de código, convenção de zero emojis e decisões arquiteturais.

---

## Estrutura do Repositório

```
carros-eletricos-dashboard/
├── .gitignore                     # Arquivos ignorados pelo Git (.venv, caches, data/raw, data/interim)
├── .python-version                # Versão padrão do Python recomendada (3.12)
├── pyproject.toml                 # Configuração de empacotamento para uv/pip
├── requirements.txt               # Lista de dependências com versões pinadas
├── README.md                      # Apresentação e guia rápido do projeto
├── Agents.md                      # Contexto geral e diretrizes para agentes de IA
├── CHANGELOG.md                   # Histórico de versões e notas de lançamento
├── app.py                         # Ponto de entrada e orquestrador do Streamlit
│
├── src/                           # Código-fonte modular da aplicação
│   ├── config.py                  # Configurações de página, paletas de cores e estilos CSS
│   ├── data.py                    # Carga (@st.cache_data) e filtragem por propulsão/Inmetro
│   └── components/                # Componentes visuais isolados
│       ├── sidebar.py             # Filtros interativos (Propulsão, top 5 marcas/categorias, etc.)
│       ├── kpis.py                # Cartões de métricas (Modelos, Autonomia Média, Consumo MJ/km)
│       ├── charts.py              # Gráficos Plotly de eficiência, Selo CONPET e classificações PBE
│       ├── table.py               # Tabela oficial completa e botão de download CSV
│       └── footer.py              # Rodapé com atribuição ao PBEV / Inmetro
│
├── data/
│   └── carros_eletricos_brasil.csv # Base oficial padronizada (380+ veículos homologados)
│
├── scripts/                       # Pipeline ETL modular
│   ├── 01_download_inmetro.py     # Download automatizado do PDF oficial no gov.br/inmetro
│   ├── 02_extract_raw_tables.py   # Extração tabular com pdfplumber de todas as páginas
│   ├── 03_process_and_standardize.py # Limpeza, filtros de propulsão e padronização
│   └── run_pipeline.py            # Orquestrador geral da esteira de dados
│
└── docs/
    ├── development_guide.md       # Guia completo para desenvolvimento local
    └── data_update_guide.md       # Procedimento operacional detalhado da esteira ETL
```
