import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier

# Função para carregar o modelo treinado
@st.cache_resource
def load_model():
    with open("modelo_melhorado.pkl", "rb") as f:
        model = pickle.load(f)
    return model

# Função para carregar os dados
@st.cache_data
def load_data():
    return pd.read_csv("Dataset_13_02.csv")

modelo = load_model()
df = load_data()

# Configuração inicial
st.set_page_config(page_title="Dashboard de Predições", layout="wide")
st.title("📊 Dashboard Abrahão e Lucas")

# Sidebar para configurações
st.sidebar.header("Configurações")
opcao = st.sidebar.radio("Escolha uma opção:", ["Visualização de Dados", "Predição"])

# Exibir Dados
if opcao == "Visualização de Dados":
    st.subheader("🔍 Dados Brutos")
    st.dataframe(df.head())

    st.subheader("📈 Gráficos Interativos")

    # Gráfico de barras
    col = st.selectbox("Escolha uma coluna para visualizar:", df.columns)
    fig, ax = plt.subplots()
    sns.histplot(df[col], kde=True, ax=ax)
    st.pyplot(fig)

# Fazer Predições
elif opcao == "Predição":
    st.subheader("🤖 Fazer uma Predição")

    idade = st.number_input("Idade", value=0)
    nome = st.text_input("Seu nome:", value="")

    selecao_status = st.selectbox("Status", ["Bom", "Médio", "Baixo"])
    selecao_regiao = st.selectbox("Região", ["Norte", "Nordeste", "Sudeste", "Sul", "Centro-Oeste"])
    selecao_sexo = st.selectbox("Sexo", ["Masculino", "Feminino"])
    selecao_domicilio = st.selectbox("Domicílio", ["Casa", "Apartamento", "Outros"])
    selecao_cozinha = st.selectbox("Possui Cozinha", ["Sim", "Não"])
    selecao_ocupacao = st.selectbox("Ocupação", ["Próprio de algum morador - já pago", "Próprio de algum morador - ainda pagando", "Alugado", "Cedido por empregador", "Cedido de outra forma", "Outra condição"])
    selecao_registro = st.selectbox("Situação do Registro", ["Urbano", "Rural"])
    selecao_tosse = st.selectbox("Presença de Tosse", ["Sim", "Não", "Não sabe/ não quis responder"])
    selecao_respiracao = st.selectbox("Tipo de Respiração", ["Sim", "Não", "Não sabe/ não quis responder"])
    selecao_alimentos = st.selectbox("Alimentos Básicos", ["Não", "Sim, raramente", "Sim, às vezes", "Sim, quase sempre", "Sim, sempre", "Não se cozinha em casa"])
    selecao_escolaridade = st.selectbox("Nível Escolaridade", ["Sem estudo", "1° ano do ensino fundamental", "1ª série/ 2°ano do ensino fundamental",
                                                                "2ª série/ 3°ano do ensino fundamental", "3ª série/ 4°ano do ensino fundamental", 
                                                                "4ª série/ 5°ano do ensino fundamental", "5ª série/ 6°ano do ensino fundamental", 
                                                                "6ª série/ 7°ano do ensino fundamental", "7ª série/ 8°ano do ensino fundamental", 
                                                                "8ª série/ 9°ano do ensino fundamental", "1°ano do ensino médio", "2°ano do ensino médio", 
                                                                "3°ano do ensino médio", "Ensino superior incompleto", "Ensino superior completo"])
    selecao_renda = st.selectbox("Faixa de Renda", ["Sem renda", "Até R$ 1.000,00", "De R$ 1.001,00 até R$ 2.000,00", "De R$ 2.001,00 até R$ 3.000,00", 
                                                    "De R$ 3.001,00 até R$ 5.000,00", "De R$ 5.001,00 até R$ 10.000,00", "R$ 10.001,00 ou mais"])
    # Adicionar as features faltantes no dashboard
    selecao_cor_pessoa = st.selectbox("Cor da Pessoa", ["Branca", "Preta", "Amarela (origem japonesa, chinesa, coreana etc.)", 
                                                    "Parda (mulata, cabocla, cafuza, mameluca ou mestiça)", 
                                                    "Indígena", "Não sabe/não quis responder"])

    selecao_moradores_alimentaram_sim = st.selectbox("Moradores que Alimentaram Acabamento (Sim)", ["Sim", "Não"])

    selecao_moradores_alimentaram_nao = st.selectbox("Moradores que Alimentaram Acabamento (Não)", ["Sim", "Não"])


    beneficios_opcoes = ["Programa Bolsa Família (PBF)", "Benefício de Prestação Continuada (BPC/LOAS)", "Bolsa ou benefício da Prefeitura Municipal", 
                         "Bolsa ou benefício do Governo do Estado", "Pensão", "Aposentadoria", "Outro benefício"]
    beneficios_selecionados = st.multiselect("Benefícios recebidos", beneficios_opcoes)
    beneficios_mapping = {
    "Programa Bolsa Família (PBF)": "A",
    "Benefício de Prestação Continuada (BPC/LOAS)": "B",
    "Bolsa ou benefício da Prefeitura Municipal": "C",
    "Bolsa ou benefício do Governo do Estado": "D",
    "Pensão": "E",
    "Aposentadoria": "F",
    "Outro benefício": "G"
    }

    beneficios_input = [1 if beneficios_mapping[ben] in beneficios_selecionados else 0 for ben in beneficios_opcoes]
    total_beneficios = len(beneficios_selecionados)

    mapping = {"Status": {"Bom": 1, "Médio": 0, "Baixo": -1}, "Região": {"Norte": 1, "Nordeste": 2, "Sudeste": 3, "Sul": 4, "Centro-Oeste": 5}, "Sexo": {"Masculino": 1, "Feminino": 2}, 
               "Domicílio": {"Casa": 1, "Apartamento": 2, "Outros": 3}, "Cozinha": {"Sim": 1, "Não": 0}, "Ocupação": {"Próprio de algum morador - já pago": 1, "Próprio de algum morador - ainda pagando": 2, 
               "Alugado": 3, "Cedido por empregador": 4, "Cedido de outra forma": 5, "Outra condição" : 6}, "Registro": {"Urbano": 1, "Rural": 2}, 
               "Tosse": {"Sim": 1, "Não": 2, "Não sabe/ não quis responder": 9}, "Respiração": {"Sim": 1, "Não": 2, "Não sabe/ não quis responder": 9}, 
               "Alimentos": {"Não": 1, "Sim, raramente": 2, "Sim, às vezes": 3, "Sim, quase sempre": 4, "Sim, sempre": 5, "Não se cozinha em casa": 6}, 
               "Escolaridade": {"Sem estudo": 0,
               "1° ano do ensino fundamental": 1,
               "1ª série/ 2°ano do ensino fundamental": 2,
               "2ª série/ 3°ano do ensino fundamental": 3,
               "3ª série/ 4°ano do ensino fundamental": 4,
               "4ª série/ 5°ano do ensino fundamental": 5,
               "5ª série/ 6°ano do ensino fundamental": 6,
               "6ª série/ 7°ano do ensino fundamental": 7,
               "7ª série/ 8°ano do ensino fundamental": 8,
               "8ª série/ 9°ano do ensino fundamental": 9,
               "1°ano do ensino médio": 10,
               "2°ano do ensino médio": 11,
               "3°ano do ensino médio": 12,
               "Ensino superior incompleto": 13,
               "Ensino superior completo": 14}, "Renda": {"Sem renda": 1, "Até R$ 1.000,00": 2, "De R$ 1.001,00 até R$ 2.000,00": 3,
               "De R$ 2.001,00 até R$ 3.000,00": 4, "De R$ 3.001,00 até R$ 5.000,00": 5,
               "De R$ 5.001,00 até R$ 10.000,00": 6, "R$ 10.001,00 ou mais": 7}}
    mapping_cor_pessoa = {
    "Branca": 1,
    "Preta": 2,
    "Amarela (origem japonesa, chinesa, coreana etc.)": 3,
    "Parda (mulata, cabocla, cafuza, mameluca ou mestiça)": 4,
    "Indígena": 5,
    "Não sabe/não quis responder": 9
    }

    mapping_sim_nao = {
        "Sim": 1, 
        "Não": 2
    }

    input_data = [
        idade, 
        mapping["Status"][selecao_status], 
        mapping["Região"][selecao_regiao], 
        mapping["Sexo"][selecao_sexo], 
        mapping["Domicílio"][selecao_domicilio], 
        mapping["Cozinha"][selecao_cozinha], 
        mapping["Ocupação"][selecao_ocupacao], 
        mapping["Registro"][selecao_registro], 
        mapping["Tosse"][selecao_tosse], 
        mapping["Respiração"][selecao_respiracao], 
        mapping["Alimentos"][selecao_alimentos], 
        mapping["Escolaridade"][selecao_escolaridade], 
        mapping["Renda"][selecao_renda]
    ] + beneficios_input + [
        total_beneficios,  # Adiciona total de benefícios
        mapping_cor_pessoa[selecao_cor_pessoa],  # Adiciona cor pessoa
        mapping_sim_nao[selecao_moradores_alimentaram_sim],  # Moradores alimentaram acabamento SIM
        mapping_sim_nao[selecao_moradores_alimentaram_nao]   # Moradores alimentaram acabamento NÃO
    ]
    if st.button("Prever"):
        resultado = modelo.predict([input_data])
        st.success(f"🧠 O modelo previu: **{resultado[0]}**")
        probabilidade = modelo.predict_proba([input_data])[0].max()
        st.write(f"Confiança da predição: {probabilidade:.2%}")

