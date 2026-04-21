import streamlit as st
import requests
import time

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Pagamento", layout="centered")

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
# GERAR PIX
# =========================
if st.button("Gerar Pix"):
    response = requests.post(f"{API_URL}/gerar_pix", json={
        "valor": valor,
        "descricao": f"Plano {plano}"
    })

    data = response.json()

    st.session_state["txid"] = data["txid"]
    st.session_state["pix"] = data["pix"]

# =========================
# MOSTRAR PIX
# =========================
if "pix" in st.session_state:

    st.header("💸 Pagamento via Pix")

    st.code(st.session_state["pix"])

    st.info("Após pagar, o sistema confirma automaticamente...")

# =========================
# AUTO VERIFICAÇÃO
# =========================
if "txid" in st.session_state:

    status = requests.get(
        f"{API_URL}/status/{st.session_state['txid']}"
    ).json()

    if status["status"] == "PAGO":
        st.success("✅ Pagamento confirmado automaticamente!")
        st.balloons()
    else:
        st.warning("⏳ Aguardando pagamento...")
        time.sleep(5)
        st.rerun()