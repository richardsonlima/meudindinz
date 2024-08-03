# src/app.py
import sys
import os

# Adiciona o diretório pai ao caminho do sistema
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from src.authentication import authenticate_user
from src.transactions import transaction_manager
from src.budget_overview import budget_overview
from src.financial_reports import generate_financial_reports
from src.financial_goals import manage_financial_goals
from src.notifications import notification_settings

def main():
    st.set_page_config(page_title="Meu DinDinz", page_icon="💰", layout="centered")
    
    # Aplicar CSS customizado
    with open("src/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Tela de login
    st.image("assets/images/logo.png", width=150)
    
    st.markdown("<h2 class='login-header'>CREATE ACCOUNT</h2>", unsafe_allow_html=True)
    st.markdown("<p class='login-subheader'>Save your financial data and manage your account on different devices</p>", unsafe_allow_html=True)

    # Autenticação do usuário
    user_info = authenticate_user()

    if user_info:
        st.success("Login bem-sucedido!")
        st.write("Você pode agora acessar o conteúdo protegido.")
    else:
        st.write("Faça login para continuar.")

    if 'user_info' in st.session_state and st.session_state['user_info'] is not None:
        st.success(f"Bem-vindo de volta, {st.session_state['user_info']['name']}!")

if __name__ == "__main__":
    main()