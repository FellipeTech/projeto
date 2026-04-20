import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Dev Freelancer",
    page_icon="🚀",
    layout="wide"
)

# HERO
st.title("🚀 Transformo ideias em sites que vendem")
st.subheader("Desenvolvimento de sites rápidos, modernos e otimizados para conversão")

col1, col2 = st.columns(2)

with col1:
    if st.button("💬 Falar comigo"):
        whatsapp_url = "https://wa.me/5573999946196?text=Olá,%20quero%20um%20site%20profissional!"

        st.markdown(f"""
        <a href="{whatsapp_url}" target="_blank">
            <button style="
                background-color:#25D366;
                color:white;
                padding:12px 20px;
                border:none;
                border-radius:8px;
                cursor:pointer;
                font-size:16px;">
                🚀 Solicitar orçamento
            </button>
        </a>
        """, unsafe_allow_html=True)

with col2:
    if st.button("📩 Solicitar orçamento"):
        st.success("Me envie uma mensagem e vamos conversar!")

st.divider()

# SOBRE
st.header("👨‍💻 Sobre mim")
st.write("""
Sou desenvolvedor web focado em criar sites modernos, rápidos e com foco em resultados.

Trabalho com foco em:
- Performance ⚡
- Design estratégico 🎯
- Conversão 💰
""")

# SERVIÇOS
st.header("🛠 Serviços")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🌐 Sites")
    st.write("Criação de sites institucionais profissionais")

with col2:
    st.subheader("📄 Landing Pages")
    st.write("Páginas focadas em conversão")

with col3:
    st.subheader("🛒 E-commerce")
    st.write("Lojas virtuais completas")

st.divider()

# PORTFÓLIO
st.header("📂 Portfólio")
st.info("Em breve você verá projetos incríveis aqui 🚀")

# PROCESSO
st.header("⚙️ Como trabalho")

st.write("""
1. 📋 Briefing  
2. 🧠 Planejamento  
3. 🎨 Design  
4. 💻 Desenvolvimento  
5. 🚀 Entrega  
""")

st.divider()

# CTA FINAL
st.header("🔥 Pronto para ter seu site profissional?")

if st.button("🚀 Começar meu projeto agora"):
    st.success("Clique no WhatsApp e vamos começar!")

st.divider()

# CONTATO
st.header("📞 Contato")

st.write("📧 Email: fpellegrini348@gmail.com")
st.write("📱 WhatsApp: (73) 999946196")