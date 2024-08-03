# src/financial_goals.py

import streamlit as st
from src.database import get_data, update_data

def manage_financial_goals(user):
    st.header("Metas Financeiras")

    # Carregar dados das metas
    data = get_data("metas")

    # Formulário para adicionar metas
    with st.form(key="goal_form"):
        goal_name = st.text_input("Nome da Meta")
        target_amount = st.number_input("Valor Alvo", min_value=0.0, format="%.2f")
        current_amount = st.number_input("Valor Atual", min_value=0.0, format="%.2f")
        submit_button = st.form_submit_button("Adicionar Meta")

    # Adicionar meta
    if submit_button:
        new_goal = {
            "Nome": goal_name,
            "Valor Alvo": target_amount,
            "Valor Atual": current_amount
        }
        data = data.append(new_goal, ignore_index=True)
        update_data("metas", data)
        st.success("Meta adicionada com sucesso!")

    # Exibir metas
    st.dataframe(data)

    # Progresso das metas
    st.subheader("Progresso das Metas")
    for index, row in data.iterrows():
        st.write(f"{row['Nome']}: {row['Valor Atual']} de {row['Valor Alvo']}")
        st.progress(row['Valor Atual'] / row['Valor Alvo'])