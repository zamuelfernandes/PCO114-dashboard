"""Componente de geração e renderização dos gráficos analíticos Plotly para veículos 100% elétricos."""

import pandas as pd
import plotly.express as px
import streamlit as st

from src.config import CATEGORY_COLOR_MAP, PLOTLY_CONFIG_PT_BR


def render_scatter_chart(df_filtrado: pd.DataFrame):
    """Renderiza o gráfico de dispersão: Autonomia Oficial (km) vs. Consumo Energético (MJ/km)."""
    st.subheader(
        "Autonomia Oficial vs. Consumo Energético (MJ/km)",
        help=(
            "Correlação técnica entre a autonomia oficial homologada pelo Inmetro e o consumo energético oficial em MJ/km. "
            "Quanto mais alto e mais à esquerda estiver o veículo elétrico no gráfico, maior o alcance com menor consumo de energia. "
            "O tamanho da bolha reflete a eficiência equivalente em km/l na cidade."
        ),
    )

    df_plot = df_filtrado.copy()
    if df_plot.empty:
        st.info("Nenhum veículo elétrico encontrado com os filtros selecionados.")
        return

    # Garante tamanho positivo para as bolhas
    df_plot["tamanho_bolha"] = df_plot["km_l_equivalente_cidade"].fillna(20.0).clip(lower=10.0, upper=70.0)

    st.caption(":material/star: **Questão Central:** Modelos no topo e à esquerda entregam a melhor relação de longo alcance com menor gasto de energia.")

    fig_scatter = px.scatter(
        df_plot,
        x="consumo_energetico_mj_km",
        y="autonomia_inmetro_km",
        color="categoria",
        color_discrete_map=CATEGORY_COLOR_MAP,
        size="tamanho_bolha",
        custom_data=[
            "marca",
            "modelo",
            "versao",
            "categoria",
            "consumo_energetico_mj_km",
            "autonomia_inmetro_km",
            "km_l_equivalente_cidade",
            "km_l_equivalente_estrada",
            "selo_conpet",
            "classificacao_geral",
        ],
        labels={
            "consumo_energetico_mj_km": "Consumo Energético (MJ/km)",
            "autonomia_inmetro_km": "Autonomia Oficial (km)",
            "categoria": "Categoria Inmetro",
        },
        template="plotly_white",
    )

    fig_scatter.update_traces(
        hovertemplate=(
            "<b>%{customdata[0]} %{customdata[1]}</b><br>"
            "<b>Versão:</b> %{customdata[2]}<br>"
            "<b>Categoria:</b> %{customdata[3]}<br>"
            "<br>"
            "<b>Autonomia Inmetro:</b> %{customdata[5]:.0f} km<br>"
            "<b>Consumo Energético:</b> %{customdata[4]:.2f} MJ/km<br>"
            "<b>Equivalente Cidade:</b> %{customdata[6]:.1f} km/l | <b>Estrada:</b> %{customdata[7]:.1f} km/l<br>"
            "<b>Classificação PBE:</b> %{customdata[9]} | <b>Selo CONPET:</b> %{customdata[8]}"
            "<extra></extra>"
        )
    )

    fig_scatter.update_layout(
        height=520,
        showlegend=False,
        margin=dict(t=15, b=40, l=10, r=10),
        separators=",.",
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="sans-serif",
            bordercolor="#cbd5e1",
        ),
        xaxis=dict(
            title="Consumo Energético Oficial (MJ/km) - Quanto menor, mais eficiente",
            ticksuffix=" MJ/km",
            gridcolor="#f1f5f9",
        ),
        yaxis=dict(
            title="Autonomia Homologada Inmetro (km)",
            ticksuffix=" km",
            gridcolor="#f1f5f9",
        ),
    )

    st.plotly_chart(fig_scatter, width="stretch", config=PLOTLY_CONFIG_PT_BR)


