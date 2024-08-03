# src/notifications.py

import streamlit as st

def notification_settings(user):
    st.header("Configurações de Notificações")

    # Configurações de notificação
    email_notifications = st.checkbox("Notificações por Email", value=True)
    sms_notifications = st.checkbox("Notificações por SMS", value=False)

    if st.button("Salvar Configurações"):
        st.success("Configurações salvas com sucesso!")

    # Simular envio de notificação
    st.subheader("Enviar Notificação")
    if st.button("Enviar"):
        st.info("Notificação enviada com sucesso!")