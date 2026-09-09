# Guia de Desenvolvimento Local

Este guia orienta qualquer desenvolvedor ou colaborador da equipe a configurar o ambiente e executar o projeto **Carros Elétricos no Brasil** localmente.

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
# Cria o ambiente virtual (.venv) usando Python 3.12 ou a versão disponível
uv venv

# Instala as dependências a partir do requirements.txt
uv pip install -r requirements.txt
```

> **Dica**: Se preferir utilizar o `pyproject.toml`, você também pode rodar `uv sync`.

#### 3. Executar o Streamlit com o `uv`

```bash
uv run streamlit run app.py
```

O dashboard abrirá automaticamente no seu navegador no endereço: `http://localhost:8501`.

> **Dica**: Para confirmar qual Python o `uv` está usando, execute:
> ```bash
> uv run which python
> ```
> O retorno apontará diretamente para o caminho `.venv/bin/python`.

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

#### 3. Atualizar o pip e instalar as dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Executar a aplicação Streamlit

```bash
streamlit run app.py
```

---

## Estrutura de Arquivos

```
carros-eletricos-dashboard/
├── .gitignore                     # Arquivos e pastas ignorados pelo Git
├── .python-version                # Versão recomendada (Python 3.12)
├── pyproject.toml                 # Configuração padrão do projeto para uv/pip
├── requirements.txt               # Dependências pinadas para fácil instalação via pip
├── README.md                      # Visão geral do repositório
├── app.py                         # Executor base / ponto de entrada da aplicação
│
├── src/                           # Código-fonte modular da aplicação
│   ├── config.py                  # Configurações gerais, caminhos e estilos CSS
│   ├── data.py                    # Carregamento em cache e filtragem de dados
│   └── components/                # Componentes visuais isolados
│       ├── sidebar.py             # Filtros interativos na barra lateral
│       ├── kpis.py                # Cartões de métricas principais
│       ├── charts.py              # Gráficos analíticos Plotly (dispersão, barras, boxplot)
│       ├── table.py               # Tabela exploratória e exportação CSV
│       └── footer.py              # Rodapé institucional
│
├── data/
│   └── carros_eletricos_brasil.csv # Base de dados de veículos elétricos
└── docs/
    └── development_guide.md       # Este guia
```

---

## Como Atualizar ou Adicionar Dados

A base de dados é mantida no arquivo CSV:
`data/carros_eletricos_brasil.csv`

Ao adicionar novos veículos, certifique-se de seguir o padrão das colunas:

| Coluna | Tipo | Exemplo | Descrição |
|---|---|---|---|
| `marca` | Texto | `BYD` | Nome da fabricante |
| `modelo` | Texto | `Dolphin` | Nome comercial do modelo |
| `versao` | Texto | `GS 180 EV` | Versão do acabamento |
| `ano_modelo` | Inteiro | `2024` | Ano/Modelo |
| `categoria` | Texto | `Hatchback` | Carroceria (Hatchback, SUV, Sedan, Subcompacto) |
| `preco_estimado_brl` | Float | `149800.00` | Preço de tabela aproximado em Reais (R$) |
| `autonomia_inmetro_km` | Inteiro | `291` | Autonomia oficial aferida pelo Inmetro (PBEV) |
| `capacidade_bateria_kwh` | Float | `44.9` | Capacidade útil/nominal da bateria em kWh |
| `potencia_cv` | Inteiro | `95` | Potência máxima do motor em cv |
| `tempo_recarga_rapida_min`| Inteiro | `30` | Tempo estimado de carga rápida (20% a 80%) |
| `tipo_conector` | Texto | `CCS2` | Padrão do conector de recarga (ex: CCS2, CHAdeMO) |
| `tracao` | Texto | `Dianteira` | Tipo de tração (Dianteira, Traseira, Integral) |

Como a função `load_data()` no `app.py` utiliza `@st.cache_data`, após alterar o CSV basta salvar o arquivo e recarregar a página no navegador (pressionar `R` ou clicar em "Rerun").

---

## Dicas de Desenvolvimento com Streamlit

- **Hot Reload (Atualização Automática):** O Streamlit detecta alterações no `app.py` automaticamente. Você pode marcar a opção "Always rerun" no canto superior direito do navegador.
- **Porta personalizada:** Se a porta padrão `8501` estiver ocupada, use:
  ```bash
  streamlit run app.py --server.port 8502
  ```
- **Modo sem telemetria:** Para desativar mensagens de estatísticas na inicialização:
  ```bash
  streamlit run app.py --browser.gatherUsageStats false
  ```
