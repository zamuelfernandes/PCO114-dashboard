"""
Módulo de configurações gerais e estilização da interface.
"""

from pathlib import Path
import streamlit as st

# Caminho absoluto seguro para a base de dados
DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "carros_eletricos_brasil.csv"

# Configuração e dicionário de localização do Plotly em Português (pt-BR)
PLOTLY_CONFIG_PT_BR = {
    "locale": "pt-BR",
    "locales": {
        "pt-BR": {
            "dictionary": {
                "min:": "mínimo:",
                "max:": "máximo:",
                "median:": "mediana:",
                "q1:": "1º quartil (Q1):",
                "q3:": "3º quartil (Q3):",
                "lower fence:": "limite inferior:",
                "upper fence:": "limite superior:",
                "mean:": "média:",
                "min": "mínimo",
                "max": "máximo",
                "median": "mediana",
                "q1": "1º quartil (Q1)",
                "q3": "3º quartil (Q3)",
                "lower fence": "limite inferior",
                "upper fence": "limite superior",
                "mean": "média",
            }
        }
    },
    "displayModeBar": True,
    "displaylogo": False,
}

# Paleta padronizada por categoria para coerência visual entre todos os gráficos
CATEGORY_COLOR_MAP = {
    "Subcompacto": "#636EFA",
    "Hatchback": "#EF553B",
    "SUV": "#00CC96",
    "Sedan": "#AB63FA",
}


def setup_page_and_styles():
    """Configura metadados da página, layout e estilos CSS customizados."""
    st.set_page_config(
        page_title="Carros Elétricos no Brasil",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        """
        <style>
        /* Reduz o espaçamento excessivo no topo da página */
        .block-container,
        div[data-testid="stMainBlockContainer"],
        div[data-testid="stAppViewBlockContainer"] {
            padding-top: 1rem !important;
            padding-bottom: 2rem !important;
            max-width: 95% !important;
        }

        /* Reduz a altura do header padrão do Streamlit */
        header[data-testid="stHeader"],
        div[data-testid="stHeader"] {
            height: 2.2rem !important;
            background: transparent !important;
        }

        /* Remove margens extras do topo do título principal */
        h1:first-of-type {
            margin-top: 0rem !important;
            padding-top: 0rem !important;
        }

        /* Cards de métricas elegantes para tema claro */
        div[data-testid="stMetric"] {
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            padding: 0.9rem 1.2rem;
            border-radius: 0.75rem;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        }
        div[data-testid="stMetricLabel"] {
            color: #64748b;
            font-weight: 600;
            font-size: 0.9rem;
        }
        div[data-testid="stMetricValue"] {
            color: #0f172a;
            font-weight: 700;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
