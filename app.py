import streamlit as st

# CONFIG
st.set_page_config(page_title="Dev Freelancer", layout="wide")

# =========================
# ESTILO (CSS)
# =========================
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Arial', sans-serif;
}

.main {
    background-color: #0E1117;
}

h1, h2, h3 {
    color: white;
}

p {
    color: #cfcfcf;
}

.stButton>button {
    width: 100%;
    border-radius: 10px;
    height: 3em;
    font-size: 16px;
    font-weight: bold;
    background: linear-gradient(90deg, #ff4b2b, #ff416c);
    color: white;
    border: none;
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
# HERO
# =========================
col1, col2 = st.columns([2,1])

with col1:
    st.title("🚀 Sites que transformam visitantes em clientes")

    st.write("""
    Eu crio sites rápidos, modernos e pensados para gerar resultado.  
    Nada de site bonito que não vende.
    """)

    st.markdown("### ⚡ Entrega rápida | 🎯 Foco em conversão | 💰 Mais clientes")

    st.button("🔥 Quero meu site agora")

with col2:
    st.markdown("""
    <div class="box">
    <h3>💬 Fale comigo</h3>
    <p>Resposta rápida no WhatsApp</p>
    <a href="https://wa.me/5573999946196" target="_blank">
        <button style="width:100%;padding:10px;background:#25D366;color:white;border:none;border-radius:8px;">
        Chamar no WhatsApp
        </button>
    </a>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# =========================
# PROVA SOCIAL
# =========================
st.header("⭐ Quem já trabalhou comigo")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="box">
    💬 "Meu site começou a gerar clientes todo dia"  
    <br><br>— Cliente local
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="box">
    💬 "Entrega rápida e muito profissional"  
    <br><br>— Empreendedora
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="box">
    💬 "Valeu cada centavo investido"  
    <br><br>— Loja online
    </div>
    """, unsafe_allow_html=True)

st.divider()

# =========================
# PORTFÓLIO
# =========================
st.header("📁 Projetos recentes")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="box">
    <h4>🛍️ Loja Virtual</h4>
    <p>Site antigo lento → Novo site otimizado</p>
    <p><b>Resultado:</b> +60% vendas</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="box">
    <h4>💼 Site empresarial</h4>
    <p>Sem presença online → Site profissional</p>
    <p><b>Resultado:</b> novos clientes toda semana</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# =========================
# PLANOS
# =========================
st.header("💰 Escolha seu plano")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="box">
    <h3>💡 Básico</h3>
    <p>✔ 1 página<br>✔ Design simples<br>✔ Rápido</p>
    <h2>R$ 500</h2>
    </div>
    """, unsafe_allow_html=True)
    st.button("Começar")

with col2:
    st.markdown("""
    <div class="box">
    <h3>🚀 Profissional</h3>
    <p>✔ Até 5 páginas<br>✔ Design moderno<br>✔ Conversão</p>
    <h2>R$ 1000</h2>
    </div>
    """, unsafe_allow_html=True)
    st.button("Mais escolhido")

with col3:
    st.markdown("""
    <div class="box">
    <h3>🔥 Premium</h3>
    <p>✔ Completo<br>✔ Performance<br>✔ Estratégia</p>
    <h2>R$ 2000</h2>
    </div>
    """, unsafe_allow_html=True)
    st.button("Quero o melhor")

st.divider()

# =========================
# PROCESSO
# =========================
st.header("⚙️ Como funciona")

st.write("""
1. 📋 Briefing  
2. 🧠 Planejamento  
3. 🎨 Design  
4. 💻 Desenvolvimento  
5. 🚀 Entrega  
""")

st.divider()

# =========================
# CTA FINAL
# =========================
st.header("🔥 Pronto para ter um site que vende?")

st.write("Quanto mais você espera, mais clientes perde.")

st.button("🚀 Começar agora")

st.divider()

# =========================
# CONTATO
# =========================
st.header("📞 Contato")

st.write("""
📧 fellipedgtech@gmail.com  
📱 (73) 99994-6196  
""")