import streamlit as st
import json
import requests
from google_auth_oauthlib.flow import Flow
import os
from dotenv import load_dotenv

# Importar os módulos
import transactions
import budget_overview
import financial_reports
import financial_goals
import notifications
import security
import google_sheets

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
    if 'user_info' not in st.session_state:
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
                    <div class="illustration">
                        <img src="https://via.placeholder.com/600x400" alt="Ilustração">
                    </div>
                    <div class="login-form">
                        <h1>Bem-vindo ao Meu DinDinz</h1>
                        <p>Por favor, faça login para continuar.</p>
                        <a href="{authorization_url}" class="google-button">
                            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/512px-Google_%22G%22_Logo.svg.png" alt="Google Logo">
                            Entrar com Google
                        </a>
                    </div>
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
                    st.experimental_rerun()  # Recarrega a aplicação após login para renderizar a interface principal
                except Exception as e:
                    st.error(f"Erro ao obter token: {e}")
        else:
            st.error("Configurações de OAuth inválidas.")
    else:
        show_main_app()  # Se já estiver logado, mostra a aplicação

# Função principal para mostrar a aplicação após o login
def show_main_app():
    st.sidebar.title("Navegação")
    selection = st.sidebar.radio("Ir para", [
        "Transações",
        "Visão Geral do Orçamento",
        "Relatórios Financeiros",
        "Metas Financeiras",
        "Notificações",
        "Segurança",
        "Integração com Google Sheets"
    ])

    st.sidebar.write(f"Usuário: {st.session_state['user_info']['name']}")

    # Chamadas de função para diferentes seções
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
            margin: 0;
        }

        .login-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #ffffff;
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            max-width: 900px;
            width: 100%;
            margin: auto;
            overflow: hidden;
        }

        .illustration {
            flex: 1;
            background: #f0f0f0;
            padding: 40px;
        }

        .illustration img {
            width: 100%;
            height: auto;
        }

        .login-form {
            flex: 1;
            padding: 40px;
            text-align: center;
        }

        .login-form h1 {
            color: #333;
            margin-bottom: 20px;
            font-weight: 500;
        }

        .login-form p {
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

    # Chama a função de login, se necessário
    google_login()