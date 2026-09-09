"""Módulo de configurações gerais e estilização da interface."""

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

# Paleta padronizada por categorias oficiais do Inmetro (PBEV)
CATEGORY_COLOR_MAP = {
    "Sub Compacto": "#636EFA",
    "Compacto": "#EF553B",
    "Médio": "#00CC96",
    "Grande": "#AB63FA",
    "Extra Grande": "#FFA15A",
    "Utilitário Esportivo Compacto": "#19D3F3",
    "Utilitário Esportivo Grande": "#FF6692",
    "Fora de Estrada Grande": "#B6E880",
    "Esportivo": "#FF97FF",
    "Comercial": "#FECB52",
    "Picape": "#8c564b",
    "Minivan": "#17becf",
}

# Paleta padronizada por tipo de propulsão
PROPULSION_COLOR_MAP = {
    "100% Elétrico": "#00CC96",
    "Híbrido Plug-in": "#636EFA",
    "Híbrido": "#FFA15A",
}


def setup_page_and_styles():
    """Configura metadados da página, layout e estilos CSS customizados."""
    st.set_page_config(
        page_title="Carros 100% Elétricos no Brasil (Inmetro)",
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
