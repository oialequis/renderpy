import streamlit as st
import pandas as pd
import os
import getpass

usuarios_permitidos = ["Alex","Beatriz"]

    

def botao_teste():
    usuario_atual = getpass.getuser()
    if usuario_atual in usuarios_permitidos:
        print("USUÁRIO PERMITIDO")
        st.title("PERMISSÃO CONCEDIDA")
    else:
        print("USUARIO NAO TA NA LISTA DE PERMISSAO")
        st.title("PERMISSÃO NEGADA")
    df = pd.read_excel(uploaded_file)
    df = df.drop(0)
    df.columns = df.loc[1]
    df = df[1:]

    # Seleção de colunas com .loc
    df_filtro = df.loc[:, ['Matricula', 'Nome', 'Data Admis.', 'Sit. Folha', 'Desc.Funcao', 'Desc. Depto', 'CPF']]

    # Conversão e formatação de datas com .loc
    df_filtro['Matricula'] = df_filtro['Matricula'].astype(str)
    df_filtro['Matricula'] = df_filtro['Matricula'].str.replace(',', '').str.replace('.', '').astype(str)
    df_filtro['Data Admis.'] = pd.to_datetime(df_filtro['Data Admis.'], errors='coerce')
    df_filtro['Data Admis.'] = df_filtro['Data Admis.'].apply(lambda x: x.strftime('%d/%m/%Y') if pd.notna(x) else '')


    # Limpeza e substituição de dados com .loc
    df_filtro.loc[:, 'Sit. Folha'] = df_filtro.loc[:, 'Sit. Folha'].fillna('ATIVO')
    df_filtro.loc[:, 'Sit. Folha'] = df_filtro.loc[:, 'Sit. Folha'].replace('F', "FÉRIAS")
    df_filtro.loc[:, 'Sit. Folha'] = df_filtro.loc[:, 'Sit. Folha'].replace('A', "AFASTADO")

    # Remoção de dados com .loc
    funcao_para_remover = ['AUTONOMO','MEDICO RESIDENTE','ENFERMEIRO RESIDENTE']
    df_filtro = df_filtro.loc[~df_filtro['Desc.Funcao'].str.lower().isin([funcao.lower() for funcao in funcao_para_remover])]

    grafico_filtrado = df_filtro.loc[:, 'Sit. Folha'].value_counts()
    # Tratar valores ausentes e converter para inteiro
    grafico_filtrado = pd.to_numeric(grafico_filtrado, errors='coerce').fillna(0).astype(int)

    # Redefinir os índices da Series
    grafico_filtrado = grafico_filtrado.reset_index()

    # Renomear as colunas para que o Streamlit as interprete corretamente
    grafico_filtrado.columns = ['Rótulos', 'Valores']

    st.bar_chart(grafico_filtrado, x='Rótulos', y='Valores')
    st.write(grafico_filtrado)
 




##STREAMLIT##

st.title("teste")
uploaded_file = st.file_uploader("Escolha um arquivo XLSX", type=["xlsx"])

##########
if st.button("Clique Aqui"):
    botao_teste()


