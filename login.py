import streamlit as st
import json
import requests
from google_auth_oauthlib.flow import Flow
import os
import base64

# Importar os módulos
import transactions
import budget_overview
import financial_reports
import financial_goals
import notifications
import security
import google_sheets

# Função para carregar as credenciais do Google OAuth
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
            redirect_uri=os.environ.get("APP_URI")  # URL correta que você está usando
        )

        authorization_url, state = flow.authorization_url(prompt='consent', include_granted_scopes='true')

        # Estilo CSS para a tela de login
        css_style = """
        <style>
            body {
                background-color: #f4f4f9;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            .login-container {
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background: linear-gradient(145deg, #e4e4e8, #ffffff);
                box-shadow: 10px 10px 20px #cbcbcf, -10px -10px 20px #ffffff;
                border-radius: 12px;
                padding: 20px;
                max-width: 400px;
                margin: auto;
                text-align: center;
            }
            .login-header {
                font-size: 2.5rem;
                color: #333;
                margin-bottom: 20px;
            }
            .google-button {
                background-color: #4285f4;
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 4px;
                cursor: pointer;
                transition: background-color 0.3s ease;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .google-button:hover {
                background-color: #357ae8;
            }
            .google-icon {
                vertical-align: middle;
                margin-right: 8px;
            }
            .sub-text {
                color: #666;
                font-size: 0.9rem;
                margin-top: 15px;
            }
            .footer {
                margin-top: 30px;
                font-size: 0.8rem;
                color: #aaa;
            }
            .logo {
                width: 150px;
                margin-bottom: 20px;
            }
        </style>
        """

        # Imagem da logo em base64
        logo_base64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAfQAAAH0CAYAAACtKy84AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAABIAAAASABGyWs+AAAA..."

        # HTML para a tela de login
        login_html = f"""
        <div class="login-container">
            <img src="{logo_base64}" alt="Logo Meu DinDinz" class="logo">
            <h1 class="login-header">Meu DinDinz</h1>
            <button class="google-button" onclick="window.location.href='{authorization_url}'">
                <img class="google-icon" src="https://www.google.com/favicon.ico" alt="Google icon" width="20" height="20">
                Entrar com Google
            </button>
            <div class="sub-text">Acesse sua conta com segurança</div>
            <div class="footer">© 2024 Meu DinDinz. Todos os direitos reservados.</div>
        </div>
        """

        # Renderizar o CSS e HTML
        st.markdown(css_style, unsafe_allow_html=True)
        st.markdown(login_html, unsafe_allow_html=True)

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
                st.experimental_rerun()  # Redirecionar após login
                return True
            except Exception as e:
                st.error(f"Erro ao obter token: {e}")
    return False

# Função para exibir a aplicação principal
def show_main_app():
    st.sidebar.title("Navegação")
    selection = st.sidebar.radio("Ir para", ["Transações", "Visão Geral do Orçamento", "Relatórios Financeiros",
                                             "Metas Financeiras", "Notificações", "Segurança", "Integração com Google Sheets"])

    st.sidebar.write(f"Usuário: {st.session_state['user_info']['name']}")

    if selection == "Transações":
        transactions.transaction_interface()
    elif selection == "Visão Geral do Orçamento":
        transactions_data = []  # Substitua pelos dados reais
        budget_overview.budget_overview(transactions_data)
    elif selection == "Relatórios Financeiros":
        transactions_data = []  # Substitua pelos dados reais
        financial_reports.financial_reports(transactions_data)
    elif selection == "Metas Financeiras":
        financial_goals.financial_goals_interface()
    elif selection == "Notificações":
        notifications.notifications_interface()
    elif selection == "Segurança":
        security.security_interface()
    elif selection == "Integração com Google Sheets":
        google_sheets.google_sheets_interface()

if __name__ == "__main__":
    st.set_page_config(page_title="Meu DinDinz", layout="wide")
    
    # Checar se o usuário já está logado
    if 'user_info' not in st.session_state:
        if google_login():
            show_main_app()
    else:
        show_main_app()
