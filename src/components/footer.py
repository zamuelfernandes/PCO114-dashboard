"""Componente de rodapé da aplicação."""

import streamlit as st


def render_footer():
    """Renderiza a linha divisória e o texto informativo do rodapé."""
    st.markdown("---")
    st.caption(
        ":material/verified: **Carros 100% Elétricos no Brasil** • "
        "Dados oficiais extraídos diretamente do Programa Brasileiro de Etiquetagem Veicular (PBEV / Inmetro) • "
        "Pipeline de dados automatizado com download, extração tabular e padronização contínua."
    )
