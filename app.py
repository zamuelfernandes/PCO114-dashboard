"""Dashboard de Carros 100% Elétricos no Brasil.

Ponto de entrada principal da aplicação Streamlit baseado nos dados
oficiais de veículos elétricos a bateria (BEV) homologados pelo PBEV / Inmetro.
"""

import streamlit as st

from src.config import DATA_FILE, setup_page_and_styles
from src.data import filter_data, load_data
from src.components.sidebar import render_sidebar
from src.components.kpis import render_kpis
from src.components.charts import render_charts, render_conpet_and_pbe_tab
from src.components.table import render_table
from src.components.footer import render_footer


def main():
    # Inicializa configurações da página e estilos visuais
    setup_page_and_styles()

    # Cabeçalho Principal
    st.title(":material/electric_car: Carros 100% Elétricos no Brasil")
    st.markdown(
        "Painel analítico baseado no Programa Brasileiro de Etiquetagem Veicular (**PBEV / Inmetro**). "
        "Explore métricas oficiais de eficiência energética (MJ/km), autonomia homologada e rendimento equivalente de veículos "
        "**100% elétricos a bateria (BEV)** comercializados no Brasil."
    )

    # Carregamento seguro dos dados oficiais
    df_raw = load_data(DATA_FILE)

    # Tratamento quando a base está vazia, ausente ou ainda não foi gerada
    if df_raw is None or df_raw.empty:
        st.info(
            "**Base de dados oficial não encontrada ou vazia.**\n\n"
            "O arquivo com os dados homologados dos veículos elétricos ainda não foi gerado. "
            "Execute a esteira de dados no seu terminal para baixar e processar a tabela mais recente do Inmetro:",
            icon=":material/database:",
        )

        tab_uv, tab_pip = st.tabs([
            ":material/bolt: Com uv (Recomendado)",
            ":material/terminal: Com Python / pip Tradicional",
        ])

        with tab_uv:
            st.caption("Execução rápida com resolução automática do ambiente:")
            st.code("uv run python scripts/run_pipeline.py", language="bash")

        with tab_pip:
            st.caption("Execução clássica (certifique-se de estar com o ambiente virtual ativado):")
            st.code("python scripts/run_pipeline.py", language="bash")

        with st.container(border=True):
            st.markdown("##### :material/schema: O que a esteira realiza automaticamente:")
            st.markdown(
                """
                1. **Download Oficial:** Conecta diretamente ao portal do Inmetro (`gov.br/inmetro`) e baixa a tabela PDF oficial mais recente.
                2. **Extração Tabular:** Processa todas as 9 páginas com `pdfplumber` e desmembra os registros empilhados.
                3. **Padronização:** Filtra modelos 100% elétricos, normaliza categorias oficiais, limpa dados e salva em `data/carros_eletricos_brasil.csv`.
                """
            )

        col_btn, _ = st.columns([1, 3])
        with col_btn:
            if st.button(":material/refresh: Recarregar Dashboard", type="primary", help="Clique após a conclusão do script para carregar a base de dados"):
                st.cache_data.clear()
                st.rerun()

        render_footer()
        st.stop()

    # Filtros interativos na barra lateral
    filters = render_sidebar(df_raw)
    df_filtrado = filter_data(df_raw, filters)

    # Validação de dados filtrados pelos seletores da barra lateral
    if df_filtrado.empty:
        st.warning(
            "Nenhum veículo elétrico encontrado com os filtros selecionados. Ajuste os filtros na barra lateral.",
            icon=":material/warning:",
        )
        st.stop()

    # Seção de Métricas Principais (KPIs)
    render_kpis(df_filtrado)
    st.markdown("---")

    # Abas de Análise e Dados
    tab_eficiencia, tab_conpet, tab_tabela = st.tabs([
        ":material/bar_chart: Autonomia & Eficiência",
        ":material/eco: Selo CONPET & Classificação PBE",
        ":material/table_chart: Tabela Oficial Homologada",
    ])

    with tab_eficiencia:
        render_charts(df_filtrado)

    with tab_conpet:
        render_conpet_and_pbe_tab(df_filtrado)

    with tab_tabela:
        render_table(df_filtrado)

    # Rodapé institucional
    render_footer()


if __name__ == "__main__":
    main()
