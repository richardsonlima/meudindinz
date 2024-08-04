import streamlit as st

# Interface de usuário para segurança e privacidade
def security_interface():
    st.title("Meu DinDinz - Segurança e Privacidade")
    
    st.write("### Autenticação")
    st.write("A aplicação utiliza autenticação OAuth para garantir a segurança das informações financeiras.")
    
    st.write("### Privacidade")
    st.write("Os dados são armazenados de forma segura e somente acessíveis pelo usuário autenticado.")

if __name__ == "__main__":
    security_interface()
