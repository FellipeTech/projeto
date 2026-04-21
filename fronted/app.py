import streamlit as st
import urllib.parse
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from utils import css_global, render_sidebar_nav, ACCENT, ACCENT2, CARD, BORDER, TEXT, MUTED, BG

st.set_page_config(
    page_title="DevStudio — Sites que Vendem",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

css_global()

WHATSAPP = "5573999946196"

def wa_link(msg: str) -> str:
    return f"https://wa.me/{WHATSAPP}?text={urllib.parse.quote(msg)}"

# ─────────────────────────────────────────
# HERO
# ─────────────────────────────────────────
st.markdown(f"""
<div style="
    min-height: 480px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 80px 0 60px;
    position: relative;
">
    <!-- Glow de fundo -->
    <div style="
        position: absolute; top: 0; left: 50%; transform: translateX(-50%);
        width: 700px; height: 300px;
        background: radial-gradient(ellipse, {ACCENT}18 0%, transparent 70%);
        pointer-events: none;
    "></div>

    <div style="position:relative; text-align:center;">
        <div style="
            display:inline-block;
            font-family:'Syne',sans-serif;
            font-size:11px; font-weight:700;
            text-transform:uppercase; letter-spacing:0.16em;
            color:{ACCENT}; background:{ACCENT}15;
            border:1px solid {ACCENT}33;
            border-radius:20px; padding:6px 16px;
            margin-bottom:28px;
        ">✦ Sites profissionais para negócios reais</div>

        <h1 style="
            font-family:'Syne',sans-serif;
            font-size:clamp(40px,6vw,76px);
            font-weight:800; line-height:1.08;
            letter-spacing:-0.03em;
            color:{TEXT};
            margin-bottom:24px;
        ">
            Sites que transformam<br>
            <span style="color:{ACCENT};">visitantes em clientes.</span>
        </h1>

        <p style="
            font-size:18px; color:{MUTED};
            max-width:520px; margin:0 auto 40px;
            line-height:1.7;
        ">
            Design moderno, entrega rápida e foco total em conversão.<br>
            Do briefing ao ar em tempo recorde.
        </p>

        <div style="display:flex; gap:16px; justify-content:center; flex-wrap:wrap;">
            <a href="{wa_link('Olá! Quero criar meu site profissional.')}" target="_blank" style="
                display:inline-block;
                background:linear-gradient(135deg, {ACCENT}, #0099BB);
                color:#000; font-family:'Syne',sans-serif;
                font-weight:700; font-size:15px;
                padding:14px 32px; border-radius:10px;
                text-decoration:none; letter-spacing:0.02em;
                box-shadow:0 8px 30px {ACCENT}40;
            ">🔥 Quero meu site agora</a>

            <a href="/4_Planos" style="
                display:inline-block;
                background:transparent;
                color:{TEXT}; font-family:'Syne',sans-serif;
                font-weight:600; font-size:15px;
                padding:14px 32px; border-radius:10px;
                text-decoration:none;
                border:1px solid {BORDER};
            ">Ver planos →</a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ─────────────────────────────────────────
# NÚMEROS / PROVA SOCIAL
# ─────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)

for col, label, value in [
    (c1, "Sites entregues", "47+"),
    (c2, "Clientes satisfeitos", "98%"),
    (c3, "Prazo médio", "7 dias"),
    (c4, "Suporte", "WhatsApp"),
]:
    col.markdown(f"""
    <div class="metric-box">
        <div class="label">{label}</div>
        <div class="value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ─────────────────────────────────────────
# DEPOIMENTOS
# ─────────────────────────────────────────
st.markdown(f'<h2 style="font-family:Syne,sans-serif;font-weight:800;margin-bottom:32px;">⭐ O que dizem os clientes</h2>', unsafe_allow_html=True)

depoimentos = [
    ("Rafael M.", "Dono de pizzaria", "Começamos a receber pedidos pelo site na primeira semana. Entrega foi muito mais rápida do que esperava."),
    ("Ana Souza", "Consultora de RH", "Design profissional, comunicação excelente. Vale cada centavo do investimento."),
    ("Carlos B.", "Loja de roupas", "Minhas vendas online aumentaram muito depois do novo site. Recomendo sem hesitar."),
]

cols = st.columns(3)
for col, (nome, cargo, texto) in zip(cols, depoimentos):
    col.markdown(f"""
    <div class="card">
        <div style="color:#FFB000; font-size:14px; margin-bottom:12px;">★★★★★</div>
        <p style="color:{TEXT}; font-size:14px; line-height:1.7; margin-bottom:16px;">"{texto}"</p>
        <div>
            <div style="font-family:'Syne',sans-serif; font-weight:700; font-size:14px; color:{ACCENT};">{nome}</div>
            <div style="font-size:12px; color:{MUTED};">{cargo}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ─────────────────────────────────────────
# PORTFÓLIO
# ─────────────────────────────────────────
st.markdown(f'<h2 style="font-family:Syne,sans-serif;font-weight:800;margin-bottom:32px;">📁 Projetos em destaque</h2>', unsafe_allow_html=True)

projetos = [
    ("🛍️", "Loja Virtual — Moda Feminina",    "+60% nas vendas em 30 dias",        "#FFB000"),
    ("🍕", "Site Restaurante — Pizzaria Roma",  "Reservas online sem mensalidade",   ACCENT),
    ("💼", "Site Corporativo — Construtora",    "Captação de leads automatizada",    "#9B8AFF"),
    ("🏋️", "Landing Page — Personal Trainer",  "Agenda cheia em 2 semanas",         ACCENT2),
]

col_a, col_b = st.columns(2)
for i, (emoji, titulo, resultado, cor) in enumerate(projetos):
    col = col_a if i % 2 == 0 else col_b
    col.markdown(f"""
    <div class="card" style="border-left:3px solid {cor};">
        <div style="font-size:28px; margin-bottom:10px;">{emoji}</div>
        <div style="font-family:'Syne',sans-serif; font-weight:700; font-size:16px; color:{TEXT}; margin-bottom:6px;">{titulo}</div>
        <div style="font-size:13px; color:{cor}; font-weight:600;">{resultado}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ─────────────────────────────────────────
# PLANOS (preview)
# ─────────────────────────────────────────
st.markdown(f'<h2 style="font-family:Syne,sans-serif;font-weight:800;margin-bottom:8px;">💰 Planos e preços</h2>', unsafe_allow_html=True)
st.markdown(f'<p style="color:{MUTED}; margin-bottom:32px;">Escolha o que faz sentido para o seu negócio</p>', unsafe_allow_html=True)

planos = [
    ("⚡", "Básico",        "R$ 500",  "#556070", ["1 página", "Design clean", "Entrega em 3 dias", "Versão mobile"]),
    ("🚀", "Profissional",  "R$ 1.000", ACCENT,   ["Até 5 páginas", "Design moderno", "Foco em conversão", "SEO básico", "Suporte 30 dias"]),
    ("🔥", "Premium",       "R$ 2.000", "#FFB000", ["Site completo", "Alta performance", "Estratégia de vendas", "Integração WhatsApp", "Suporte 90 dias"]),
]

cols = st.columns(3)
for col, (emoji, nome, preco, cor, itens) in zip(cols, planos):
    destaque = nome == "Profissional"
    border_style = f"border:2px solid {cor}" if destaque else f"border:1px solid {BORDER}"
    itens_html = "".join(f'<li style="font-size:13px;color:{TEXT};margin:4px 0;">✓ {i}</li>' for i in itens)
    col.markdown(f"""
    <div style="background:{CARD};{border_style};border-radius:16px;padding:28px;{'box-shadow:0 0 40px '+cor+'33;' if destaque else ''}">
        <div style="font-size:26px;margin-bottom:8px;">{emoji}</div>
        <div style="font-family:'Syne',sans-serif;font-size:18px;font-weight:800;color:{cor};margin-bottom:4px;">{nome}</div>
        <div style="font-family:'Syne',sans-serif;font-size:32px;font-weight:800;color:{TEXT};margin:12px 0;">
            {preco}
        </div>
        <ul style="list-style:none;padding:0;margin:0 0 20px;">{itens_html}</ul>
        <a href="{wa_link(f'Quero o plano {nome} — R$ {preco}')}" target="_blank" style="
            display:block; text-align:center;
            background:{'linear-gradient(135deg,'+cor+','+cor+'BB)' if destaque else 'transparent'};
            color:{'#000' if destaque else cor};
            border:1px solid {cor};
            font-family:'Syne',sans-serif; font-weight:700; font-size:14px;
            padding:12px; border-radius:8px; text-decoration:none;
        ">Contratar via WhatsApp</a>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ─────────────────────────────────────────
# CTA FINAL
# ─────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center; padding:60px 0;">
    <h2 style="font-family:'Syne',sans-serif;font-weight:800;font-size:40px;color:{TEXT};margin-bottom:16px;">
        Pronto para ter um site que <span style="color:{ACCENT};">vende de verdade?</span>
    </h2>
    <p style="color:{MUTED};font-size:16px;margin-bottom:32px;">
        Respondo rápido no WhatsApp. Vamos conversar sobre o seu projeto.
    </p>
    <a href="{wa_link('Olá! Quero começar meu projeto agora!')}" target="_blank" style="
        display:inline-block;
        background:linear-gradient(135deg,{ACCENT},#0099BB);
        color:#000; font-family:'Syne',sans-serif;
        font-weight:700; font-size:16px;
        padding:16px 48px; border-radius:12px;
        text-decoration:none;
        box-shadow:0 10px 40px {ACCENT}44;
    ">🚀 Começar agora no WhatsApp</a>

    <div style="margin-top:40px; font-size:13px; color:{MUTED};">
        📧 fellipedgtech@gmail.com &nbsp;·&nbsp; 📱 (73) 99994-6196
    </div>
</div>
""", unsafe_allow_html=True)
