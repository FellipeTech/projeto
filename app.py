import streamlit as st
import requests
import time

API = "http://localhost:8000"

st.set_page_config(page_title="Sistema")

# MENU
if "user" not in st.session_state:
    menu = st.sidebar.selectbox("Menu", ["Login", "Cadastro"])
else:
    if st.session_state.get("admin"):
        menu = st.sidebar.selectbox("Menu", ["Admin", "Sair"])
    else:
        menu = st.sidebar.selectbox(
            "Menu",
            ["Dashboard", "Meus Sites", "Pagamento", "Sair"]
        )

# CADASTRO
if menu == "Cadastro":
    st.title("Cadastro")

    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")

    if st.button("Cadastrar"):
        r = requests.post(f"{API}/register", json={
            "email": email,
            "senha": senha
        }).json()

        st.write(r)

# LOGIN
if menu == "Login":
    st.title("Login")

    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        r = requests.post(f"{API}/login", json={
            "email": email,
            "senha": senha
        }).json()

        if "erro" in r:
            st.error("Erro")
        else:
            st.session_state["user"] = email
            st.session_state["admin"] = r["admin"]
            st.session_state["ativo"] = r["ativo"]

# DASHBOARD
if menu == "Dashboard":
    st.title("Área do membro")

    user = requests.get(f"{API}/usuario/{st.session_state['user']}").json()

    if user.get("ativo"):
        st.success("Acesso liberado")
    else:
        st.warning("Precisa pagar")

# MEUS SITES
if menu == "Meus Sites":
    st.title("Seus sites")

    user = requests.get(f"{API}/usuario/{st.session_state['user']}").json()

    for site in user.get("sites", []):
        st.success(site)

# PAGAMENTO
if menu == "Pagamento":
    st.title("Pagamento")

    if st.button("Gerar Pix"):
        r = requests.post(f"{API}/gerar_pix", json={
            "email": st.session_state["user"]
        }).json()

        st.session_state["txid"] = r["txid"]
        st.code(r["pix"])

    if "txid" in st.session_state:
        status = requests.get(
            f"{API}/status/{st.session_state['txid']}"
        ).json()

        if status.get("status") == "PAGO":
            st.success("Pago!")
        else:
            st.warning("Aguardando...")
            time.sleep(5)
            st.rerun()

# ADMIN
if menu == "Admin":
    st.title("Admin")

    usuarios = requests.get(f"{API}/usuarios").json()

    for email, dados in usuarios.items():
        st.write(email, dados)

        if not dados.get("ativo"):
            if st.button(f"Ativar {email}"):
                requests.post(f"{API}/ativar", json={"email": email})
                st.rerun()

# SAIR
if menu == "Sair":
    st.session_state.clear()
    st.rerun()
import streamlit as st
import urllib.parse

st.set_page_config(page_title="Dev Freelancer", layout="wide")

# =========================
# CONFIG WHATSAPP
# =========================
numero = "5573999946196"

def criar_link(msg):
    return f"https://wa.me/{numero}?text={urllib.parse.quote(msg)}"

# =========================
# ESTILO
# =========================
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}
h1, h2, h3 {
    color: white;
}
p {
    color: #cfcfcf;
}
.stButton>button {
    width: 100%;
    border-radius: 10px;
    height: 3em;
    font-size: 16px;
    font-weight: bold;
    background: linear-gradient(90deg, #ff4b2b, #ff416c);
    color: white;
    border: none;
}
.box {
    padding: 20px;
    border-radius: 12px;
    background: #161b22;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HERO
# =========================
col1, col2 = st.columns([2,1])

with col1:
    st.title("🚀 Sites que transformam visitantes em clientes")

    st.write("""
    Eu crio sites rápidos, modernos e pensados para gerar resultado.  
    Seu site deixa de ser só bonito e passa a **vender de verdade**.
    """)

    link = criar_link("Olá! Quero criar um site profissional que gere clientes.")
    st.markdown(f"[🔥 Quero meu site agora]({link})")

with col2:
    link = criar_link("Olá! Vim pelo site e quero mais informações.")
    st.markdown(f"""
    <div class="box">
    <h3>💬 Fale comigo</h3>
    <p>Resposta rápida no WhatsApp</p>
    <a href="{link}" target="_blank">
        <button style="width:100%;padding:10px;background:#25D366;color:white;border:none;border-radius:8px;">
        Chamar no WhatsApp
        </button>
    </a>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# =========================
# PROVA SOCIAL
# =========================
st.header("⭐ Resultados reais")

st.write("""
💬 "Comecei a receber clientes toda semana"  
💬 "Entrega rápida e profissional"  
💬 "Valeu cada centavo"
""")

st.divider()

# =========================
# PORTFÓLIO
# =========================
st.header("📁 Projetos")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="box">
    <h4>🛍️ Loja Virtual</h4>
    <p>+60% nas vendas após novo site</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="box">
    <h4>💼 Site Empresarial</h4>
    <p>Novos clientes toda semana</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# =========================
# PLANOS COM PAGAMENTO
# =========================
st.header("💰 Planos")

col1, col2, col3 = st.columns(3)

with col1:
    msg = "Quero o plano Básico (R$500)"
    link = criar_link(msg)

    st.markdown("""
    <div class="box">
    <h3>💡 Básico</h3>
    <p>✔ 1 página<br>✔ Design simples<br>✔ Entrega rápida</p>
    <h2>R$ 500</h2>
    <p>💳 Pix / Cartão</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("[Escolher Básico](?plano=basico)")
    if st.button("Escolher Básico"):
        st.session_state.plano = "basico"
        st.switch_page("pages/pagamento.py")



with col2:
    msg = "Quero o plano Profissional (R$1000)"
    link = criar_link(msg)

    st.markdown("""
    <div class="box">
    <h3>🚀 Profissional</h3>
    <p>✔ Até 5 páginas<br>✔ Design moderno<br>✔ Foco em conversão</p>
    <h2>R$ 1000</h2>
    <p>💳 Pix / Cartão / Parcelado</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("[Escolher Profissional](?plano=profissional)")
    if st.button("Escolher Profissional"):
        st.session_state.plano = "profissional"
        st.switch_page("pages/pagamento.py")


with col3:
    msg = "Quero o plano Premium (R$2000)"
    link = criar_link(msg)

    st.markdown("""
    <div class="box">
    <h3>🔥 Premium</h3>
    <p>✔ Site completo<br>✔ Alta performance<br>✔ Estratégia de vendas</p>
    <h2>R$ 2000</h2>
    <p>💳 Pix / Cartão / Parcelado</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("[Escolher Premium](?plano=premium)")
    if st.button("Escolher Premium"):
        st.session_state.plano = "premium"
        st.switch_page("pages/pagamento.py")


st.divider()

# =========================
# CTA FINAL
# =========================
st.header("🔥 Pronto para ter um site que vende?")

link = criar_link("Quero começar meu projeto agora!")

st.markdown(f"[🚀 Começar agora]({link})")

st.divider()

# =========================
# CONTATO
# =========================
st.header("📞 Contato")

st.write("""
📧 fellipedgtech@gmail.com  
📱 WhatsApp disponível acima  
""")
