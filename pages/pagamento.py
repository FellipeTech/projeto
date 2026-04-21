import streamlit as st
import requests
import time

API = "http://localhost:8000"

st.set_page_config(page_title="Área de Membros")

# =========================
# MENU
# =========================
if "user" not in st.session_state:
    menu = st.sidebar.selectbox("Menu", ["Login", "Cadastro"])
else:
    menu = st.sidebar.selectbox(
        "Menu",
        ["Dashboard", "Configurações", "Meus Sites", "Pagamento", "Sair"]
    )

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

        if "erro" in r:
            st.error(r["erro"])
        else:
            st.success("Conta criada!")

# =========================
# LOGIN
# =========================
if menu == "Login":
    st.title("Entrar")

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
# DASHBOARD
# =========================
if menu == "Dashboard" and "user" in st.session_state:
    st.title("Dashboard")

    user = requests.get(f"{API}/usuario/{st.session_state['user']}").json()

    if user.get("ativo"):
        st.success("Conta ativa ✅")
    else:
        st.warning("Conta não ativa")

# =========================
# CONFIGURAÇÕES
# =========================
if menu == "Configurações":
    st.title("Configurar conta")

    nome = st.text_input("Nome")
    telefone = st.text_input("Telefone")

    if st.button("Salvar"):
        requests.post(f"{API}/configurar", json={
            "email": st.session_state["user"],
            "nome": nome,
            "telefone": telefone
        })

        st.success("Atualizado!")

# =========================
# MEUS SITES
# =========================
if menu == "Meus Sites":
    st.title("Meus Sites")

    user = requests.get(f"{API}/usuario/{st.session_state['user']}").json()

    sites = user.get("sites", [])

    if not sites:
        st.warning("Você não tem sites ainda")
    else:
        for site in sites:
            st.success(site)

# =========================
# PAGAMENTO
# =========================
if menu == "Pagamento":
    st.title("Pagamento")

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

# =========================
# SAIR
# =========================
if menu == "Sair":
    st.session_state.clear()
    st.rerun()