# Carros Elétricos no Brasil — Dashboard Streamlit

Painel interativo e moderno desenvolvido com **Streamlit**, **Pandas** e **Plotly** para análise e exploração de dados sobre o mercado de veículos 100% elétricos (BEV) no Brasil.

Este repositório foi concebido como uma **versão base inicial (First Commit)** para que a equipe possa testar, expandir e implementar novas funcionalidades e visualizações com facilidade.

---

## Principais Recursos

- **Filtros Interativos na Barra Lateral:** Segmentação dinâmica por marca, categoria da carroceria (SUV, Hatchback, Sedan, Subcompacto), teto de preço e autonomia mínima.
- **KPIs Estratégicos:** Total de modelos no filtro, preço médio, autonomia média e veículo campeão de autonomia.
- **Gráficos Interativos (Plotly):**
  - Dispersão: Relação Preço vs. Autonomia com indicador de potência (cv) no tamanho da bolha.
  - Barras: Quantidade de modelos por montadora/marca.
  - Boxplot: Distribuição e dispersão de preços por categoria.
- **Tabela Exploratória & Exportação:** Visualização completa e botão para download dos dados filtrados em formato `.csv`.
- **Suporte Duplo de Ambientes:** Compatível com **`uv`** (alta velocidade) e com **`venv` + `pip`** clássico.

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

# 2. Executa a aplicação
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

## Documentação para a Equipe

Na pasta [`docs/`](docs/) você encontra guias detalhados preparados especialmente para os colaboradores:

| Documento | Conteúdo |
|---|---|
| [**Guia de Desenvolvimento Local**](docs/development_guide.md) | Passo a passo detalhado para Windows, Linux e Mac usando `uv` ou `pip`, dicionário de dados do CSV e dicas de desenvolvimento com Streamlit. |
| [**Guia de Deploy no Streamlit Cloud**](docs/deployment_guide.md) | Instruções completas para publicar o dashboard gratuitamente na plataforma oficial do Streamlit Community Cloud conectada ao GitHub. |

---

## Estrutura do Projeto

```
carros-eletricos-dashboard/
├── .gitignore                     # Arquivos ignorados pelo Git (.venv, caches, temporários)
├── .python-version                # Versão padrão do Python recomendada (3.12)
├── pyproject.toml                 # Configuração moderna de empacotamento para uv/pip
├── requirements.txt               # Lista de dependências para instalação rápida com pip
├── README.md                      # Apresentação e guia rápido do projeto
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
│   └── carros_eletricos_brasil.csv # Base de dados com modelos reais vendidos no Brasil
│
└── docs/
    ├── development_guide.md       # Guia para execução e desenvolvimento local
    └── deployment_guide.md        # Guia para deploy no Streamlit Community Cloud
```

---

## Base de Dados Inicial

Os dados estão localizados em `data/carros_eletricos_brasil.csv` e contemplam modelos populares e de destaque comercializados no Brasil (como BYD Dolphin, Dolphin Mini, Seal, GWM Ora 03, Volvo EX30, XC40, Renault Kwid E-Tech, Peugeot e-2008, BMW iX1, Porsche Taycan, etc.).

Principais colunas:
- `marca`: Fabricante do veículo (ex: BYD, GWM, Volvo, etc.)
- `modelo`: Nome do modelo
- `versao`: Versão do acabamento/motorização
- `ano_modelo`: Ano do modelo
- `categoria`: Tipo de carroceria (Hatchback, SUV, Sedan, Subcompacto)
- `preco_estimado_brl`: Preço aproximado de tabela em R$
- `autonomia_inmetro_km`: Autonomia oficial aferida pelo Programa Brasileiro de Etiquetagem Veicular (PBEV / Inmetro)
- `capacidade_bateria_kwh`: Capacidade da bateria (kWh)
- `potencia_cv`: Potência em cavalos-vapor (cv)
- `tempo_recarga_rapida_min`: Tempo médio para recarga de 20% a 80% em carregadores DC
- `tipo_conector`: Padrão do plugue de recarga rápida (ex: CCS2)
- `tracao`: Dianteira, Traseira ou Integral (AWD)

---

## Próximos Passos Sugeridos para a Equipe

1. Expandir a base de dados com novos lançamentos do mercado brasileiro.
2. Adicionar novas métricas (ex: custo por km rodado, tempo de 0 a 100 km/h).
3. Implementar comparador lado a lado entre dois modelos selecionados pelo usuário.
