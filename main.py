import streamlit as st
import pandas as pd
import sqlite3 as db



google_drive_id = "1FtkhmnlAUWmGaFxXDn374UsWZ0k8IYpB"

# Criar um link direto para exibir a imagem
image_url = f"https://drive.google.com/uc?export=view&id={google_drive_id}"




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
       st.title("PAINEL DE USUÁRIO")
       # Exibir a imagem no app
       st.image(image_url, caption="Imagem carregada do Google Drive")
      
     