def render_bar_chart(df_filtrado: pd.DataFrame, altura: int):
    """Renderiza o gráfico de barras: Quantidade de modelos elétricos por fabricante com cores por categoria."""
    st.subheader(
        "Modelos Elétricos por Fabricante",
        help=(
            "Ranking de montadoras pela quantidade de veículos 100% elétricos homologados no PBEV. "
            "As cores identificam as categorias oficiais do Inmetro."
        ),
    )

    modelos_por_marca_cat = (
        df_filtrado.groupby(["marca", "categoria"])
        .size()
        .reset_index(name="quantidade")
    )

    total_por_marca = (
        df_filtrado.groupby("marca")
        .size()
        .sort_values(ascending=True)
    )
    ordem_marcas = total_por_marca.index.tolist()
    max_qtd = int(total_por_marca.max()) if not total_por_marca.empty else 5

    fig_bar = px.bar(
        modelos_por_marca_cat,
        x="quantidade",
        y="marca",
        color="categoria",
        color_discrete_map=CATEGORY_COLOR_MAP,
        orientation="h",
        labels={"quantidade": "Qtd. de Modelos", "marca": "Fabricante", "categoria": "Categoria"},
        template="plotly_white",
        category_orders={"marca": ordem_marcas},
    )

    fig_bar.update_traces(
        cliponaxis=False,
        hovertemplate="<b>%{y}</b><br>Categoria: <b>%{fullData.name}</b><br>Modelos: <b>%{x}</b><extra></extra>",
    )

    for marca, total in total_por_marca.items():
        fig_bar.add_annotation(
            x=total + 0.15,
            y=marca,
            text=str(total),
            showarrow=False,
            xanchor="left",
            yanchor="middle",
            font=dict(size=12, color="#0f172a"),
        )

    fig_bar.update_layout(
        height=altura,
        showlegend=False,
        margin=dict(l=10, r=40, t=10, b=30),
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="sans-serif",
            bordercolor="#cbd5e1",
        ),
        xaxis=dict(
            title="Número de Modelos / Versões",
            dtick=1,
            range=[0, max_qtd + 1.2],
            gridcolor="#f1f5f9",
        ),
        yaxis=dict(title="", tickfont=dict(size=12, color="#0f172a")),
    )

    st.plotly_chart(fig_bar, width="stretch", config=PLOTLY_CONFIG_PT_BR)


def render_box_chart(df_filtrado: pd.DataFrame, altura: int):
    """Renderiza o box plot de distribuição de autonomia por categoria oficial."""
    st.subheader(
        "Distribuição de Autonomia por Categoria",
        help=(
            "Dispersão do alcance homologado entre as categorias oficiais de veículos elétricos no PBEV. "
            "A caixa representa o intervalo interquartil (Q1 a Q3), a linha central a mediana, "
            "e os pontos isolados os valores atípicos."
        ),
    )

    fig_box = px.box(
        df_filtrado,
        x="categoria",
        y="autonomia_inmetro_km",
        color="categoria",
        color_discrete_map=CATEGORY_COLOR_MAP,
        points="outliers",
        labels={
            "categoria": "Categoria Inmetro",
            "autonomia_inmetro_km": "Autonomia Oficial (km)",
        },
        template="plotly_white",
    )

    fig_box.update_layout(
        height=altura,
        showlegend=False,
        margin=dict(t=10, b=30, l=10, r=10),
        separators=",.",
        yaxis=dict(
            title="Autonomia Homologada (km)",
            ticksuffix=" km",
            gridcolor="#f1f5f9",
        ),
        xaxis=dict(title=""),
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="sans-serif",
            bordercolor="#cbd5e1",
        ),
    )

    st.plotly_chart(fig_box, width="stretch", config=PLOTLY_CONFIG_PT_BR)


def render_charts(df_filtrado: pd.DataFrame):
    """Renderiza a aba principal de gráficos de autonomia e eficiência."""
    col_g1, col_g2 = st.columns(2)
    qtd_marcas = df_filtrado["marca"].nunique()
    altura_graficos = max(450, qtd_marcas * 26 + 80)

    with col_g1:
        render_bar_chart(df_filtrado, altura_graficos)

    with col_g2:
        render_box_chart(df_filtrado, altura_graficos)

    st.markdown("---")

    render_scatter_chart(df_filtrado)


