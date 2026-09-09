# Contexto Geral do Projeto — Carros Elétricos Dashboard

Este documento fornece o contexto geral, decisões arquiteturais, padrões de código e diretrizes de desenvolvimento para agentes de IA e desenvolvedores que venham a manter ou evoluir este repositório.

---

## 1. Visão Geral do Projeto

O **Carros Elétricos no Brasil** é um painel analítico interativo voltado para visualização, comparação e análise técnica e mercadológica de veículos **100% elétricos (BEV)**, **híbridos plug-in (PHEV)** e **híbridos convencionais (HEV)** homologados e comercializados no Brasil, com base estrita no **Programa Brasileiro de Etiquetagem Veicular (PBEV / Inmetro)**.

### Objetivos Principais:
- Proporcionar uma visão clara e comparativa da eficiência energética ($MJ/km$), autonomia elétrica oficial homologada pelo Inmetro ($km$) e rendimento equivalente ($km/l$).
- Permitir filtros rápidos por montadora, categoria oficial do Inmetro, piso de autonomia e propulsão (permitindo isolar 100% elétricos ou híbridos).
- Manter uma esteira de dados 100% automatizada e auditável para atualização a partir do PDF oficial do Inmetro, sem dados fictícios ou referências estáticas manuais.
- Servir como base modular, extensível e pronta para produção no Streamlit Community Cloud.

---

## 2. Stack Tecnológica

- **Linguagem:** Python 3.12 (compatível com 3.11+).
- **Framework Web/Dashboard:** Streamlit (>= 1.40.0).
- **Manipulação de Dados:** Pandas (>= 2.2.0).
- **Visualização Analítica:** Plotly Express & Plotly Graph Objects (>= 5.24.0).
- **Processamento de PDFs e Tabelas:** `pdfplumber` (>= 0.11.0).
- **Requisições HTTP & Download:** `requests` (>= 2.31.0).
- **Gerenciador de Dependências:** `uv` (padrão recomendado) e `pip` (com suporte retrocompatível).

---

## 3. Arquitetura do Repositório

O projeto segue uma arquitetura modularizada em camadas para manter responsabilidades isoladas e permitir fácil escalabilidade:

```
carros-eletricos-dashboard/
├── .gitignore                     # Arquivos ignorados pelo Git (.venv, data/raw, data/interim)
├── .python-version                # Versão padrão do Python (3.12)
├── pyproject.toml                 # Metadados do projeto e dependências (uv/pip)
├── requirements.txt               # Dependências pinadas para instalação via pip
├── README.md                      # Apresentação do projeto e instruções de execução
├── Agents.md                      # Este guia de contexto para agentes de IA
├── CHANGELOG.md                   # Registro de versões seguindo Keep a Changelog e SemVer
├── app.py                         # Orquestrador base e ponto de entrada da aplicação
│
├── src/                           # Código-fonte modular da aplicação
│   ├── __init__.py
│   ├── config.py                  # Configurações de página, tema, CSS, cores e localização Plotly
│   ├── data.py                    # Carga de dados em cache (@st.cache_data) e filtros
│   │
│   └── components/                # Componentes isolados da interface
│       ├── __init__.py
│       ├── sidebar.py             # Barra lateral com controles de propulsão e filtros Inmetro (top 5 inicial)
│       ├── kpis.py                # Cartões de métricas principais (KPIs) com question tags
│       ├── charts.py              # Gráficos analíticos Plotly (Autonomia, Eficiência, Selo CONPET, PBE)
│       ├── table.py               # Tabela exploratória detalhada e exportação CSV
│       └── footer.py              # Rodapé institucional da aplicação com fonte Inmetro
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
    ├── development_guide.md       # Guia passo a passo de desenvolvimento local
    └── data_update_guide.md       # Guia operacional detalhado do pipeline PBEV Inmetro
```

---

## 4. Diretrizes e Convenções Estritas

Ao alterar ou adicionar código, qualquer agente de IA **DEVE** seguir rigorosamente estas convenções:

### 4.1. Zero Emojis (Material Symbols)
- **NUNCA utilize emojis tradicionais** (`🚗`, `⚡`, `📊`, `⚠️`, etc.) no código, na interface ou na documentação.
- Utilize estritamente os **Google Material Symbols** suportados nativamente pelo Streamlit:
  - Exemplo: `:material/electric_car:`, `:material/tune:`, `:material/bar_chart:`, `:material/eco:`, `:material/warning:`, `:material/download:`.

### 4.2. Localização e Padrão Brasileiro (pt-BR)
- **Números e Decimais:** Formatação com vírgula como separador decimal e ponto como separador de milhar.
- **Separadores no Plotly:** Todos os gráficos devem utilizar `separators=",."` no layout.
- **Dicionário de Tradução:** O `PLOTLY_CONFIG_PT_BR` (definido em `src/config.py`) deve ser repassado ao `config` de qualquer chamada `st.plotly_chart(fig, config=PLOTLY_CONFIG_PT_BR)`.

### 4.3. Coerência de Cores por Categoria Oficial e Propulsão
- Utilize sempre o dicionário `CATEGORY_COLOR_MAP` para categorias normatizadas pelo Inmetro (`Sub Compacto`, `Compacto`, `Médio`, `Grande`, `Extra Grande`, `Utilitário Esportivo Compacto`, `Utilitário Esportivo Grande`, `Fora de Estrada Grande`, `Esportivo`, `Comercial`, `Picape`).
- Utilize o dicionário `PROPULSION_COLOR_MAP` para gráficos segmentados por propulsão (`100% Elétrico`, `Híbrido Plug-in`, `Híbrido`).

### 4.4. Acessibilidade e Ajuda Contextual (*Question Tags*)
- Todo cartão de KPI (`st.metric`) e título de seção/gráfico deve possuir o parâmetro `help="..."` com explicações técnicas e contextuais para facilitar a experiência do usuário.

### 4.5. Orquestrador Enxuto (`app.py`)
- O arquivo `app.py` deve permanecer com responsabilidade exclusiva de orquestração (inicialização de estilos, leitura de filtros e chamada de renderizadores), mantendo-se conciso (~50 a 65 linhas).
- Qualquer nova lógica de negócio, processamento ou novo componente visual deve ser adicionado em um módulo dedicado dentro de `src/` ou `src/components/`.

### 4.6. Integridade dos Dados de Origem
- Não utilizar referências estáticas locais codificadas no script (hardcoded) para dados veiculares. Toda e qualquer informação deve ser extraída e gerada dinamicamente pelo pipeline a partir da tabela oficial do Inmetro.

---

## 5. Como Executar e Testar

```bash
# Execução da aplicação Streamlit:
uv run streamlit run app.py

# Execução do pipeline de dados (ETL):
uv run python scripts/run_pipeline.py
```
