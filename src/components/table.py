"""
Componente de exibição da tabela de dados e botão para download.
"""

import pandas as pd
import streamlit as st


def render_table(df_filtrado: pd.DataFrame):
    """Renderiza a tabela detalhada com os dados dos veículos e botão de exportação CSV."""
    st.subheader(
        "Base de Dados Selecionada",
        help="Tabela detalhada com especificações técnicas e comerciais dos veículos filtrados. Permite ordenação pelas colunas.",
    )

    df_exibicao = df_filtrado.copy()
    df_exibicao["preco_formatado"] = df_exibicao["preco_estimado_brl"].apply(
        lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    )

    colunas_ordenadas = [
        "marca",
        "modelo",
        "versao",
        "ano_modelo",
        "categoria",
        "preco_formatado",
        "autonomia_inmetro_km",
        "capacidade_bateria_kwh",
        "potencia_cv",
        "tempo_recarga_rapida_min",
        "tipo_conector",
        "tracao",
    ]

    st.dataframe(
        df_exibicao[colunas_ordenadas].rename(
            columns={
                "marca": "Marca",
                "modelo": "Modelo",
                "versao": "Versão",
                "ano_modelo": "Ano",
                "categoria": "Categoria",
                "preco_formatado": "Preço Estimado",
                "autonomia_inmetro_km": "Autonomia (km)",
                "capacidade_bateria_kwh": "Bateria (kWh)",
                "potencia_cv": "Potência (cv)",
                "tempo_recarga_rapida_min": "Carga Rápida (min)",
                "tipo_conector": "Conector",
                "tracao": "Tração",
            }
        ),
        width="stretch",
        hide_index=True,
    )

    # Botão para download do CSV filtrado
    csv_bytes = df_filtrado.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Baixar Dados Filtrados em CSV",
        data=csv_bytes,
        file_name="carros_eletricos_filtrados.csv",
        mime="text/csv",
        icon=":material/download:",
        help="Exporta a planilha atual com os filtros aplicados em formato .csv",
    )
