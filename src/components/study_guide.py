"""Componente explicativo sobre o contexto do trabalho acadêmico (Visualização de Informação).

Apresenta o público-alvo, a demanda de informação e as perguntas orientadoras
com linguagem acessível, direta e destaque para a questão central.
"""

import streamlit as st


def render_study_guide():
    """Renderiza a aba explicativa com Público-Alvo, Demanda e Perguntas do Estudo."""
    st.subheader(
        "Entenda o Estudo: O que este painel responde?",
        help="Contexto do estudo, público-alvo, demandas de informação e as perguntas que guiaram a criação das visualizações.",
    )
    st.markdown(
        "Este painel foi desenvolvido para transformar dados técnicos e complexos de testes oficiais do **Inmetro (PBEV)** "
        "em respostas práticas, diretas e visuais para quem quer entender a realidade dos carros 100% elétricos no Brasil."
    )

    # 1. Público-Alvo e Demanda de Informação em duas colunas elegantes
    col_pub, col_dem = st.columns(2)

    with col_pub:
        with st.container(border=True):
            st.markdown("#### :material/groups: Para quem é este painel? (Público-Alvo)")
            st.markdown(
                """
                - **Motoristas e futuros compradores:** Pessoas que pensam em comprar um carro elétrico, mas têm receio da bateria acabar no caminho (*"ansiedade de autonomia"*) ou dúvidas se a economia na tomada realmente compensa.
                - **Empresas e gestores de frota:** Profissionais que precisam decidir se vale a pena substituir veículos a combustão por elétricos, buscando cortar gastos com combustível e reduzir emissões de carbono.
                - **Curiosos e entusiastas:** Qualquer pessoa interessada em acompanhar como a tecnologia de carros elétricos está evoluindo e quais marcas estão trazendo novidades ao Brasil.
                """
            )

    with col_dem:
        with st.container(border=True):
            st.markdown("#### :material/manage_search: O que essas pessoas querem saber? (Demanda de Informação)")
            st.markdown(
                """
                - **A verdade além do comercial:** Descobrir quanto o carro realmente anda com uma carga completa em testes oficiais e padronizados, sem depender apenas das promessas das montadoras.
                - **O equilíbrio ideal:** Identificar quais modelos andam muito gastando pouca energia, evitando carros que têm boa autonomia apenas porque carregam baterias gigantescas e pesadas.
                - **Urbano vs. Estrada:** Entender na prática como o trânsito da cidade afeta a bateria em comparação com viagens rodoviárias.
                """
            )

    st.markdown("---")

    # 2. Perguntas Norteadoras
    st.markdown("### :material/quiz: As 5 Perguntas que Guiaram este Painel")
    st.caption("Entre as principais dúvidas sobre carros elétricos, definimos uma questão central de destaque e 4 perguntas complementares:")

    # 1. Questão Central da Análise (Estrutura Nativa Padrão)
    with st.container(border=True):
        st.caption(":material/star: **QUESTÃO CENTRAL DA ANÁLISE**")
        st.markdown("##### 1. Qual carro anda mais gastando o mínimo de energia?")
        st.markdown(
            """
            *Ter uma bateria enorme garante rodar muitos quilômetros, mas deixa o carro pesado e "gastão". 
            Existe um ponto de equilíbrio ideal? Quais modelos no Brasil conseguem entregar bastante autonomia sem desperdiçar energia na tomada?*
            
            :material/arrow_forward: *Veja a resposta no gráfico de **Autonomia vs. Consumo (Dispersão)** na aba **Autonomia & Eficiência**.*
            """
        )

    # Perguntas 2 a 5 dispostas em coluna sequencial
    with st.container(border=True):
        st.markdown("##### 2. O tamanho do carro muda muito o quanto ele consegue rodar?")
        st.markdown(
            """
            *Carros pequenos (compactos urbanos) andam muito menos que os SUVs grandalhões de luxo? 
            Existem modelos que surpreendem e superam a média de alcance da sua categoria?*
            
            :material/arrow_forward: *Veja a resposta no gráfico de **Distribuição por Categoria (Boxplot)** na aba **Autonomia & Eficiência**.*
            """
        )

    with st.container(border=True):
        st.markdown("##### 3. Quais marcas oferecem mais opções de elétricos no Brasil?")
        st.markdown(
            """
            *Quem está liderando a variedade de modelos no país: montadoras tradicionais ou novas marcas que chegaram recentemente? 
            E em quais tipos de veículos elas estão apostando (populares, SUVs ou sedãs)?*
            
            :material/arrow_forward: *Veja a resposta no gráfico de **Modelos por Fabricante** na aba **Autonomia & Eficiência**.*
            """
        )

    with st.container(border=True):
        st.markdown("##### 4. É verdade que carro elétrico gasta menos na cidade do que na estrada?")
        st.markdown(
            """
            *Diferente dos carros comuns a combustão (que gastam mais no trânsito), o elétrico recarrega a bateria toda vez que freia. 
            Qual é o tamanho real dessa vantagem urbana no dia a dia dos modelos à venda no Brasil?*
            
            :material/arrow_forward: *Veja a resposta no gráfico **Rendimento Urbano vs. Rodoviário** na aba **Selo CONPET & Classificação PBE**.*
            """
        )

    with st.container(border=True):
        st.markdown("##### 5. Todos os carros elétricos merecem selo de eficiência máxima?")
        st.markdown(
            """
            *Ser 100% elétrico é garantia automática de nota máxima? Quantos veículos realmente conquistam o cobiçado Selo CONPET 
            de alta eficiência do governo brasileiro e quantos deixam a desejar?*
            
            :material/arrow_forward: *Veja a resposta nos gráficos de **Selo CONPET e Notas PBE** na aba **Selo CONPET & Classificação PBE**.*
            """
        )
