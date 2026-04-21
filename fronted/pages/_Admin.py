"""
pages/8_Admin.py — Painel Administrativo
Acesso restrito: admin@email.com
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import (css_global, render_sidebar_nav, requer_admin,
                   api_get, api_post, ACCENT, ACCENT2, CARD, BORDER, TEXT, MUTED, PLANOS_INFO)

st.set_page_config(page_title="Admin — DevStudio", page_icon="🛡️", layout="wide")
css_global()
requer_admin()
render_sidebar_nav()

st.markdown(f"""
<div style="padding:8px 0 32px;">
    <div style="font-family:'Syne',sans-serif;font-size:11px;font-weight:700;
                text-transform:uppercase;letter-spacing:0.12em;color:{ACCENT2};
                background:{ACCENT2}15;border:1px solid {ACCENT2}33;
                border-radius:20px;display:inline-block;padding:4px 12px;margin-bottom:16px;">
        🛡️ Área restrita
    </div>
    <h1 style="font-family:'Syne',sans-serif;font-weight:800;font-size:32px;color:{TEXT};">
        Painel Administrativo
    </h1>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# TABS
# ─────────────────────────────────────────
tab_users, tab_pags = st.tabs(["👥 Usuários", "💰 Pagamentos"])

# ─────────────────────────────────────────
# ABA USUÁRIOS
# ─────────────────────────────────────────
with tab_users:
    usuarios = api_get("/admin/usuarios")

    if not usuarios:
        st.info("Nenhum usuário cadastrado.")
    else:
        # Métricas
        total    = len(usuarios)
        ativos   = sum(1 for u in usuarios.values() if u.get("ativo"))
        inativos = total - ativos

        m1, m2, m3 = st.columns(3)
        m1.markdown(f'<div class="metric-box"><div class="label">Total de usuários</div><div class="value">{total}</div></div>', unsafe_allow_html=True)
        m2.markdown(f'<div class="metric-box"><div class="label">Contas ativas</div><div style="font-family:Syne,sans-serif;font-size:28px;font-weight:800;color:#00C875;">{ativos}</div></div>', unsafe_allow_html=True)
        m3.markdown(f'<div class="metric-box"><div class="label">Aguardando pagamento</div><div style="font-family:Syne,sans-serif;font-size:28px;font-weight:800;color:{ACCENT2};">{inativos}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Filtro
        filtro = st.selectbox("Filtrar por status", ["Todos", "Ativos", "Inativos"])

        for email, dados in usuarios.items():
            ativo = dados.get("ativo", False)

            if filtro == "Ativos" and not ativo:
                continue
            if filtro == "Inativos" and ativo:
                continue

            plano_key  = dados.get("plano")
            plano_info = PLANOS_INFO.get(plano_key, {}) if plano_key else {}
            status_badge = '<span class="badge badge-ativo">Ativo</span>' if ativo else '<span class="badge badge-inativo">Inativo</span>'
            plano_badge  = f'<span class="badge badge-plano">{plano_info.get("nome","—")}</span>' if plano_key else ""

            with st.container():
                col_info, col_acoes = st.columns([3, 1])

                with col_info:
                    st.markdown(f"""
                    <div class="card" style="margin-bottom:0;">
                        <div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap;">
                            <div>
                                <div style="font-family:'Syne',sans-serif;font-weight:700;color:{TEXT};font-size:15px;">
                                    {dados.get('nome') or '—'}
                                </div>
                                <div style="font-size:13px;color:{MUTED};margin:2px 0 8px;">{email}</div>
                                <div style="display:flex;gap:8px;flex-wrap:wrap;">
                                    {status_badge} {plano_badge}
                                </div>
                            </div>
                        </div>
                        <div style="font-size:12px;color:{MUTED};margin-top:10px;">
                            Sites: {len(dados.get('sites', []))} &nbsp;·&nbsp;
                            Tel: {dados.get('telefone') or '—'} &nbsp;·&nbsp;
                            Desde: {dados.get('criado_em', '—')[:10] if dados.get('criado_em') else '—'}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                with col_acoes:
                    if not ativo:
                        plano_sel = st.selectbox(
                            "Plano",
                            options=list(PLANOS_INFO.keys()),
                            format_func=lambda k: PLANOS_INFO[k]["nome"],
                            key=f"plano_{email}"
                        )
                        if st.button("✅ Ativar", key=f"ativar_{email}"):
                            r = api_post("/admin/ativar", {"email": email, "plano": plano_sel})
                            st.success(r.get("msg", "Ativado!"))
                            st.rerun()
                    else:
                        if st.button("🔒 Desativar", key=f"desativar_{email}"):
                            r = api_post("/admin/desativar", {"email": email})
                            st.warning(r.get("msg", "Desativado."))
                            st.rerun()

# ─────────────────────────────────────────
# ABA PAGAMENTOS
# ─────────────────────────────────────────
with tab_pags:
    pagamentos = api_get("/admin/pagamentos")

    if not pagamentos:
        st.info("Nenhum pagamento gerado ainda.")
    else:
        # Métricas
        pago      = sum(1 for p in pagamentos.values() if p.get("status") == "PAGO")
        pendente  = sum(1 for p in pagamentos.values() if p.get("status") == "PENDENTE")
        receita   = sum(p.get("valor", 0) for p in pagamentos.values() if p.get("status") == "PAGO")

        m1, m2, m3 = st.columns(3)
        m1.markdown(f'<div class="metric-box"><div class="label">Pagamentos confirmados</div><div style="font-family:Syne,sans-serif;font-size:28px;font-weight:800;color:#00C875;">{pago}</div></div>', unsafe_allow_html=True)
        m2.markdown(f'<div class="metric-box"><div class="label">Aguardando</div><div style="font-family:Syne,sans-serif;font-size:28px;font-weight:800;color:#FFB000;">{pendente}</div></div>', unsafe_allow_html=True)
        m3.markdown(f'<div class="metric-box"><div class="label">Receita confirmada</div><div style="font-family:Syne,sans-serif;font-size:24px;font-weight:800;color:{ACCENT};">R$ {receita:,.0f}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        for txid, pag in sorted(pagamentos.items(), key=lambda x: x[1].get("criado_em",""), reverse=True):
            status = pag.get("status")
            cor    = "#00C875" if status == "PAGO" else "#FFB000"
            plano_nome = PLANOS_INFO.get(pag.get("plano",""), {}).get("nome", pag.get("plano","—"))

            st.markdown(f"""
            <div class="card">
                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
                    <div>
                        <div style="font-family:'Syne',sans-serif;font-weight:700;color:{TEXT};font-size:14px;">
                            {pag.get('email','—')}
                        </div>
                        <div style="font-size:12px;color:{MUTED};margin-top:2px;">
                            Plano: {plano_nome} &nbsp;·&nbsp; TXID: {txid[:12]}...
                            &nbsp;·&nbsp; {pag.get('criado_em','')[:16] if pag.get('criado_em') else ''}
                        </div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-family:'Syne',sans-serif;font-weight:800;color:{cor};font-size:18px;">
                            R$ {pag.get('valor', 0):,}
                        </div>
                        <span style="
                            font-size:11px;font-weight:700;font-family:'Syne',sans-serif;
                            background:{cor}22;color:{cor};border:1px solid {cor}44;
                            border-radius:20px;padding:3px 10px;text-transform:uppercase;
                        ">{status}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
