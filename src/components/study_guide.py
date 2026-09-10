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
        "Este painel foi criado para responder de forma simples às principais dúvidas sobre carros elétricos no Brasil. "
        "Seguindo as boas práticas da disciplina de **Visualização de Informação**, organizamos a experiência em duas etapas: "
        "primeiro os **Destaques do Mercado** (com respostas rápidas e rankings populares), e depois as **Abas Analíticas** "
        "(para quem quiser mergulhar nos detalhes técnicos oficiais do Inmetro)."
    )

    # 1. Público-Alvo e Demanda de Informação em duas colunas elegantes
    col_pub, col_dem = st.columns(2)

    with col_pub:
        with st.container(border=True):
            st.markdown("#### :material/groups: Para quem é este painel? (Público-Alvo)")
            st.markdown(
                """
                - **Compradores e motoristas:** Pessoas que têm curiosidade em ter um elétrico, mas têm receio de ficar sem bateria no caminho ou querem saber se a economia na tomada é real.
                - **Empresas e frotistas:** Quem precisa decidir na ponta do lápis se compensa trocar carros a combustão por elétricos para cortar despesas e emissões.
                - **Alunos e curiosos:** Quem quer ver a fotografia atual do mercado automotivo nacional e como novas montadoras estão desafiando as marcas tradicionais.
                """
            )

    with col_dem:
        with st.container(border=True):
            st.markdown("#### :material/manage_search: O que as pessoas querem saber? (Demanda de Informação)")
            st.markdown(
                """
                - **A vida real além da propaganda:** Quanto cada modelo realmente percorre com uma bateria cheia em testes padronizados e oficiais, sem promessas vazias.
                - **O campeão do custo-benefício:** Quais carros conseguem andar muito gastando o mínimo de eletricidade, sem precisar carregar baterias excessivamente pesadas.
                - **Cidade contra estrada:** Entender na prática por que o elétrico é imbatível no anda-e-para urbano e como ele se comporta em rodovias.
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
            
            :material/arrow_forward: *Veja a resposta rápida nos rankings da aba **Destaques do Mercado** e a correlação técnica completa no gráfico de **Autonomia vs. Consumo** na aba **Autonomia & Eficiência**.*
            """
        )

    # Perguntas 2 a 5 dispostas em coluna sequencial
    with st.container(border=True):
        st.markdown("##### 2. O tamanho do carro muda muito o quanto ele consegue rodar?")
        st.markdown(
            """
            *Carros pequenos (compactos urbanos) andam muito menos que os SUVs grandalhões de luxo? 
            Existem modelos que surpreendem e superam a média de alcance da sua categoria?*
            
            :material/arrow_forward: *Veja a divisão no **Top 10 Autonomia** (aba **Destaques**) e a dispersão real no **Boxplot por Categoria** (aba **Autonomia & Eficiência**).*
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
            
            :material/arrow_forward: *Veja a resposta direta no gráfico **Cidade vs. Estrada** na aba **Destaques do Mercado**.*
            """
        )

    with st.container(border=True):
        st.markdown("##### 5. Onde consultar e comparar os dados oficiais de cada modelo?")
        st.markdown(
            """
            *Quer checar as informações completas de um veículo específico que você viu na rua ou pretende comprar? 
            Como auditar os dados brutos de homologação sem depender de promessas de comerciais?*
            
            :material/arrow_forward: *Pesquise por marca ou versão, ordene qualquer indicador técnico e baixe a planilha completa na aba **Tabela Oficial Homologada**.*
            """
        )
