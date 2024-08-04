import streamlit as st
import pandas as pd

# Função para calcular o orçamento
def calculate_budget(transactions):
    total_revenue = transactions[transactions["Tipo"] == "Receita"]["Valor"].sum()
    total_expenses = transactions[transactions["Tipo"] == "Despesa"]["Valor"].sum()
    balance = total_revenue - total_expenses
    return total_revenue, total_expenses, balance

# Interface de usuário para visão geral do orçamento
def budget_overview(transactions):
    st.title("Meu DinDinz - Visão Geral do Orçamento")
    
    total_revenue, total_expenses, balance = calculate_budget(transactions)
    
    st.write("### Orçamento Mensal")
    st.write(f"Receitas Totais: R$ {total_revenue:.2f}")
    st.write(f"Despesas Totais: R$ {total_expenses:.2f}")
    st.write(f"Saldo: R$ {balance:.2f}")
    
    # Gráficos
    st.bar_chart(transactions.groupby("Categoria")["Valor"].sum())

if __name__ == "__main__":
    transactions = pd.DataFrame([
        {"Tipo": "Receita", "Categoria": "Salário", "Descrição": "Salário de Agosto", "Valor": 5000, "Data": "2024-08-01"},
        {"Tipo": "Despesa", "Categoria": "Alimentação", "Descrição": "Supermercado", "Valor": 300, "Data": "2024-08-02"},
    ])
    budget_overview(transactions)
