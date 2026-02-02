import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuração básica
st.set_page_config(page_title="Omni Digital", layout="wide")
st.title("🚀 Omni Digital - Vozia/MiraIA")

# Entrada da API Key na barra lateral
api_key = st.sidebar.text_input("Cole sua API Key do Google aqui:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    # Usando o 1.5 Flash que é super estável para Streamlit
    model = genai.GenerativeModel('gemini-1.5-flash') 

    # Espaço da Agenda
    st.subheader("📅 Sua Agenda")
    if 'agenda' not in st.session_state:
        st.session_state.agenda = []
    
    nova_tarefa = st.text_input("Adicionar tarefa manualmente:")
    if st.button("Salvar na Agenda"):
        st.session_state.agenda.append(nova_tarefa)
        st.success("Tarefa salva!")

    for item in st.session_state.agenda:
        st.write(f"✅ {item}")

    # Parte da Visão
    st.divider()
    st.subheader("👁️ Visão da IA")
    img_file = st.camera_input("Capture uma imagem para o Omni analisar")

    if img_file:
        img = Image.open(img_file)
        st.image(img, caption="Imagem capturada")
        with st.spinner("Analisando..."):
            response = model.generate_content(["Descreva esta imagem e veja se há algo para a agenda.", img])
            st.write("### O que o Omni viu:")
            st.write(response.text)
else:
    st.warning("Aguardando API Key para iniciar...")
