from fastapi import FastAPI, Request
import requests
import uuid

app = FastAPI()

# =========================
# CONFIG INTER
# =========================
CLIENT_ID = "SEU_CLIENT_ID"
CLIENT_SECRET = "SEU_CLIENT_SECRET"
CHAVE_PIX = "SUA_CHAVE_PIX"

CERT_PATH = "certificado.pem"
KEY_PATH = "chave.pem"

# banco simples (substituir depois)
pagamentos = {}

# =========================
# GERAR TOKEN
# =========================
def gerar_token():
    url = "https://cdpj.partners.bancointer.com.br/oauth/v2/token"

    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials",
        "scope": "pix.write pix.read"
    }

    response = requests.post(
        url,
        data=data,
        cert=(CERT_PATH, KEY_PATH)
    )

    return response.json()["access_token"]

# =========================
# GERAR PIX REAL
# =========================
@app.post("/gerar_pix")
def gerar_pix(dados: dict):

    token = gerar_token()

    txid = str(uuid.uuid4())[:30]

    url = f"https://cdpj.partners.bancointer.com.br/pix/v2/cob/{txid}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    body = {
        "calendario": {"expiracao": 3600},
        "valor": {"original": f"{dados['valor']:.2f}"},
        "chave": CHAVE_PIX,
        "solicitacaoPagador": dados["descricao"]
    }

    response = requests.put(
        url,
        json=body,
        headers=headers,
        cert=(CERT_PATH, KEY_PATH)
    )

    resposta = response.json()

    pagamentos[txid] = "PENDENTE"

    return {
        "txid": txid,
        "pix": resposta["pixCopiaECola"]
    }

# =========================
# WEBHOOK (INTER CHAMA AQUI)
# =========================
@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()

    try:
        pix = data["pix"][0]
        txid = pix["txid"]

        pagamentos[txid] = "PAGO"

        print("Pagamento confirmado:", txid)

    except:
        print("Erro no webhook")

    return {"ok": True}

# =========================
# CONSULTAR STATUS
# =========================
@app.get("/status/{txid}")
def status(txid: str):
    return {"status": pagamentos.get(txid, "PENDENTE")}