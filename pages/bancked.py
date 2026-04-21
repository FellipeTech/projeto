from fastapi import FastAPI, Request
import uuid

app = FastAPI()

# =========================
# "BANCO" TEMPORÁRIO
# =========================
usuarios = {}
pagamentos = {}

# =========================
# CADASTRO
# =========================
@app.post("/register")
def register(dados: dict):
    email = dados["email"]

    if email in usuarios:
        return {"erro": "Usuário já existe"}

    usuarios[email] = {
        "senha": dados["senha"],
        "ativo": False
    }

    return {"msg": "Usuário criado"}

# =========================
# LOGIN
# =========================
@app.post("/login")
def login(dados: dict):
    user = usuarios.get(dados["email"])

    if not user or user["senha"] != dados["senha"]:
        return {"erro": "Login inválido"}

    return {
        "msg": "ok",
        "ativo": user["ativo"]
    }

# =========================
# GERAR PIX
# =========================
@app.post("/gerar_pix")
def gerar_pix(dados: dict):

    txid = str(uuid.uuid4())

    pagamentos[txid] = {
        "email": dados["email"],
        "status": "PENDENTE"
    }

    pix_fake = f"PIX-{txid}"

    return {
        "txid": txid,
        "pix": pix_fake
    }

# =========================
# WEBHOOK (SIMULADO)
# =========================
@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()

    txid = data["txid"]

    pagamentos[txid]["status"] = "PAGO"

    email = pagamentos[txid]["email"]
    usuarios[email]["ativo"] = True

    return {"ok": True}

# =========================
# STATUS
# =========================
@app.get("/status/{txid}")
def status(txid: str):
    return pagamentos.get(txid, {})