import os
import json
import streamlit as st
from google_sheets import connect_to_google_sheets, save_data_to_sheet  # Importando as funções corretamente
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

def transaction_interface():
    st.title("Interface de Transações")

    # Nome da planilha
    sheet_name = st.text_input("Nome da Planilha no Google Sheets", "Nome da Planilha")

    if st.button("Carregar Transações"):
        try:
            data = connect_to_google_sheets(sheet_name)
            st.write("Transações Carregadas:", data)
        except Exception as e:
            st.error(f"Erro ao carregar transações: {e}")

    # Exemplo de dados de transações
    new_transaction_data = [
        {"Data": "2024-08-01", "Descrição": "Compra", "Valor": 100.0, "Categoria": "Compras"},
        {"Data": "2024-08-02", "Descrição": "Venda", "Valor": 200.0, "Categoria": "Vendas"},
    ]

    if st.button("Salvar Novas Transações"):
        try:
            success = save_data_to_sheet(sheet_name, new_transaction_data)
            if success:
                st.success("Transações salvas com sucesso!")
        except Exception as e:
            st.error(f"Erro ao salvar transações: {e}")
