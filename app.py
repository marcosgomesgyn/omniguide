import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Vozia - MiraIA", layout="centered")

st.title("🚀 Omni Digital - Vozia/MiraIA")

# Barra Lateral para a API Key
st.sidebar.header("Configurações")
api_key = st.sidebar.text_input("Cole sua API Key do Google aqui:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        st.subheader("👁️ Visão da IA")
        
        # Opção para o usuário escolher entre Câmera ou Upload de arquivo
        metodo = st.radio("Como deseja enviar a imagem?", ("Usar Câmera", "Carregar Foto do Computador"))
        
        img_file = None
        
        if metodo == "Usar Câmera":
            img_file = st.camera_input("Tire uma foto para o Omni")
        else:
            img_file = st.file_uploader("Escolha um arquivo de imagem", type=['png', 'jpg', 'jpeg'])

        if img_file:
            img = Image.open(img_file)
            st.image(img, caption="Imagem carregada com sucesso!", use_container_width=True)
            
            with st.spinner("O Omni está analisando sua imagem..."):
                prompt = "Você é o Omni, assistente do projeto Vozia/MiraIA. Analise esta imagem e descreva o que vê."
                response = model.generate_content([prompt, img])
                st.success("✅ Resultado da Análise:")
                st.write(response.text)
                
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
else:
    st.info("Por favor, insira sua API Key na barra lateral para ativar o Omni.")
