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
from google_sheets import connect_to_google_sheets  # Importando a função corretamente

from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Definir o nome da planilha do Google Sheets com um valor padrão
sheet_name = os.environ.get("SHEET_NAME", "Nome_Padrao_da_Sua_Planilha")  # Substitua pelo nome padrão da sua planilha

# CSS Personalizado para uma interface visual atraente
def set_custom_css():
    st.markdown(
        """
        <style>
            /* Background do aplicativo */
            body {
                background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
                font-family: 'Arial', sans-serif;
            }

            /* Container principal */
            .main-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                padding: 20px;
            }

            /* Box de Login */
            .login-box {
                background-color: #ffffff;
                box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
                border-radius: 12px;
                padding: 40px;
                width: 100%;
                max-width: 400px;
                text-align: center;
                transition: transform 0.3s ease;
            }

            .login-box:hover {
                transform: translateY(-5px);
            }

            /* Título */
            .login-box h2 {
                font-weight: bold;
                color: #333333;
                margin-bottom: 20px;
            }

            /* Botão do Google */
            .google-btn {
                display: flex;
                align-items: center;
                justify-content: center;
                background-color: #4285f4;
                color: #ffffff;
                border: none;
                border-radius: 6px;
                padding: 12px 20px;
                font-size: 16px;
                font-weight: 500;
                cursor: pointer;
                transition: background-color 0.3s ease, box-shadow 0.3s ease;
                text-decoration: none;
            }

            .google-btn:hover {
                background-color: #3367d6;
                box-shadow: 0 4px 15px rgba(66, 133, 244, 0.4);
            }

            .google-btn img {
                margin-right: 8px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

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

        # Renderizar a interface de login
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown("<h2>Bem-vindo ao Meu DinDinz</h2>", unsafe_allow_html=True)

        st.markdown(
            f'<a class="google-btn" href="{authorization_url}">'
            f'<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/512px-Google_%22G%22_Logo.svg.png" alt="Google Logo" width="20"/>'
            f' Entrar com Google</a>',
            unsafe_allow_html=True
        )
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

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

    if 'user_info' in st.session_state:
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
        # Chamar a função de integração com o Google Sheets
        google_sheets_interface()

def google_sheets_interface():
    global sheet_name
    sheet_name = st.text_input("Nome da Planilha no Google Sheets", sheet_name)

    if st.button("Conectar ao Google Sheets"):
        try:
            data = connect_to_google_sheets(sheet_name)
            st.write("Dados da Planilha:", data)
        except FileNotFoundError as fnf_err:
            st.error(fnf_err)
        except ConnectionError as conn_err:
            st.error(conn_err)
        except RuntimeError as run_err:
            st.error(run_err)
        except Exception as e:
            st.error(f"Erro: {e}")

if __name__ == "__main__":
    st.set_page_config(page_title="Meu DinDinz", layout="wide")
    
    set_custom_css()  # Aplicar o CSS personalizado

    # Checar se o usuário já está logado
    if 'user_info' not in st.session_state:
        if google_login():
            show_main_app()
    else:
        show_main_app()