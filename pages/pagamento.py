import streamlit as st
import urllib.parse

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Pagamento", layout="centered")

numero = "5573999946196"  # WhatsApp

# Pix copia e cola (EMV)
pix_copia_cola = "00020101021126330014br.gov.bcb.pix0111097492825905204000053039865802BR5920FELLIPE F BITENCOURT6007ITABUNA62070503***6304F001"

# =========================
# FUNÇÃO WHATSAPP
# =========================
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
# PAGAMENTO PIX (CÓPIA E COLA)
# =========================
st.header("💸 Pagamento via Pix")

st.write("Copie o código abaixo e pague no seu banco:")

st.code(pix_copia_cola)

st.caption("Após o pagamento, clique em confirmar abaixo 👇")

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
    validade = st.text_input("Validade (MM/AA)")

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