"""
Componente de rodapé da aplicação.
"""

import streamlit as st


def render_footer():
    """Renderiza a linha divisória e o texto informativo do rodapé."""
    st.markdown("---")
    st.caption(
        ":material/bolt: **Carros Elétricos no Brasil** • Versão de Base • "
        "Dados com valores estimados de tabela e autonomia homologada Inmetro (PBEV)."
    )
