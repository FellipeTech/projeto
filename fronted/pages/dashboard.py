"""
pages/3_Dashboard.py — Painel do usuário
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import (css_global, render_sidebar_nav, requer_login,
                   api_get, api_post, ACCENT, ACCENT2, CARD, BORDER, TEXT, MUTED, PLANOS_INFO)

st.set_page_config(page_title="Dashboard — DevStudio", page_icon="📊", layout="wide")
css_global()
requer_login()
render_sidebar_nav()

# ─────────────────────────────────────────
# Carrega dados atualizados do usuário
# ─────────────────────────────────────────
user = api_get(f"/usuario/{st.session_state['user']}")
if user:
    st.session_state["ativo"] = user.get("ativo", False)
    st.session_state["plano"] = user.get("plano")
    st.session_state["nome"]  = user.get("nome", "")

nome  = st.session_state.get("nome") or st.session_state["user"]
ativo = st.session_state.get("ativo", False)
plano = st.session_state.get("plano")

# ─────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────
st.markdown(f"""
<div style="padding:8px 0 32px;">
    <h1 style="font-family:'Syne',sans-serif;font-weight:800;font-size:34px;color:{TEXT};margin-bottom:4px;">
        Olá, {nome.split()[0] if nome else 'visitante'} 👋
    </h1>
    <p style="color:{MUTED};font-size:15px;">Bem-vindo ao seu painel DevStudio</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# STATUS + PLANO
# ─────────────────────────────────────────
c1, c2, c3 = st.columns(3)

with c1:
    status_color = "#00C875" if ativo else ACCENT2
    status_label = "Conta Ativa ✅" if ativo else "Pagamento Pendente"
    st.markdown(f"""
    <div class="metric-box">
        <div class="label">Status da conta</div>
        <div style="font-family:'Syne',sans-serif;font-size:18px;font-weight:700;color:{status_color};margin-top:4px;">
            {status_label}
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    plano_info = PLANOS_INFO.get(plano, {}) if plano else {}
    plano_nome = plano_info.get("nome", "Nenhum") if plano_info else "Nenhum"
    plano_cor  = plano_info.get("cor", MUTED) if plano_info else MUTED
    st.markdown(f"""
    <div class="metric-box">
        <div class="label">Plano atual</div>
        <div style="font-family:'Syne',sans-serif;font-size:18px;font-weight:700;color:{plano_cor};margin-top:4px;">
            {plano_nome}
        </div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    qtd_sites = len(user.get("sites", []))
    st.markdown(f"""
    <div class="metric-box">
        <div class="label">Sites contratados</div>
        <div class="value">{qtd_sites}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────
# AVISO SE INATIVO
# ─────────────────────────────────────────
if not ativo:
    st.warning("⚠️ Sua conta ainda não está ativa. Acesse **Pagamento** para contratar um plano.")
    st.page_link("pages/5_Pagamento.py", label="→ Ir para Pagamento")

# ─────────────────────────────────────────
# SITES RECENTES
# ─────────────────────────────────────────
sites = user.get("sites", [])

st.markdown(f'<h3 style="font-family:Syne,sans-serif;font-weight:700;margin-bottom:16px;">🌐 Seus sites</h3>', unsafe_allow_html=True)

if not sites:
    st.markdown(f"""
    <div class="card" style="text-align:center;padding:40px;">
        <div style="font-size:32px;margin-bottom:12px;">🚀</div>
        <div style="font-family:'Syne',sans-serif;font-weight:700;color:{TEXT};margin-bottom:8px;">
            Nenhum site ainda
        </div>
        <div style="color:{MUTED};font-size:14px;">
            Escolha um plano e comece seu projeto hoje.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/4_Planos.py", label="→ Ver planos disponíveis")
else:
    for site in sites:
        st.markdown(f"""
        <div class="card" style="display:flex;align-items:center;gap:16px;">
            <div style="font-size:24px;">🌐</div>
            <div>
                <div style="font-family:'Syne',sans-serif;font-weight:700;color:{TEXT};font-size:15px;">{site}</div>
                <div style="font-size:12px;color:{MUTED};margin-top:2px;">Contate-nos via WhatsApp para acompanhar o progresso</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ─────────────────────────────────────────
# AÇÕES RÁPIDAS
# ─────────────────────────────────────────
st.markdown(f'<h3 style="font-family:Syne,sans-serif;font-weight:700;margin-bottom:16px;">⚡ Ações rápidas</h3>', unsafe_allow_html=True)

ca, cb, cc = st.columns(3)
with ca:
    st.page_link("pages/4_Planos.py",     label="📋 Ver planos")
with cb:
    st.page_link("pages/5_Pagamento.py",  label="💳 Ir para pagamento")
with cc:
    st.page_link("pages/6_Configuracoes.py", label="⚙️ Configurar perfil")