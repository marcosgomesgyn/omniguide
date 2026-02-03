import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
from google.generativeai.types import RequestOptions

# CONFIGURAÇÃO INICIAL
st.set_page_config(page_title="Vozia - MiraIA", layout="wide")

if 'agenda' not in st.session_state:
    st.session_state.agenda = pd.DataFrame(columns=['Hora/Data', 'Tarefa/Evento', 'Status'])

st.title("🚀 Omni Digital - Vozia/MiraIA")

api_key = st.sidebar.text_input("Cole sua API Key aqui:", type="password")

if api_key:
    try:
        # CONFIGURAÇÃO DO MODELO
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name='gemini-1.5-flash')
        
        # --- ÁREA DE COMANDO ---
        st.subheader("🎤 O que o Omni deve fazer?")
        comando = st.text_input("Comando:", value="Agendar live no Instagram quarta às 19h")
        arquivo = st.file_uploader("Suba um Print ou Foto", type=['png', 'jpg', 'jpeg'])
        
        if st.button("Executar Comando"):
            with st.spinner("O Omni está processando..."):
                conteudo = [f"Aja como o assistente Vozia. O usuário quer: {comando}"]
                if arquivo:
                    img = Image.open(arquivo)
                    conteudo.append(img)
                
                # Chamada com a trava de segurança para o Plano Gratuito
                response = model.generate_content(
                    conteudo, 
                    request_options=RequestOptions(api_version='v1')
                )
                
                if response.text:
                    st.success(f"Resposta do Omni: {response.text}")
                    # Adiciona automaticamente na tabela abaixo
                    nova_linha = pd.DataFrame([{'Hora/Data': 'Confirmar', 'Tarefa/Evento': comando, 'Status': 'Novo'}])
                    st.session_state.agenda = pd.concat([st.session_state.agenda, nova_linha], ignore_index=True)

        # AGENDA INTERATIVA (Edição e Exclusão)
        st.divider()
        st.subheader("📝 Registros e Agenda")
        st.session_state.agenda = st.data_editor(st.session_state.agenda, num_rows="dynamic", use_container_width=True)

    except Exception as e:
        st.error(f"Erro de conexão: {e}")
        st.info("Dica: Verifique se sua API Key no Google AI Studio tem permissão para o modelo Gemini 1.5 Flash.")
