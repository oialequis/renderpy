import streamlit as st
import requests

# Carregar o token do GitHub armazenado no secrets.toml
github_token = st.secrets["GITHUB_TOKEN"]

# Função para acessar o arquivo no GitHub
def get_github_file(repo_owner, repo_name, file_path, token):
    # URL da API do GitHub para acessar o conteúdo do arquivo
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
    
    # Cabeçalhos para autenticação usando o token
    headers = {
        "Authorization": f"token {token}"
    }
    
    # Requisição para obter o arquivo
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        # Obter o link de download do arquivo
        file_url = response.json()['download_url']
        
        # Baixar o arquivo
        file_response = requests.get(file_url)
        
        # Retornar o conteúdo do arquivo
        return file_response.content
    else:
        st.error(f"Erro ao acessar o arquivo: {response.status_code}")
        return None

# Streamlit UI
st.title("Exibir Arquivo do Repositório Privado do GitHub")

# Informações do repositório
repo_owner = "oialequis"  # Substitua pelo nome do proprietário do repositório
repo_name = "renderpy"  # Substitua pelo nome do repositório
file_path = "teste.jpg"  # Substitua pelo caminho do arquivo no repositório

# Chamar a função para obter o arquivo
file_content = get_github_file(repo_owner, repo_name, file_path, github_token)

# Exibir o arquivo se foi obtido com sucesso
if file_content:
    st.image(file_content, caption="Imagem do Repositório Privado")
