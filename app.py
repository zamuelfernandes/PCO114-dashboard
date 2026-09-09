"""
Dashboard de Carros Elétricos no Brasil
Ponto de entrada principal da aplicação Streamlit.
"""

import streamlit as st

from src.config import DATA_FILE, setup_page_and_styles
from src.data import filter_data, load_data
from src.components.sidebar import render_sidebar
from src.components.kpis import render_kpis
from src.components.charts import render_charts
from src.components.table import render_table
from src.components.footer import render_footer


def main():
    # Inicializa configurações da página e estilos visuais
    setup_page_and_styles()

    # Carregamento dos dados
    df_raw = load_data(DATA_FILE)

    # Filtros interativos na barra lateral
    filters = render_sidebar(df_raw)
    df_filtrado = filter_data(df_raw, filters)

    # Cabeçalho Principal
    st.title(":material/electric_car: Carros Elétricos no Brasil")
    st.markdown(
        "Painel exploratório de modelos 100% elétricos (BEV) comercializados no mercado brasileiro. "
        "Use os filtros na barra lateral para segmentar por marca, preço e autonomia oficial do Inmetro."
    )

    # Validação de dados filtrados
    if df_filtrado.empty:
        st.warning(
            "Nenhum veículo encontrado com os filtros selecionados. Ajuste os filtros na barra lateral.",
            icon=":material/warning:",
        )
        st.stop()

    # Seção de Métricas (KPIs)
    render_kpis(df_filtrado)
    st.markdown("---")

    # Abas de Análise e Dados
    tab_graficos, tab_tabela = st.tabs([
        ":material/bar_chart: Gráficos & Comparações",
        ":material/table_chart: Tabela Detalhada",
    ])

    with tab_graficos:
        render_charts(df_filtrado)

    with tab_tabela:
        render_table(df_filtrado)

    # Rodapé institucional
    render_footer()


if __name__ == "__main__":
    main()
