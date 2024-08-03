# src/budget_overview.py

import streamlit as st
import pandas as pd

def budget_overview(user):
    st.header("Visão Geral do Orçamento")

    # Simular dados para demonstração
    data = {
        "Receitas": [5000, 6000, 5500],
        "Despesas": [3000, 3200, 3100],
        "Mês": ["Janeiro", "Fevereiro", "Março"]
    }

    df = pd.DataFrame(data)
    df["Saldo"] = df["Receitas"] - df["Despesas"]

    st.subheader("Resumo Mensal")
    st.dataframe(df)

    # Gráfico de barras
    st.subheader("Gráfico de Receitas e Despesas")
    st.bar_chart(df.set_index("Mês")[["Receitas", "Despesas"]])

    st.subheader("Gráfico de Saldo")
    st.line_chart(df.set_index("Mês")["Saldo"])