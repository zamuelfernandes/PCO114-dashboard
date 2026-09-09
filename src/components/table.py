"""Componente de exibição da tabela de dados oficiais e botão para download."""

import pandas as pd
import streamlit as st


def render_table(df_filtrado: pd.DataFrame):
    """Renderiza a tabela detalhada com os dados homologados do Inmetro e botão de exportação CSV."""
    st.subheader(
        "Tabela de Homologação Oficial PBEV / Inmetro",
        help="Planilha completa com especificações energéticas e certificações dos modelos 100% elétricos filtrados. Clique no cabeçalho das colunas para ordenar.",
    )

    df_exibicao = df_filtrado.copy()

    colunas_ordenadas = [
        "marca",
        "modelo",
        "versao",
        "categoria",
        "cambio",
        "autonomia_inmetro_km",
        "consumo_energetico_mj_km",
        "km_l_equivalente_cidade",
        "km_l_equivalente_estrada",
        "classificacao_geral",
        "selo_conpet",
        "ar_condicionado",
        "direcao",
    ]

    nomes_colunas = {
        "marca": "Marca",
        "modelo": "Modelo",
        "versao": "Versão",
        "categoria": "Categoria Inmetro",
        "cambio": "Câmbio",
        "autonomia_inmetro_km": "Autonomia (km)",
        "consumo_energetico_mj_km": "Consumo (MJ/km)",
        "km_l_equivalente_cidade": "km/l Cidade",
        "km_l_equivalente_estrada": "km/l Estrada",
        "classificacao_geral": "PBE Geral",
        "selo_conpet": "Selo CONPET",
        "ar_condicionado": "Ar Cond.",
        "direcao": "Direção",
    }

    st.dataframe(
        df_exibicao[colunas_ordenadas].rename(columns=nomes_colunas),
        width="stretch",
        hide_index=True,
    )

    # Botão para download do CSV filtrado
    csv_bytes = df_filtrado.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Baixar Dados Oficiais Filtrados (CSV)",
        data=csv_bytes,
        file_name="carros_eletricos_inmetro_filtrados.csv",
        mime="text/csv",
        icon=":material/download:",
        help="Exporta a planilha atual com os filtros aplicados em formato .csv",
    )
