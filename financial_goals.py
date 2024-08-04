import streamlit as st
import pandas as pd

# Função para definir metas financeiras
def set_financial_goal(goal_name, goal_amount, current_savings):
    return {
        "Meta": goal_name,
        "Objetivo": goal_amount,
        "Poupança Atual": current_savings,
        "Progresso": (current_savings / goal_amount) * 100
    }

# Interface de usuário para metas financeiras
def financial_goals_interface():
    st.title("Meu DinDinz - Metas Financeiras")
    
    goal_name = st.text_input("Nome da Meta")
    goal_amount = st.number_input("Valor da Meta", min_value=0.0, format="%.2f")
    current_savings = st.number_input("Poupança Atual", min_value=0.0, format="%.2f")
    
    if st.button("Definir Meta"):
        goal = set_financial_goal(goal_name, goal_amount, current_savings)
        st.success("Meta financeira definida com sucesso!")
        st.write(goal)

if __name__ == "__main__":
    financial_goals_interface()
