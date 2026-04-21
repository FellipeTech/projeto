import streamlit as st
import qrcode
from io import BytesIO
import urllib.parse
query_params = st.query_params

plano = query_params.get("plano", "basico")
if plano == "basico":
    nome_plano = "Básico"
    preco = "R$500"
elif plano == "profissional":
    nome_plano = "Profissional"
    preco = "R$1000"
else:
    nome_plano = "Premium"
    preco = "R$2000"

st.set_page_config(page_title="Pagamento", layout="centered")

# =========================
# CONFIG
# =========================
numero = "5573999946196"  # seu WhatsApp

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
# ESCOLHA DO PLANO
# =========================
plano = st.selectbox("Escolha seu plano:", [
    "Básico - R$500",
    "Profissional - R$1000",
    "Premium - R$2000"
])

# =========================
# RESUMO
# =========================
st.markdown(f"""
### 📦 Resumo
Plano: {nome_plano}  
Valor: {preco}
""")
#st.markdown(f"""
#<div class="box">
#<h3>📦 Resumo do pedido</h3>
#<p><b>Plano:</b> {plano}</p>
#<p>✔ Entrega rápida</p>
#<p>✔ Suporte incluído</p>
#</div>
#""", unsafe_allow_html=True)

# =========================
# PAGAMENTO PIX
# =========================
st.header("💸 Pagamento via Pix")

pix_chave = "09749282590"

# gerar QR code
qr = qrcode.make(pix_chave)
buf = BytesIO()
qr.save(buf)
st.image(buf.getvalue(), caption="Escaneie para pagar")

st.write(f"🔑 Chave Pix: {pix_chave}")

# =========================
# PAGAMENTO CARTÃO (SIMULADO)
# =========================
st.header("💳 Cartão (simulação)")

st.text_input("Número do cartão")
st.text_input("Nome no cartão")
st.text_input("Validade")
st.text_input("CVV")

st.button("Pagar com cartão")

# =========================
# CONFIRMAÇÃO
# =========================
st.divider()

st.header("✅ Já realizou o pagamento?")
msg = f"Já fiz o pagamento do plano {nome_plano} ({preco})"
link = f"https://wa.me/{numero}?text={urllib.parse.quote(msg)}"

st.markdown(f"[Confirmar pagamento no WhatsApp]({link})")


