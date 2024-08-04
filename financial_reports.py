import streamlit as st
import pandas as pd

# Função para gerar relatório financeiro
def generate_report(transactions, period):
    if period == "Mensal":
        report = transactions.groupby(transactions["Data"].str[:7]).sum()
    elif period == "Trimestral":
        transactions["Trimestre"] = pd.to_datetime(transactions["Data"]).dt.to_period("Q")
        report = transactions.groupby("Trimestre").sum()
    else:
        transactions["Ano"] = pd.to_datetime(transactions["Data"]).dt.year
        report = transactions.groupby("Ano").sum()
    return report

# Interface de usuário para relatórios financeiros
def financial_reports(transactions):
    st.title("Meu DinDinz - Relatórios Financeiros")
    
    period = st.selectbox("Período do Relatório", ["Mensal", "Trimestral", "Anual"])
    
    report = generate_report(transactions, period)
    
    st.write(f"### Relatório Financeiro - {period}")
    st.dataframe(report)

if __name__ == "__main__":
    transactions = pd.DataFrame([
        {"Tipo": "Receita", "Categoria": "Salário", "Descrição": "Salário de Agosto", "Valor": 5000, "Data": "2024-08-01"},
        {"Tipo": "Despesa", "Categoria": "Alimentação", "Descrição": "Supermercado", "Valor": 300, "Data": "2024-08-02"},
    ])
    financial_reports(transactions)
