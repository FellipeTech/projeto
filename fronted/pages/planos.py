"""
pages/4_Planos.py — Planos e preços
"""

import streamlit as st
import urllib.parse
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import css_global, render_sidebar_nav, ACCENT, ACCENT2, CARD, BORDER, TEXT, MUTED

st.set_page_config(page_title="Planos — DevStudio", page_icon="💰", layout="wide")
css_global()
render_sidebar_nav()

WHATSAPP = "5573999946196"
def wa(msg): return f"https://wa.me/{WHATSAPP}?text={urllib.parse.quote(msg)}"

# ─────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center;padding:40px 0 48px;">
    <h1 style="font-family:'Syne',sans-serif;font-weight:800;font-size:44px;color:{TEXT};margin-bottom:12px;">
        Planos e Preços
    </h1>
    <p style="color:{MUTED};font-size:16px;max-width:500px;margin:0 auto;">
        Invista no site certo para o seu negócio.<br>
        Sem mensalidade oculta — você paga uma vez.
    </p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# CARDS DE PLANOS
# ─────────────────────────────────────────
planos = [
    {
        "key":      "basico",
        "emoji":    "⚡",
        "nome":     "Básico",
        "preco":    "R$ 500",
        "subtitulo":"Para começar com o pé direito",
        "cor":      "#8899AA",
        "destaque": False,
        "itens": [
            "1 página completa",
            "Design clean e moderno",
            "Versão mobile (responsivo)",
            "Formulário de contato",
            "Entrega em até 3 dias",
        ],
        "nao_inclui": ["SEO avançado", "Múltiplas páginas", "Suporte estendido"],
    },
    {
        "key":      "profissional",
        "emoji":    "🚀",
        "nome":     "Profissional",
        "preco":    "R$ 1.000",
        "subtitulo":"O mais escolhido pelos clientes",
        "cor":      ACCENT,
        "destaque": True,
        "itens": [
            "Até 5 páginas",
            "Design moderno e exclusivo",
            "Versão mobile (responsivo)",
            "Foco em conversão e vendas",
            "SEO básico configurado",
            "Integração com WhatsApp",
            "Suporte por 30 dias",
            "Entrega em até 7 dias",
        ],
        "nao_inclui": ["Loja virtual", "Blog integrado"],
    },
    {
        "key":      "premium",
        "emoji":    "🔥",
        "nome":     "Premium",
        "preco":    "R$ 2.000",
        "subtitulo":"Para quem quer resultados máximos",
        "cor":      "#FFB000",
        "destaque": False,
        "itens": [
            "Site completo (sem limite de páginas)",
            "Design premium e exclusivo",
            "Alta performance (PageSpeed 90+)",
            "Estratégia de conversão inclusa",
            "SEO completo e otimizado",
            "Integração WhatsApp + Email",
            "Blog ou área de conteúdo",
            "Suporte prioritário por 90 dias",
            "Entrega em até 15 dias",
        ],
        "nao_inclui": [],
    },
]

cols = st.columns(3)
for col, p in zip(cols, planos):
    cor          = p["cor"]
    nome         = p["nome"]
    preco        = p["preco"]
    emoji        = p["emoji"]
    subtitulo    = p["subtitulo"]
    destaque     = p["destaque"]
    key          = p["key"]

    itens_html   = "".join(f'<li style="font-size:13px;color:{TEXT};margin:5px 0;padding-left:4px;">✓ {i}</li>' for i in p["itens"])
    nao_html     = "".join(f'<li style="font-size:13px;color:{MUTED};margin:5px 0;padding-left:4px;text-decoration:line-through;">✗ {i}</li>' for i in p["nao_inclui"])
    shadow       = f"box-shadow:0 0 60px {cor}30;" if destaque else ""
    border_width = "2px" if destaque else "1px"
    badge        = f'<div style="display:inline-block;background:{cor}22;color:{cor};border:1px solid {cor}44;border-radius:20px;font-size:10px;font-weight:700;font-family:Syne,sans-serif;text-transform:uppercase;letter-spacing:0.1em;padding:4px 10px;margin-bottom:12px;">⭐ Mais popular</div>' if destaque else ""

    nao_block    = f'<ul style="list-style:none;padding:0;margin:0 0 24px;">{nao_html}</ul>' if nao_html else '<div style="margin-bottom:24px;"></div>'

    if destaque:
        btn_bg    = f"linear-gradient(135deg,{cor},{cor}AA)"
        btn_color = "#000"
        btn_border = f"2px solid {cor}"
    else:
        btn_bg    = "transparent"
        btn_color = cor
        btn_border = f"1px solid {cor}"

    wa_link = wa(f"Quero contratar o plano {nome} por {preco}")

    col.markdown(f"""
    <div style="background:{CARD};border:{border_width} solid {cor};border-radius:18px;padding:32px 24px;{shadow}height:100%;">
        {badge}
        <div style="font-size:32px;margin-bottom:10px;">{emoji}</div>
        <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;color:{cor};">{nome}</div>
        <div style="font-size:12px;color:{MUTED};margin:4px 0 20px;">{subtitulo}</div>
        <div style="font-family:'Syne',sans-serif;font-size:38px;font-weight:800;color:{TEXT};margin-bottom:24px;">
            {preco}
            <span style="font-size:14px;font-weight:400;color:{MUTED};">/ único</span>
        </div>
        <ul style="list-style:none;padding:0;margin:0 0 12px;">
            {itens_html}
        </ul>
        {nao_block}
        <a href="{wa_link}" target="_blank" style="
            display:block; text-align:center;
            background:{btn_bg};
            color:{btn_color};
            border:{btn_border};
            font-family:'Syne',sans-serif; font-weight:700; font-size:14px;
            padding:14px; border-radius:10px; text-decoration:none;
            margin-bottom:8px;
        ">Contratar no WhatsApp</a>
    </div>
    """, unsafe_allow_html=True)

    if col.button(f"Pagar online — {nome}", key=key):
        st.session_state["plano_selecionado"] = key
        st.switch_page("pages/5_Pagamento.py")

st.divider()

# ─────────────────────────────────────────
# FAQ
# ─────────────────────────────────────────
st.markdown(f'<h2 style="font-family:Syne,sans-serif;font-weight:800;margin-bottom:24px;text-align:center;">❓ Perguntas frequentes</h2>', unsafe_allow_html=True)

faqs = [
    ("Quanto tempo leva para ficar pronto?", "Depende do plano: Básico em 3 dias, Profissional em 7 dias e Premium em até 15 dias."),
    ("O site fica no meu domínio?", "Sim! Configuramos o site no seu próprio domínio. Se ainda não tiver um, podemos ajudar a registrar."),
    ("Preciso pagar mensalidade?", "Não. Você paga uma vez pelo desenvolvimento. Hospedagem e domínio têm custos separados e bem acessíveis."),
    ("Posso pedir alterações depois?", "Sim, dentro do período de suporte incluso no plano. Alterações adicionais são cobradas separadamente."),
    ("Quais formas de pagamento?", "Pix, cartão de crédito (em até 12x) ou boleto bancário."),
]

for pergunta, resposta in faqs:
    with st.expander(pergunta):
        st.write(resposta)
