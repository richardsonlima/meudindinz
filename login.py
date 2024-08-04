import streamlit as st
import json
import requests
from google_auth_oauthlib.flow import Flow
import os

# Importar os módulos
import transactions
import budget_overview
import financial_reports
import financial_goals
import notifications
import security
import google_sheets

from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()


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
            redirect_uri= os.environ.get("APP_URI")  # Substitua pela URL correta que você está usando
        )

        authorization_url, state = flow.authorization_url(prompt='consent')

        st.write("## Bem-vindo ao Meu DinDinz")
        st.write("Por favor, faça login para continuar.")
        st.write(f"[Entrar com Google]({authorization_url})")

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