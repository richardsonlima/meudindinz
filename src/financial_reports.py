# src/financial_reports.py

import streamlit as st
from src.database import get_data

def generate_financial_reports(user):
    st.header("Relatórios Financeiros")

    # Carregar dados
    data = get_data("transacoes")

    # Analisar categorias mais comuns
    common_categories = data['Categoria'].value_counts()

    st.subheader("Categorias de Despesas Mais Comuns")
    st.bar_chart(common_categories)

    # Comparação de despesas ao longo dos meses
    monthly_expenses = data.groupby(data['Data'].dt.month)['Valor'].sum()
    st.subheader("Despesas Mensais")
    st.line_chart(monthly_expenses)