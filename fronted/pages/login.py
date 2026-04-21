"""
pages/1_Login.py — Página de Login
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import css_global, render_sidebar_nav, api_post, ACCENT, CARD, BORDER, TEXT, MUTED, BG

st.set_page_config(page_title="Login — DevStudio", page_icon="🔑", layout="centered")
css_global()

# Redireciona se já logado
if "user" in st.session_state:
    st.switch_page("pages/3_Dashboard.py")

render_sidebar_nav()

# ─────────────────────────────────────────
# FORMULÁRIO
# ─────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center; padding:40px 0 32px;">
    <div style="font-size:40px; margin-bottom:12px;">🔑</div>
    <h1 style="font-family:'Syne',sans-serif;font-weight:800;font-size:32px;color:{TEXT};margin-bottom:8px;">
        Bem-vindo de volta
    </h1>
    <p style="color:{MUTED};font-size:15px;">Entre na sua conta para acessar o painel</p>
</div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown(f'<div class="card" style="max-width:420px;margin:0 auto;">', unsafe_allow_html=True)

    email = st.text_input("Email", placeholder="seu@email.com")
    senha = st.text_input("Senha", type="password", placeholder="••••••••")

    col_btn, col_link = st.columns([2, 1])
    with col_btn:
        entrar = st.button("Entrar", use_container_width=True)
    with col_link:
        st.page_link("pages/2_Cadastro.py", label="Criar conta →")

    st.markdown("</div>", unsafe_allow_html=True)

if entrar:
    if not email or not senha:
        st.error("Preencha todos os campos.")
    else:
        with st.spinner("Verificando..."):
            r = api_post("/login", {"email": email.strip().lower(), "senha": senha})

        if "erro" in r:
            st.error(f"❌ {r['erro']}")
        else:
            st.session_state["user"]  = r["email"]
            st.session_state["nome"]  = r.get("nome", "")
            st.session_state["ativo"] = r["ativo"]
            st.session_state["admin"] = r["admin"]
            st.session_state["plano"] = r.get("plano")
            st.success("✅ Login realizado! Redirecionando...")
            st.switch_page("pages/3_Dashboard.py")