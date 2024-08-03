# src/authentication.py

import os
import hashlib
import streamlit as st
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Credenciais do Google OAuth 2.0
CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
AUTHORIZATION_BASE_URL = 'https://accounts.google.com/o/oauth2/auth'
TOKEN_URL = 'https://accounts.google.com/o/oauth2/token'
REDIRECT_URI = 'https://meudindinz-gkswcxjh3pge74l9w6bwvq.streamlit.app/'  # Certifique-se de que coincide com o console

# Scope de permissão
SCOPE = ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']

def generate_state():
    """Função para gerar um estado seguro com hash."""
    return hashlib.sha256(os.urandom(1024)).hexdigest()

def authenticate_user():
    """Função para autenticar o usuário via Google OAuth 2.0"""

    # Verificar se o usuário já está autenticado
    if 'authenticated' in st.session_state and st.session_state.authenticated:
        st.write("Usuário já autenticado.")
        return st.session_state.user_info

    # Criar a sessão OAuth2
    google = OAuth2Session(CLIENT_ID, scope=SCOPE, redirect_uri=REDIRECT_URI)

    # Obter URL de autorização
    authorization_url, state = google.authorization_url(
        AUTHORIZATION_BASE_URL,
        access_type="offline",
        prompt="select_account"
    )

    # Armazenar o estado na sessão do Streamlit
    st.session_state['oauth_state'] = state
    st.write(f"Estado de autorização enviado: {state}")

    # Exibir o link de login se o código não estiver presente
    if 'code' not in st.query_params:
        st.write("Por favor, faça login para continuar.")
        st.markdown(f'<a href="{authorization_url}" target="_self">Login com Google</a>', unsafe_allow_html=True)
        return None

    # Recuperar o estado armazenado na sessão
    stored_state = st.session_state.get('oauth_state')
    st.write(f"Estado de autorização armazenado na sessão: {stored_state}")

    # Verificar se o estado é válido
    query_state = st.query_params.get('state', None)
    st.write(f"Estado de autorização recebido: {query_state}")

    if query_state != stored_state:
        st.error("Estado inválido de OAuth.")
        st.error(f"Esperado: {stored_state}, Recebido: {query_state}")
        return None

    # Ler o URL do callback
    code = st.query_params['code']
    try:
        token = google.fetch_token(
            TOKEN_URL,
            client_secret=CLIENT_SECRET,
            code=code
        )
    except Exception as e:
        st.error("Erro ao obter o token de acesso. Por favor, tente novamente.")
        st.error(str(e))
        return None

    # Obter informações do usuário
    try:
        user_info = google.get('https://www.googleapis.com/oauth2/v1/userinfo').json()
        st.session_state.authenticated = True
        st.session_state.user_info = user_info
        st.success(f"Bem-vindo, {user_info['name']}!")
        return user_info
    except Exception as e:
        st.error("Erro ao obter informações do usuário. Por favor, tente novamente.")
        st.error(str(e))
        return None
