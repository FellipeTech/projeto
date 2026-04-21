"""
Backend - API FastAPI
Sistema de Membros e Vendas de Sites
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uuid
import hashlib
from datetime import datetime

app = FastAPI(title="Dev Freelancer API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# BANCO DE DADOS EM MEMÓRIA (substitua por DB real)
# ==========================================
usuarios = {}
pagamentos = {}

PLANOS = {
    "basico":       {"nome": "Básico",       "valor": 500,  "descricao": "1 página, design simples, entrega rápida"},
    "profissional": {"nome": "Profissional", "valor": 1000, "descricao": "Até 5 páginas, design moderno, foco em conversão"},
    "premium":      {"nome": "Premium",      "valor": 2000, "descricao": "Site completo, alta performance, estratégia de vendas"},
}

def hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()


# ==========================================
# AUTENTICAÇÃO
# ==========================================

@app.post("/register")
def register(dados: dict):
    email = dados.get("email", "").strip().lower()
    senha = dados.get("senha", "")

    if not email or not senha:
        return {"erro": "Email e senha são obrigatórios"}

    if email in usuarios:
        return {"erro": "Este email já está cadastrado"}

    if len(senha) < 6:
        return {"erro": "Senha deve ter pelo menos 6 caracteres"}

    usuarios[email] = {
        "email": email,
        "senha": hash_senha(senha),
        "nome": dados.get("nome", ""),
        "telefone": dados.get("telefone", ""),
        "ativo": False,
        "sites": [],
        "plano": None,
        "admin": email == "admin@email.com",
        "criado_em": datetime.now().isoformat(),
    }

    return {"msg": "Conta criada com sucesso!"}


@app.post("/login")
def login(dados: dict):
    email = dados.get("email", "").strip().lower()
    senha = dados.get("senha", "")

    user = usuarios.get(email)

    if not user or user["senha"] != hash_senha(senha):
        return {"erro": "Email ou senha inválidos"}

    return {
        "msg": "Login realizado!",
        "email": user["email"],
        "nome": user["nome"],
        "ativo": user["ativo"],
        "admin": user["admin"],
        "plano": user["plano"],
    }


# ==========================================
# USUÁRIO
# ==========================================

@app.get("/usuario/{email}")
def get_user(email: str):
    user = usuarios.get(email.lower())
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    # Retorna sem a senha
    return {k: v for k, v in user.items() if k != "senha"}


@app.post("/configurar")
def configurar(dados: dict):
    email = dados.get("email", "").lower()
    user = usuarios.get(email)

    if not user:
        return {"erro": "Usuário não encontrado"}

    if dados.get("nome"):
        user["nome"] = dados["nome"]
    if dados.get("telefone"):
        user["telefone"] = dados["telefone"]

    return {"msg": "Perfil atualizado!"}


# ==========================================
# PLANOS
# ==========================================

@app.get("/planos")
def listar_planos():
    return PLANOS


# ==========================================
# PAGAMENTO (Pix simulado)
# ==========================================

@app.post("/gerar_pix")
def gerar_pix(dados: dict):
    email = dados.get("email", "").lower()
    plano_key = dados.get("plano", "basico")

    if email not in usuarios:
        return {"erro": "Usuário não encontrado"}

    plano = PLANOS.get(plano_key)
    if not plano:
        return {"erro": "Plano inválido"}

    txid = str(uuid.uuid4()).replace("-", "")[:20].upper()

    pagamentos[txid] = {
        "email": email,
        "plano": plano_key,
        "valor": plano["valor"],
        "status": "PENDENTE",
        "criado_em": datetime.now().isoformat(),
    }

    # Código Pix fictício (em produção, integre com banco real)
    pix_code = (
        f"00020126580014br.gov.bcb.pix"
        f"0136{txid}"
        f"520400005303986"
        f"54{str(plano['valor']).zfill(6)}"
        f"5802BR5925DEV FREELANCER6009SAO PAULO"
        f"62140510{txid[:10]}6304ABCD"
    )

    return {
        "txid": txid,
        "pix": pix_code,
        "valor": plano["valor"],
        "plano": plano["nome"],
    }


@app.get("/status/{txid}")
def status_pagamento(txid: str):
    pag = pagamentos.get(txid)
    if not pag:
        return {"erro": "Pagamento não encontrado"}
    return pag


@app.post("/webhook")
async def webhook(request: Request):
    """Webhook chamado pelo banco ao confirmar pagamento"""
    data = await request.json()
    txid = data.get("txid")

    if txid not in pagamentos:
        return {"erro": "txid inválido"}

    pagamentos[txid]["status"] = "PAGO"
    pagamentos[txid]["pago_em"] = datetime.now().isoformat()

    email = pagamentos[txid]["email"]
    plano_key = pagamentos[txid]["plano"]
    plano = PLANOS.get(plano_key, {})

    usuarios[email]["ativo"] = True
    usuarios[email]["plano"] = plano_key
    usuarios[email]["sites"].append(f"Site {plano.get('nome', 'Premium')} - Contrate via WhatsApp")

    return {"ok": True}


# ==========================================
# ADMIN
# ==========================================

@app.get("/admin/usuarios")
def admin_listar():
    return {
        email: {k: v for k, v in dados.items() if k != "senha"}
        for email, dados in usuarios.items()
    }


@app.post("/admin/ativar")
def admin_ativar(dados: dict):
    email = dados.get("email", "").lower()

    if email not in usuarios:
        return {"erro": "Usuário não encontrado"}

    plano_key = dados.get("plano", "basico")
    plano = PLANOS.get(plano_key, PLANOS["basico"])

    usuarios[email]["ativo"] = True
    usuarios[email]["plano"] = plano_key

    site_label = f"Site {plano['nome']} — Ativado manualmente em {datetime.now().strftime('%d/%m/%Y')}"
    if site_label not in usuarios[email]["sites"]:
        usuarios[email]["sites"].append(site_label)

    return {"msg": f"Usuário {email} ativado com sucesso"}


@app.post("/admin/desativar")
def admin_desativar(dados: dict):
    email = dados.get("email", "").lower()

    if email not in usuarios:
        return {"erro": "Usuário não encontrado"}

    usuarios[email]["ativo"] = False
    return {"msg": f"Usuário {email} desativado"}


@app.get("/admin/pagamentos")
def admin_pagamentos():
    return pagamentos


# ==========================================
# SIMULAR PAGAMENTO (apenas para testes)
# ==========================================

@app.post("/dev/simular_pago")
def simular_pago(dados: dict):
    """Apenas para testes — simula confirmação do Pix"""
    txid = dados.get("txid")

    if txid not in pagamentos:
        return {"erro": "txid inválido"}

    pagamentos[txid]["status"] = "PAGO"
    pagamentos[txid]["pago_em"] = datetime.now().isoformat()

    email = pagamentos[txid]["email"]
    plano_key = pagamentos[txid]["plano"]
    plano = PLANOS.get(plano_key, {})

    usuarios[email]["ativo"] = True
    usuarios[email]["plano"] = plano_key
    usuarios[email]["sites"].append(f"Site {plano.get('nome', 'Premium')} — Pago em {datetime.now().strftime('%d/%m/%Y')}")

    return {"msg": "Pagamento simulado com sucesso!"}