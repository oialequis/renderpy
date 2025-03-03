import streamlit as st
import pandas as pd
import sqlite3 as db


# Criar conexão com o banco de dados SQLite
conn = db.connect("database.db", check_same_thread=False)
cursor = conn.cursor()
def validar_login(nome, senha):
    cursor.execute("SELECT * FROM usuarios WHERE nome = ? AND senha = ?", (nome, senha))
    return cursor.fetchone() is not None



def botao_teste():
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


   
def login():
    if validar_login(username, password):
        st.success("LOGADO COM SUCESSO")
        st.session_state.show_login = False
        st.rerun()
    
        
    else:
        st.error("USUÁRIO OU SENHA INCORRETOS")
       





if 'show_login' not in st.session_state:
    st.session_state.show_login = True

if st.session_state.show_login:
    st.title("ENTRAR")
    username = st.text_input("USUÁRIO")
    password = st.text_input("SENHA", type='password')
    
    col1, col2, col3 = st.columns([1,0.1,1])
    with col3: 
        if st.button("CADASTRAR"):
            print("CADASTRAR")
    with col1:
        if st.button("ENTRAR"):
            st.session_state.username = username
            login()
        
else:
     #TELA PRINCIPAL
     user_conectado = st.session_state.username
     st.title(f"Bem-vindo {user_conectado}")

     uploaded_file = st.file_uploader("Escolha uma SRA.xlsx", type=["xlsx"])
     if st.button("Enviar arquivo."):
        botao_teste()
    
     