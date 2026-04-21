"""
pages/7_Meus_Sites.py — Sites do usuário
"""

import streamlit as st
import urllib.parse
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import (css_global, render_sidebar_nav, requer_login,
                   api_get, ACCENT, ACCENT2, CARD, BORDER, TEXT, MUTED, PLANOS_INFO)

st.set_page_config(page_title="Meus Sites — DevStudio", page_icon="🌐", layout="wide")
css_global()
requer_login()
render_sidebar_nav()

WHATSAPP = "5573999946196"
def wa(msg): return f"https://wa.me/{WHATSAPP}?text={urllib.parse.quote(msg)}"

st.markdown(f"""
<div style="padding:8px 0 32px;">
    <h1 style="font-family:'Syne',sans-serif;font-weight:800;font-size:32px;color:{TEXT};">
        🌐 Meus Sites
    </h1>
    <p style="color:{MUTED};">Acompanhe os projetos vinculados à sua conta</p>
</div>
""", unsafe_allow_html=True)

user = api_get(f"/usuario/{st.session_state['user']}")
sites = user.get("sites", [])
plano = user.get("plano")
ativo = user.get("ativo", False)

# ─────────────────────────────────────────
# STATUS DO PLANO
# ─────────────────────────────────────────
if plano:
    info = PLANOS_INFO.get(plano, {})
    st.markdown(f"""
    <div class="card" style="border-left:3px solid {info.get('cor', ACCENT)};margin-bottom:24px;">
        <span style="font-family:'Syne',sans-serif;font-weight:700;color:{TEXT};">
            {info.get('emoji','')} Plano {info.get('nome','')}
        </span>
        &nbsp; &nbsp;
        {'<span class="badge badge-ativo">Ativo</span>' if ativo else '<span class="badge badge-inativo">Aguardando pagamento</span>'}
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# LISTA DE SITES
# ─────────────────────────────────────────
if not sites:
    st.markdown(f"""
    <div class="card" style="text-align:center;padding:60px 40px;">
        <div style="font-size:48px;margin-bottom:16px;">🚀</div>
        <h3 style="font-family:'Syne',sans-serif;font-weight:800;color:{TEXT};margin-bottom:12px;">
            Nenhum site ainda
        </h3>
        <p style="color:{MUTED};font-size:15px;max-width:380px;margin:0 auto 24px;">
            Escolha um plano, faça o pagamento e seu projeto será iniciado em breve.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.page_link("pages/4_Planos.py",    label="📋 Ver planos")
    with c2:
        st.page_link("pages/5_Pagamento.py", label="💳 Ir para pagamento")

else:
    for i, site in enumerate(sites, 1):
        c_info, c_wa = st.columns([4, 1])

        with c_info:
            st.markdown(f"""
            <div class="card">
                <div style="display:flex;align-items:flex-start;gap:16px;">
                    <div style="background:{ACCENT}22;border:1px solid {ACCENT}44;border-radius:10px;
                                width:44px;height:44px;display:flex;align-items:center;justify-content:center;
                                font-size:20px;flex-shrink:0;">🌐</div>
                    <div style="flex:1;">
                        <div style="font-family:'Syne',sans-serif;font-weight:700;color:{TEXT};font-size:16px;margin-bottom:4px;">
                            {site}
                        </div>
                        <div style="font-size:12px;color:{MUTED};">
                            Projeto #{i} · Entre em contato para acompanhar o andamento
                        </div>
                        <div style="margin-top:10px;">
                            <span class="badge badge-ativo">Em desenvolvimento</span>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with c_wa:
            st.markdown(f"""
            <div style="padding-top:20px;">
                <a href="{wa(f'Olá! Quero acompanhar o andamento do meu site: {site}')}" target="_blank" style="
                    display:block;text-align:center;
                    background:#25D36622;color:#25D366;
                    border:1px solid #25D36644;
                    font-family:'Syne',sans-serif;font-weight:700;font-size:13px;
                    padding:12px 16px;border-radius:10px;text-decoration:none;
                ">💬 Acompanhar no WhatsApp</a>
            </div>
            """, unsafe_allow_html=True)

st.divider()

# Dicas
st.markdown(f"""
<div class="card" style="background:#050810;">
    <div style="font-family:'Syne',sans-serif;font-weight:700;color:{ACCENT};font-size:14px;margin-bottom:12px;">
        💡 Como funciona o processo?
    </div>
    <div style="color:{MUTED};font-size:13px;line-height:1.9;">
        1. Você escolhe um plano e efetua o pagamento<br>
        2. Entramos em contato via WhatsApp para coletar informações do projeto<br>
        3. Apresentamos o design para aprovação<br>
        4. Desenvolvemos e entregamos no prazo combinado<br>
        5. Você recebe as credenciais de acesso ao site
    </div>
</div>
""", unsafe_allow_html=True)