"""
pages/2_Cadastro.py — Criar conta
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import css_global, render_sidebar_nav, api_post, ACCENT, CARD, BORDER, TEXT, MUTED

st.set_page_config(page_title="Cadastro — DevStudio", page_icon="✨", layout="centered")
css_global()

if "user" in st.session_state:
    st.switch_page("pages/3_Dashboard.py")

render_sidebar_nav()

# ─────────────────────────────────────────
# FORMULÁRIO
# ─────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center; padding:40px 0 32px;">
    <div style="font-size:40px; margin-bottom:12px;">✨</div>
    <h1 style="font-family:'Syne',sans-serif;font-weight:800;font-size:32px;color:{TEXT};margin-bottom:8px;">
        Criar sua conta
    </h1>
    <p style="color:{MUTED};font-size:15px;">Acesse o painel e acompanhe seu projeto</p>
</div>
""", unsafe_allow_html=True)

nome     = st.text_input("Nome completo", placeholder="João da Silva")
email    = st.text_input("Email", placeholder="seu@email.com")
telefone = st.text_input("WhatsApp (opcional)", placeholder="(73) 99999-9999")
senha    = st.text_input("Senha", type="password", placeholder="Mínimo 6 caracteres")
senha2   = st.text_input("Confirmar senha", type="password", placeholder="Repita a senha")

col_btn, col_link = st.columns([2, 1])
with col_btn:
    cadastrar = st.button("Criar conta", use_container_width=True)
with col_link:
    st.page_link("pages/1_Login.py", label="Já tenho conta →")

if cadastrar:
    if not email or not senha:
        st.error("Email e senha são obrigatórios.")
    elif len(senha) < 6:
        st.error("A senha deve ter pelo menos 6 caracteres.")
    elif senha != senha2:
        st.error("As senhas não coincidem.")
    else:
        with st.spinner("Criando conta..."):
            r = api_post("/register", {
                "email": email.strip().lower(),
                "senha": senha,
                "nome": nome.strip(),
                "telefone": telefone.strip(),
            })

        if "erro" in r:
            st.error(f"❌ {r['erro']}")
        else:
            st.success("✅ Conta criada com sucesso!")
            st.info("Agora faça login para acessar o painel.")
            st.page_link("pages/1_Login.py", label="→ Ir para o Login")
