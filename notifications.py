import streamlit as st
from datetime import date, timedelta

# Função para enviar notificações
def send_notification(message):
    st.info(message)

# Interface de usuário para notificações
def notifications_interface():
    st.title("Meu DinDinz - Notificações e Lembretes")
    
    reminder_date = st.date_input("Data de Lembrete", min_value=date.today())
    reminder_message = st.text_input("Mensagem de Lembrete")
    
    if st.button("Enviar Lembrete"):
        send_notification(f"Lembrete para {reminder_date}: {reminder_message}")
        st.success("Lembrete enviado!")

if __name__ == "__main__":
    notifications_interface()
