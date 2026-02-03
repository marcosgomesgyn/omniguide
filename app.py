import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd

# CONFIGURAÇÃO INICIAL
st.set_page_config(page_title="Vozia - MiraIA", layout="wide")

if 'agenda' not in st.session_state:
    st.session_state.agenda = pd.DataFrame(columns=['Hora/Data', 'Tarefa/Evento', 'Status'])

st.title("🚀 Omni Digital - Vozia/MiraIA")

# Barra lateral para a API Key
api_key = st.sidebar.text_input("Cole sua NOVA API Key aqui:", type="password")

if api_key:
    try:
        # Configuração da API - Versão mais simples possível
        genai.configure(api_key=api_key)
        
        # Definindo o modelo (sem prefixos extras)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # --- ÁREA DE COMANDO ---
        st.subheader("🎤 O que o Omni deve fazer?")
        comando = st.text_input("Comando:", value="Agendar live no Instagram quarta às 19h")
        arquivo = st.file_uploader("Suba um Print ou Foto", type=['png', 'jpg', 'jpeg'])
        
        if st.button("Executar Comando"):
            if not comando:
                st.warning("Por favor, digite um comando.")
            else:
                with st.spinner("O Omni está processando..."):
                    # Preparando a lista de conteúdo para o Gemini
                    conteudo = [f"Aja como o assistente Vozia. O usuário quer: {comando}"]
                    if arquivo:
                        img = Image.open(arquivo)
                        conteudo.append(img)
                    
                    # CHAMADA PURA: Sem transport, sem api_version, sem nada que dê erro
                    response = model.generate_content(conteudo)
                    
                    if response.text:
                        st.success(f"Resposta do Omni: {response.text}")
                        # Adiciona na tabela de agenda
                        nova_linha = pd.DataFrame([{'Hora/Data': 'Confirmar', 'Tarefa/Evento': comando, 'Status': 'Novo'}])
                        st.session_state.agenda = pd.concat([st.session_state.agenda, nova_linha], ignore_index=True)

        # AGENDA INTERATIVA (Edição e Exclusão)
        st.divider()
        st.subheader("📝 Registros e Agenda")
        st.session_state.agenda = st.data_editor(st.session_state.agenda, num_rows="dynamic", use_container_width=True)

    except Exception as e:
        # Se o 404 voltar aqui, vamos saber que é a conta e não o código
        st.error(f"Erro de conexão: {e}")

else:
    st.info("Aguardando a API Key na barra lateral para iniciar...")
