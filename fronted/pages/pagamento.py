"""
pages/5_Pagamento.py — Pagamento via Pix
"""

import streamlit as st
import time
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import (css_global, render_sidebar_nav, requer_login,
                   api_get, api_post, ACCENT, ACCENT2, CARD, BORDER, TEXT, MUTED, PLANOS_INFO)

st.set_page_config(page_title="Pagamento — DevStudio", page_icon="💳", layout="centered")
css_global()
requer_login()
render_sidebar_nav()

# ─────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center;padding:32px 0 24px;">
    <div style="font-size:36px;margin-bottom:10px;">💳</div>
    <h1 style="font-family:'Syne',sans-serif;font-weight:800;font-size:30px;color:{TEXT};margin-bottom:8px;">
        Pagamento via Pix
    </h1>
    <p style="color:{MUTED};font-size:14px;">Confirmação automática em segundos</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# SELEÇÃO DE PLANO
# ─────────────────────────────────────────
plano_pre = st.session_state.get("plano_selecionado")

plano_opcoes = {
    "⚡ Básico — R$ 500":        "basico",
    "🚀 Profissional — R$ 1.000": "profissional",
    "🔥 Premium — R$ 2.000":     "premium",
}

default_idx = 0
if plano_pre:
    labels = list(plano_opcoes.keys())
    valores = list(plano_opcoes.values())
    if plano_pre in valores:
        default_idx = valores.index(plano_pre)

plano_label = st.selectbox("Selecione o plano", list(plano_opcoes.keys()), index=default_idx)
plano_key   = plano_opcoes[plano_label]
plano_info  = PLANOS_INFO[plano_key]

# Resumo do plano
st.markdown(f"""
<div class="card" style="border-left:3px solid {plano_info['cor']};margin:12px 0 24px;">
    <div style="display:flex;justify-content:space-between;align-items:center;">
        <div>
            <div style="font-family:'Syne',sans-serif;font-weight:700;color:{TEXT};font-size:16px;">
                {plano_info['emoji']} Plano {plano_info['nome']}
            </div>
            <div style="color:{MUTED};font-size:13px;margin-top:4px;">Pagamento único · Sem mensalidade</div>
        </div>
        <div style="font-family:'Syne',sans-serif;font-weight:800;font-size:26px;color:{plano_info['cor']};">
            R$ {plano_info['valor']:,}
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# GERAR PIX
# ─────────────────────────────────────────
if "txid" not in st.session_state or st.session_state.get("txid_plano") != plano_key:
    if st.button("Gerar código Pix", use_container_width=True):
        with st.spinner("Gerando Pix..."):
            r = api_post("/gerar_pix", {
                "email": st.session_state["user"],
                "plano": plano_key,
            })

        if "erro" in r:
            st.error(r["erro"])
        else:
            st.session_state["txid"]       = r["txid"]
            st.session_state["txid_plano"] = plano_key
            st.rerun()

# ─────────────────────────────────────────
# AGUARDANDO PAGAMENTO
# ─────────────────────────────────────────
if "txid" in st.session_state and st.session_state.get("txid_plano") == plano_key:
    txid = st.session_state["txid"]

    status_data = api_get(f"/status/{txid}")
    status      = status_data.get("status", "PENDENTE")

    if status == "PAGO":
        st.balloons()
        st.success("✅ Pagamento confirmado! Bem-vindo ao DevStudio.")
        st.session_state["ativo"] = True
        st.session_state["plano"] = plano_key
        st.session_state.pop("txid", None)
        st.session_state.pop("txid_plano", None)
        st.page_link("pages/3_Dashboard.py", label="→ Ir ao Dashboard")

    else:
        # Exibe código Pix
        pix_code = status_data.get("pix") or ""

        st.markdown(f"""
        <div class="card" style="text-align:center;">
            <div style="font-size:11px;color:{MUTED};text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;">
                Código Pix Copia e Cola
            </div>
            <div style="
                background:#050810;border:1px solid {BORDER};border-radius:8px;
                padding:14px 16px;font-family:monospace;font-size:11px;
                color:{ACCENT};word-break:break-all;line-height:1.6;
                margin-bottom:16px;
            ">{pix_code or 'Aguardando geração...'}</div>
            <div style="font-size:12px;color:{MUTED};">
                Abra o app do seu banco → Pix → Copia e Cola → cole o código acima
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.warning("⏳ Aguardando confirmação do pagamento...")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔄 Verificar pagamento"):
                st.rerun()
        with c2:
            if st.button("❌ Cancelar e trocar plano"):
                st.session_state.pop("txid", None)
                st.session_state.pop("txid_plano", None)
                st.rerun()

        # Auto-refresh a cada 8s
        with st.spinner("Verificando automaticamente em instantes..."):
            time.sleep(8)
        st.rerun()

st.divider()

# ─────────────────────────────────────────
# MODO TESTE (apenas em dev)
# ─────────────────────────────────────────
with st.expander("🧪 Simular pagamento (modo teste)"):
    st.warning("Remova este bloco em produção!")
    if "txid" in st.session_state:
        if st.button("✅ Simular Pix Pago"):
            r = api_post("/dev/simular_pago", {"txid": st.session_state["txid"]})
            st.success(r.get("msg", "Simulado!"))
            st.rerun()
    else:
        st.info("Gere um Pix primeiro para poder simular.")
