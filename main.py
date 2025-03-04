import streamlit as st
import pandas as pd
import sqlite3 as db
from io import BytesIO
import requests



# Função para obter o arquivo do GitHub
def get_github_file(repo_owner, repo_name, file_path, token):
    # URL para acessar o arquivo do repositório privado
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}'
    
    # Cabeçalhos para autenticação
    headers = {'Authorization': f'token {token}'}
    
    # Requisição para obter as informações do arquivo
    response = requests.get(url, headers=headers)
    
    # Verificando se a requisição foi bem-sucedida
    if response.status_code == 200:
        file_url = response.json()['download_url']
        # Baixando o arquivo diretamente
        file_response = requests.get(file_url)
        return BytesIO(file_response.content)  # Retorna o conteúdo do arquivo
    else:
        st.error("Erro ao acessar o arquivo no GitHub")
        return None




# Informações do repositório GitHub
repo_owner = "oialequis"  # Substitua pelo nome de usuário do GitHub
repo_name = "renderpy"  # Substitua pelo nome do repositório
file_path = "teste.jpg"  # Substitua pelo caminho do arquivo




# Criar conexão com o banco de dados SQLite
conn = db.connect("database.db", check_same_thread=False)
cursor = conn.cursor()
def validar_login(nome, senha):
    cursor.execute("SELECT * FROM usuarios WHERE nome = ? AND senha = ?", (nome, senha))
    return cursor.fetchone() is not None



def botao_enviar():
    if uploaded_file is not None:
        cursor.execute("INSERT INTO files (name, data) VALUES (?, ?)", 
                    (uploaded_file.name, uploaded_file.getvalue()))
        conn.commit()
        st.success("Arquivo salvo no banco de dados!")
    
    


   
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
   if st.session_state.username == "admin":
      st.title("PAINEL DE ADMINISTRADOR")
     #TELA PRINCIPAL
      user_conectado = st.session_state.username
      st.title(f"Bem-vindo {user_conectado}")

      uploaded_file = st.file_uploader("ESCOLHA UMA IMAGEM.JPG", type=["jpg"])
      if st.button("Enviar arquivo."):
        botao_enviar()
   else:
       file = get_github_file(repo_owner, repo_name, file_path, token)
       st.title("PAINEL DE USUÁRIO..")
       st.image(file, caption="Imagem carregada do Google Drive")
      
     