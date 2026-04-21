from fastapi import FastAPI, Request

app = FastAPI()

# banco fake (depois você troca por banco real)
pagamentos = {}

@app.post("/webhook")
async def receber_webhook(request: Request):
    data = await request.json()

    try:
        pix = data["pix"][0]
        txid = pix["txid"]

        pagamentos[txid] = "PAGO"

        print(f"Pagamento confirmado: {txid}")

    except:
        print("Erro no webhook")

    return {"status": "ok"}

@app.get("/status/{txid}")
def status(txid: str):
    return {"status": pagamentos.get(txid, "PENDENTE")}