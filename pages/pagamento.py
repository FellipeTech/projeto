import streamlit as st
import qrcode
from io import BytesIO
import urllib.parse

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Pagamento", layout="centered")

numero = "5573999946196"  # seu WhatsApp
pix_chave = "09749282590"

# =========================
# FUNÇÕES
# =========================
def criar_link(msg):
    return f"https://wa.me/{numero}?text={urllib.parse.quote(msg)}"

def gerar_qrcode(dado):
    qr = qrcode.make(dado)
    buf = BytesIO()
    qr.save(buf)
    return buf.getvalue()

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
.box {
    padding: 20px;
    border-radius: 12px;
    background: #161b22;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# TÍTULO
# =========================
st.title("💳 Finalizar pagamento")

# =========================
# PLANOS
# =========================
planos = {
    "Básico": 500,
    "Profissional": 1000,
    "Premium": 2000
}

plano_escolhido = st.selectbox("Escolha seu plano:", list(planos.keys()))
preco = planos[plano_escolhido]

# =========================
# RESUMO
# =========================
st.markdown(f"""
<div class="box">
<h3>📦 Resumo do pedido</h3>
<p><b>Plano:</b> {plano_escolhido}</p>
<p><b>Valor:</b> R${preco}</p>
<p>✔ Entrega rápida</p>
<p>✔ Suporte incluído</p>
</div>
""", unsafe_allow_html=True)

# =========================
# PAGAMENTO PIX
# =========================
st.header("💸 Pagamento via Pix")

qr_img = gerar_qrcode(pix_chave)
st.image(qr_img, caption="Escaneie para pagar")

st.code(pix_chave, language="")

# =========================
# PAGAMENTO CARTÃO (SIMULADO)
# =========================
st.header("💳 Cartão (simulação)")

col1, col2 = st.columns(2)

with col1:
    numero_cartao = st.text_input("Número do cartão")

with col2:
    nome_cartao = st.text_input("Nome no cartão")

col3, col4 = st.columns(2)

with col3:
    validade = st.text_input("Validade")

with col4:
    cvv = st.text_input("CVV")

if st.button("Pagar com cartão"):
    if numero_cartao and nome_cartao and validade and cvv:
        st.success("Pagamento simulado com sucesso!")
    else:
        st.error("Preencha todos os campos")

# =========================
# CONFIRMAÇÃO
# =========================
st.divider()

st.header("✅ Já realizou o pagamento?")

mensagem = f"Já fiz o pagamento do plano {plano_escolhido} (R${preco})"
link = criar_link(mensagem)

st.markdown(f"[📲 Confirmar pagamento no WhatsApp]({link})")