def render_conpet_and_pbe_tab(df_filtrado: pd.DataFrame):
    """Renderiza a aba analítica com Selo CONPET, Classificações PBE e Rendimento Cidade vs. Estrada."""
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Selo CONPET de Eficiência Energética", help="Proporção de veículos elétricos que alcançaram a distinção máxima do Selo CONPET.")
        conpet_counts = df_filtrado["selo_conpet"].value_counts().reset_index()
        conpet_counts.columns = ["Selo CONPET", "Quantidade"]
        fig_donut = px.pie(
            conpet_counts,
            names="Selo CONPET",
            values="Quantidade",
            hole=0.55,
            color="Selo CONPET",
            color_discrete_map={"Sim": "#00CC96", "Não": "#cbd5e1"},
            template="plotly_white",
        )
        fig_donut.update_traces(textposition="inside", textinfo="percent+label")
        fig_donut.update_layout(
            height=380,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                title_text="Selo CONPET:",
            ),
            margin=dict(t=10, b=10),
        )
        st.plotly_chart(fig_donut, width="stretch", config=PLOTLY_CONFIG_PT_BR)

    with col2:
        st.subheader("Classificação Geral PBE (Nota A-E)", help="Distribuição das notas gerais de eficiência energética conferidas pelo Inmetro.")
        pbe_counts = df_filtrado["classificacao_geral"].replace("-", "Sem Nota").value_counts().reset_index()
        pbe_counts.columns = ["Nota PBE", "Quantidade"]
        fig_pbe = px.bar(
            pbe_counts,
            x="Nota PBE",
            y="Quantidade",
            color="Nota PBE",
            color_discrete_map={"A": "#00CC96", "B": "#636EFA", "C": "#FFA15A", "D": "#FF6692", "E": "#EF553B"},
            template="plotly_white",
        )
        fig_pbe.update_layout(
            height=380,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                title_text="Nota PBE:",
            ),
            margin=dict(t=10, b=30),
            xaxis=dict(categoryorder="array", categoryarray=["A", "B", "C", "D", "E", "Sem Nota"]),
        )
        st.plotly_chart(fig_pbe, width="stretch", config=PLOTLY_CONFIG_PT_BR)

    # Gráfico de Rendimento Equivalente: Cidade vs Estrada
    st.subheader(
        "Rendimento Equivalente: Cidade vs. Estrada (km/l)",
        help="Comparativo entre o rendimento equivalente urbano e rodoviário. Em veículos elétricos, o consumo urbano costuma ser superior devido à regeneração em frenagens.",
    )
    fig_equiv = px.scatter(
        df_filtrado,
        x="km_l_equivalente_estrada",
        y="km_l_equivalente_cidade",
        color="categoria",
        color_discrete_map=CATEGORY_COLOR_MAP,
        size="autonomia_inmetro_km",
        custom_data=["marca", "modelo", "versao", "categoria", "km_l_equivalente_cidade", "km_l_equivalente_estrada", "autonomia_inmetro_km"],
        labels={
            "km_l_equivalente_estrada": "Equivalente Estrada (km/l)",
            "km_l_equivalente_cidade": "Equivalente Cidade (km/l)",
            "categoria": "Categoria Inmetro",
        },
        template="plotly_white",
    )
    fig_equiv.update_traces(
        hovertemplate=(
            "<b>%{customdata[0]} %{customdata[1]}</b><br>"
            "<b>Versão:</b> %{customdata[2]}<br>"
            "<b>Categoria:</b> %{customdata[3]}<br>"
            "<br>"
            "<b>Equivalente Cidade:</b> %{customdata[4]:.1f} km/l<br>"
            "<b>Equivalente Estrada:</b> %{customdata[5]:.1f} km/l<br>"
            "<b>Autonomia:</b> %{customdata[6]:.0f} km"
            "<extra></extra>"
        )
    )
    fig_equiv.update_layout(height=450, showlegend=False, margin=dict(t=10, b=30), separators=",.")
    st.plotly_chart(fig_equiv, width="stretch", config=PLOTLY_CONFIG_PT_BR)
