import streamlit as st
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
import os
import json
import requests

# Configurar o ambiente do Google OAuth
def load_google_oauth():
    try:
        # Carregar credenciais de uma variável de ambiente
        client_secret_json = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET", "{}")
        return json.loads(client_secret_json)
    except Exception as e:
        st.error(f"Erro ao carregar as credenciais do Google OAuth: {e}")
        return None

# Função para autenticação do Google
def google_login():
    client_secrets = load_google_oauth()

    if client_secrets:
        flow = Flow.from_client_config(
            client_secrets,
            scopes=[
                "https://www.googleapis.com/auth/userinfo.email",
                "https://www.googleapis.com/auth/userinfo.profile",
                "openid"
            ],
            redirect_uri=os.environ.get("APP_URI")  # Substitua pela URL correta que você está usando
        )

        authorization_url, state = flow.authorization_url(prompt='consent')

        # Estrutura HTML do botão
        st.markdown(f"""
            <div class="login-container">
                <h1>Bem-vindo ao Meu DinDinz</h1>
                <p>Por favor, faça login para continuar.</p>
                <a href="{authorization_url}" class="google-button">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/512px-Google_%22G%22_Logo.svg.png" alt="Google Logo">
                    Entrar com Google
                </a>
            </div>
        """, unsafe_allow_html=True)

        # Obter o código de autorização a partir dos parâmetros da URL
        query_params = st.experimental_get_query_params()
        code = query_params.get("code")

        if code:
            try:
                # Adicionar o estado ao fluxo
                flow.fetch_token(code=code[0])

                credentials = flow.credentials
                session = requests.Session()
                token = f"Bearer {credentials.token}"
                headers = {"Authorization": token}
                user_info = session.get('https://www.googleapis.com/userinfo/v2/me', headers=headers).json()

                st.session_state['user_info'] = user_info  # Armazenar informações do usuário na sessão
                st.success("Login realizado com sucesso!")
                return True
            except Exception as e:
                st.error(f"Erro ao obter token: {e}")
    return False

def main():
    st.set_page_config(
        page_title="MeuDinDinz Login",
        layout="centered"
    )

    # CSS styles
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

        body {
            font-family: 'Roboto', sans-serif;
            background-color: #f4f4f9;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .login-container {
            background: #ffffff;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            text-align: center;
            max-width: 400px;
            width: 100%;
            margin: auto;
        }

        .login-container h1 {
            color: #333;
            margin-bottom: 20px;
        }

        .login-container p {
            color: #555;
            margin-bottom: 30px;
        }

        .google-button {
            background-color: #4285f4;
            color: white;
            font-size: 18px;
            padding: 12px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s ease, transform 0.2s ease;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            text-decoration: none;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        .google-button:hover {
            background-color: #357ae8;
            transform: translateY(-2px);
        }

        .google-button img {
            width: 20px;
            height: 20px;
        }

        </style>
    """, unsafe_allow_html=True)

    if 'user_info' not in st.session_state:
        google_login()
    else:
        user_info = st.session_state['user_info']
        st.success(f"Bem-vindo, {user_info['name']}!")
        st.image(user_info['picture'], width=100)
        st.markdown(f"Email: {user_info['email']}")

if __name__ == "__main__":
    main()