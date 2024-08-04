import os
import json
import streamlit as st
from google_sheets import connect_to_google_sheets, save_data_to_sheet
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Definir o nome da planilha do Google Sheets
SHEET_NAME = "meu_dindinz_planilha"  # nome real da planilha

# Função para cadastrar transações
def add_transaction(transaction_type, category, description, amount, date):
    # Retorna a transação formatada como lista para ser salva na planilha
    return [date.strftime("%Y-%m-%d"), transaction_type, category, description, amount]

# Interface de usuário para cadastro de transações
def transaction_interface():
    st.title("Meu DinDinz - Cadastro de Transações")
    
    transaction_type = st.selectbox("Tipo de Transação", ["Receita", "Despesa"])
    category = st.selectbox("Categoria", ["Salário", "Investimento", "Alimentação", "Transporte", "Lazer", "Outros"])
    description = st.text_input("Descrição")
    amount = st.number_input("Valor", min_value=0.0, format="%.2f")
    date = st.date_input("Data")
    
    if st.button("Adicionar Transação"):
        transaction = add_transaction(transaction_type, category, description, amount, date)
        
        # Conectar à planilha do Google Sheets
        try:
            data = connect_to_google_sheets(SHEET_NAME)  # Use a constante SHEET_NAME
            st.info("Conectado à planilha com sucesso!")
            
            # Salvar a transação na planilha do Google Sheets
            updated_data = data + [dict(zip(["Data", "Tipo", "Categoria", "Descrição", "Valor"], transaction))]
            if save_data_to_sheet(SHEET_NAME, updated_data):  # Certifique-se de passar os dados como uma lista de listas
                st.success("Transação adicionada e salva na planilha com sucesso!")
        except Exception as e:
            st.error(f"Erro ao acessar a planilha: {e}")

if __name__ == "__main__":
    transaction_interface()