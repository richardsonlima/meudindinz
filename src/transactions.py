# src/transactions.py

import streamlit as st
from src.database import get_data, update_data

def transaction_manager(user):
    st.header("Gerenciar Transações")

    # Carregar dados das transações
    data = get_data("transacoes")

    # Formulário para adicionar transações
    with st.form(key="transaction_form"):
        date = st.date_input("Data")
        category = st.selectbox("Categoria", ["Receita", "Despesa"])
        description = st.text_input("Descrição")
        amount = st.number_input("Valor", min_value=0.0, format="%.2f")
        submit_button = st.form_submit_button("Adicionar")

    # Adicionar transação
    if submit_button:
        new_transaction = {
            "Data": date,
            "Categoria": category,
            "Descrição": description,
            "Valor": amount
        }
        data = data.append(new_transaction, ignore_index=True)
        update_data("transacoes", data)
        st.success("Transação adicionada com sucesso!")

    # Exibir transações
    st.dataframe(data)

    # Opções de edição e exclusão
    if st.button("Editar Transação"):
        st.write("Funcionalidade de edição em desenvolvimento...")

    if st.button("Excluir Transação"):
        st.write("Funcionalidade de exclusão em desenvolvimento...")