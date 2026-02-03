import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Vozia - MiraIA", layout="wide")

# 2. INICIALIZAÇÃO DA AGENDA (Onde o "piti" começou, agora protegido)
if 'agenda' not in st.session_state:
    st.session_state.agenda = pd.DataFrame(columns=['Hora/Data', 'Tarefa/Evento', 'Status'])

st.title("🚀 Omni Digital - Vozia/MiraIA")

# 3. BARRA LATERAL
api_key = st.sidebar.text_input("Cole sua NOVA API Key aqui:", type="password")

if api_key:
    try:
        # Configuração pura da API
        genai.configure(api_key=api_key)
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
                    # Preparando a conversa
                    conteudo = [f"Aja como o assistente Vozia. O usuário quer: {comando}"]
                    if arquivo:
                        img = Image.open(arquivo)
                        conteudo.append(img)
                    
                    # Chamada simples (sem transport ou api_version para não dar erro)
                    response = model.generate_content(conteudo)
                    
                    if response.text:
                        st.success(f"Resposta do Omni: {response.text}")
                        # Adiciona automaticamente na tabela abaixo
                        nova_linha = pd.DataFrame([{'Hora/Data': 'Confirmar', 'Tarefa/Evento': comando, 'Status': 'Novo'}])
                        st.session_state.agenda = pd.concat([st.session_state.agenda, nova_linha], ignore_index=True)

        # 4. AGENDA INTERATIVA (O diferencial do seu App!)
        st.divider()
        st.subheader("📝 Registros e Agenda")
        st.session_state.agenda = st.data_editor(
            st.session_state.agenda, 
            num_rows="dynamic", 
            use_container_width=True
        )

    except Exception as e:
        st.error(f"Erro: {e}")
        st.info("Dica: Se o erro 404 persistir por alguns minutos, o Google ainda está ativando sua chave nova.")

else:
    st.info("Aguardando a API Key para começar.")
