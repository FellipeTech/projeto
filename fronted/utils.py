"""
utils.py - Funções e estilos compartilhados entre todas as páginas
"""

import streamlit as st
import requests

API = "http://localhost:8000"

# ==========================================
# PALETA E FONTES
# ==========================================
ACCENT = "#00E5FF"        # ciano elétrico
ACCENT2 = "#FF4B6E"       # vermelho-rosa
BG = "#080C14"            # fundo ultra escuro
CARD = "#0F1623"          # card
BORDER = "#1C2A40"        # bordas sutis
TEXT = "#E2EAF4"          # texto principal
MUTED = "#556070"         # texto secundário

def css_global():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

    html, body, [class*="css"] {{
        font-family: 'DM Sans', sans-serif;
        background-color: {BG};
        color: {TEXT};
    }}

    /* Esconde o menu padrão do Streamlit */
    #MainMenu, footer {{ visibility: hidden; }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background: {CARD};
        border-right: 1px solid {BORDER};
    }}
    [data-testid="stSidebar"] * {{
        color: {TEXT} !important;
    }}

    /* Inputs */
    .stTextInput > div > div > input,
    .stSelectbox > div > div {{
        background: #111826 !important;
        border: 1px solid {BORDER} !important;
        color: {TEXT} !important;
        border-radius: 8px !important;
    }}
    .stTextInput > div > div > input:focus {{
        border-color: {ACCENT} !important;
        box-shadow: 0 0 0 2px {ACCENT}22 !important;
    }}

    /* Botões */
    .stButton > button {{
        background: linear-gradient(135deg, {ACCENT}, #0099BB) !important;
        color: #000 !important;
        font-weight: 700 !important;
        font-family: 'Syne', sans-serif !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.5rem !important;
        letter-spacing: 0.02em !important;
        transition: all 0.2s !important;
    }}
    .stButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px {ACCENT}44 !important;
    }}

    /* Alertas */
    .stSuccess {{ background: #0A2A1A !important; border-left: 3px solid #00C875 !important; }}
    .stError   {{ background: #2A0A0A !important; border-left: 3px solid {ACCENT2} !important; }}
    .stWarning {{ background: #2A1E0A !important; border-left: 3px solid #FFB000 !important; }}
    .stInfo    {{ background: #0A1A2A !important; border-left: 3px solid {ACCENT} !important; }}

    /* Divider */
    hr {{ border-color: {BORDER} !important; margin: 2rem 0 !important; }}

    /* Títulos */
    h1, h2, h3 {{ font-family: 'Syne', sans-serif !important; color: {TEXT} !important; }}
    h1 {{ font-weight: 800 !important; }}

    /* Badges / chips */
    .badge {{
        display: inline-block;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        font-family: 'Syne', sans-serif;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    .badge-ativo   {{ background: #00C87522; color: #00C875; border: 1px solid #00C87544; }}
    .badge-inativo {{ background: {ACCENT2}22; color: {ACCENT2}; border: 1px solid {ACCENT2}44; }}
    .badge-plano   {{ background: {ACCENT}22; color: {ACCENT}; border: 1px solid {ACCENT}44; }}

    /* Cards */
    .card {{
        background: {CARD};
        border: 1px solid {BORDER};
        border-radius: 14px;
        padding: 24px;
        margin-bottom: 16px;
        transition: border-color 0.2s;
    }}
    .card:hover {{ border-color: {ACCENT}66; }}

    /* Métrica */
    .metric-box {{
        background: {CARD};
        border: 1px solid {BORDER};
        border-radius: 12px;
        padding: 20px 24px;
        text-align: center;
    }}
    .metric-box .label {{
        font-size: 12px;
        color: {MUTED};
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 4px;
    }}
    .metric-box .value {{
        font-family: 'Syne', sans-serif;
        font-size: 28px;
        font-weight: 800;
        color: {ACCENT};
    }}
    </style>
    """, unsafe_allow_html=True)


# ==========================================
# PROTEÇÃO DE ROTA
# ==========================================

def requer_login():
    if "user" not in st.session_state:
        st.warning("Você precisa estar logado para acessar esta página.")
        st.page_link("pages/1_Login.py", label="→ Fazer Login")
        st.stop()

def requer_admin():
    requer_login()
    if not st.session_state.get("admin"):
        st.error("Acesso restrito a administradores.")
        st.stop()


# ==========================================
# HELPERS HTTP
# ==========================================

def api_get(path: str):
    try:
        return requests.get(f"{API}{path}", timeout=5).json()
    except Exception as e:
        st.error(f"Erro de conexão com a API: {e}")
        return {}

def api_post(path: str, payload: dict):
    try:
        return requests.post(f"{API}{path}", json=payload, timeout=5).json()
    except Exception as e:
        st.error(f"Erro de conexão com a API: {e}")
        return {}


# ==========================================
# COMPONENTES REUTILIZÁVEIS
# ==========================================

def render_sidebar_nav():
    """Exibe logo e info do usuário na sidebar"""
    st.sidebar.markdown(f"""
    <div style="padding: 16px 0 24px;">
        <div style="font-family:'Syne',sans-serif; font-size:22px; font-weight:800; color:{ACCENT}; letter-spacing:-0.02em;">
            ⬡ DEV<span style="color:{TEXT};">STUDIO</span>
        </div>
        <div style="font-size:11px; color:{MUTED}; margin-top:4px; text-transform:uppercase; letter-spacing:0.08em;">
            Plataforma de Sites
        </div>
    </div>
    """, unsafe_allow_html=True)

    if "user" in st.session_state:
        plano = st.session_state.get("plano") or "—"
        ativo = st.session_state.get("ativo", False)
        badge = f'<span class="badge badge-ativo">Ativo</span>' if ativo else f'<span class="badge badge-inativo">Inativo</span>'
        st.sidebar.markdown(f"""
        <div style="padding:12px 16px; background:#111826; border-radius:10px; margin-bottom:16px; border:1px solid {BORDER};">
            <div style="font-size:13px; color:{MUTED};">Logado como</div>
            <div style="font-size:14px; font-weight:600; color:{TEXT}; margin:2px 0 6px;">{st.session_state['user']}</div>
            {badge}
        </div>
        """, unsafe_allow_html=True)


PLANOS_INFO = {
    "basico":       {"emoji": "⚡", "nome": "Básico",       "valor": 500,  "cor": "#556070"},
    "profissional": {"emoji": "🚀", "nome": "Profissional", "valor": 1000, "cor": ACCENT},
    "premium":      {"emoji": "🔥", "nome": "Premium",      "valor": 2000, "cor": "#FFB000"},}