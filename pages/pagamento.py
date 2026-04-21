import streamlit as st
import requests
import time

API = "http://localhost:8000"

st.set_page_config(page_title="Área de Membros")

# =========================
# MENU
# =========================
menu = st.sidebar.selectbox("Menu", ["Login", "Cadastro"])

# =========================
# CADASTRO
# =========================
if menu == "Cadastro":
    st.title("Criar conta")

    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")

    if st.button("Cadastrar"):
        r = requests.post(f"{API}/register", json={
            "email": email,
            "senha": senha
        }).json()

        st.write(r)

# =========================
# LOGIN
# =========================
if menu == "Login":
    st.title("Login")

    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        r = requests.post(f"{API}/login", json={
            "email": email,
            "senha": senha
        }).json()

        if "erro" in r:
            st.error("Login inválido")
        else:
            st.session_state["user"] = email
            st.session_state["ativo"] = r["ativo"]

# =========================
# ÁREA LOGADA
# =========================
if "user" in st.session_state:

    st.sidebar.success(f"Logado: {st.session_state['user']}")

    if st.session_state["ativo"]:
        st.success("🎉 Acesso liberado!")

        st.write("Conteúdo exclusivo aqui 🔒")

    else:
        st.warning("Você precisa pagar para liberar acesso")

        planos = {
            "Básico": 500,
            "Premium": 1000
        }

        plano = st.selectbox("Plano", list(planos.keys()))
        valor = planos[plano]

        if st.button("Gerar Pix"):
            r = requests.post(f"{API}/gerar_pix", json={
                "email": st.session_state["user"],
                "valor": valor
            }).json()

            st.session_state["txid"] = r["txid"]
            st.code(r["pix"])

        # verificar pagamento
        if "txid" in st.session_state:

            status = requests.get(
                f"{API}/status/{st.session_state['txid']}"
            ).json()

            if status.get("status") == "PAGO":
                st.success("Pagamento confirmado!")
                st.session_state["ativo"] = True
                st.rerun()
            else:
                st.warning("Aguardando pagamento...")
                time.sleep(5)
                st.rerun()