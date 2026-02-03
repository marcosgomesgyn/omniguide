import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd

# CONFIGURAÇÃO INICIAL
st.set_page_config(page_title="Vozia - MiraIA", layout="wide")

if 'agenda' not in st.session_state:
    st.session_state.agenda = pd.DataFrame(columns=['Hora/Data', 'Tarefa/Evento', 'Status'])

st.title("🚀 Omni Digital - Vozia/MiraIA")

api_key = st.sidebar.text_input("Cole sua API Key aqui:", type="password")

if api_key:
    try:

        # Em vez de apenas definir o modelo, vamos forçar a configuração da API
        genai.configure(api_key=api_key)

        # Tente trocar a linha do modelo por esta:
        model = genai.GenerativeModel(model_name='gemini-1.5-flash')        
   
        # --- ÁREA DE TESTE ---
        st.subheader("🎤 O que o Omni deve fazer?")
        comando = st.text_input("Comando:", value="Agendar live no Instagram quarta às 19h")
        arquivo = st.file_uploader("Suba um Print ou Foto", type=['png', 'jpg', 'jpeg'])
        
        if st.button("Executar Comando"):
            with st.spinner("O Omni está processando..."):
                # Criando o conteúdo para envio
                conteudo = [f"Aja como o assistente Vozia. O usuário quer: {comando}"]
                if arquivo:
                    img = Image.open(arquivo)
                    conteudo.append(img)
                
                # Chamada da geração
                response = model.generate_content(conteudo)
                
                if response.text:
                    st.success(f"Resposta: {response.text}")
                    nova_linha = pd.DataFrame([{'Hora/Data': 'Confirmar', 'Tarefa/Evento': comando, 'Status': 'Novo'}])
                    st.session_state.agenda = pd.concat([st.session_state.agenda, nova_linha], ignore_index=True)

        # AGENDA INTERATIVA (Onde você edita e exclui como no Studio)
        st.divider()
        st.subheader("📝 Registros e Agenda")
        st.session_state.agenda = st.data_editor(st.session_state.agenda, num_rows="dynamic", use_container_width=True)

    except Exception as e:
        # Se o erro 404 persistir, vamos capturar o log detalhado aqui
        st.error(f"Erro de conexão: {e}")
        st.info("Dica: Verifique se sua API Key no Google AI Studio tem permissão para o modelo Gemini 1.5 Flash.")
