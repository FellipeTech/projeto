import streamlit as st
import mercadopago
import urllib.parse

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Pagamento", layout="centered")

ACCESS_TOKEN = "SEU_ACCESS_TOKEN_AQUI"
sdk = mercadopago.SDK(ACCESS_TOKEN)

numero = "5573999946196"

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
# CRIAR PAGAMENTO PIX
# =========================
if st.button("Gerar Pix"):
    payment_data = {
        "transaction_amount": valor,
        "description": f"Plano {plano}",
        "payment_method_id": "pix",
        "payer": {
            "email": "cliente@email.com"
        }
    }

    pagamento = sdk.payment().create(payment_data)
    resposta = pagamento["response"]

    pix_code = resposta["point_of_interaction"]["transaction_data"]["qr_code"]
    qr_base64 = resposta["point_of_interaction"]["transaction_data"]["qr_code_base64"]

    st.success("Pix gerado!")

    st.image(f"data:image/png;base64,{qr_base64}")
    st.code(pix_code)

# =========================
# PAGAMENTO CARTÃO
# =========================
st.header("💳 Cartão")

st.write("Pagamento com cartão (via Mercado Pago Checkout):")

preference_data = {
    "items": [
        {
            "title": f"Plano {plano}",
            "quantity": 1,
            "currency_id": "BRL",
            "unit_price": valor
        }
    ]
}

preference = sdk.preference().create(preference_data)
link_pagamento = preference["response"]["init_point"]

st.markdown(f"[👉 Pagar com cartão]({link_pagamento})")

# =========================
# WHATSAPP
# =========================
st.divider()

msg = f"Já fiz o pagamento do plano {plano} (R${valor})"
link = criar_link(msg)

st.markdown(f"[📲 Confirmar no WhatsApp]({link})")