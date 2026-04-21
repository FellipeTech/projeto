import streamlit as st
import urllib.parse

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Pagamento", layout="centered")

numero = "5573999946196"

# Pix copia e cola
pix_copia_cola = "00020101021126330014br.gov.bcb.pix0111097492825905204000053039865802BR5920FELLIPE F BITENCOURT6007ITABUNA62070503***6304F001"

# =========================
# FUNÇÃO WHATSAPP
# =========================
def criar_link(msg):
    return f"https://wa.me/{numero}?text={urllib.parse.quote(msg)}"

# =========================
# PLANOS
# =========================
planos = {
    "Básico": 500,
    "Profissional": 1000,
    "Premium": 2000
}

st.title("💳 Finalizar pagamento")

plano = st.selectbox("Escolha seu plano:", list(planos.keys()))
valor = planos[plano]

# =========================
# RESUMO
# =========================
st.markdown(f"""
### 📦 Resumo
Plano: {plano}  
Valor: R${valor}
""")

# =========================
# PAGAMENTO PIX
# =========================
st.header("💸 Pagamento via Pix")

st.write("Copie o código abaixo e pague no seu banco:")

st.code(pix_copia_cola)

st.caption("Após o pagamento, clique em confirmar abaixo 👇")

# =========================
# CONFIRMAÇÃO
# =========================
st.divider()

msg = f"Já fiz o pagamento do plano {plano} (R${valor})"
link = criar_link(msg)

st.markdown(f"[📲 Confirmar no WhatsApp]({link})")