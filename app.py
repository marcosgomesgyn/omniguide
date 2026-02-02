import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd

st.set_page_config(page_title="Vozia - MiraIA", layout="wide")

# 1. SISTEMA DE MEMÓRIA (Para incluir, editar e excluir)
if 'agenda' not in st.session_state:
    # Criamos a tabela inicial vazia
    st.session_state.agenda = pd.DataFrame(columns=['Hora/Data', 'Tarefa/Evento', 'Status'])

st.title("🚀 Omni Digital - Vozia/MiraIA")

# Barra Lateral
api_key = st.sidebar.text_input("Cole sua API Key aqui:", type="password")

if api_key:
    try:
        # CORREÇÃO DO ERRO: Nome oficial do modelo
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # 2. ÁREA DE COMANDO (Texto ou Imagem/Print)
        st.subheader("🎤 O que o Omni deve fazer?")
        comando = st.text_input("Ex: Agendar reunião amanhã às 15h ou Analisar este erro na tela")
        
        arquivo = st.file_uploader("Suba um Print da tela ou Foto", type=['png', 'jpg', 'jpeg'])
        
        if st.button("Executar Comando"):
            with st.spinner("O Omni está processando..."):
                conteudo = [f"Aja como o assistente Vozia. O usuário quer: {comando}"]
                if arquivo:
                    img = Image.open(arquivo)
                    conteudo.append(img)
                
                response = model.generate_content(conteudo)
                st.info(f"Resposta: {response.text}")
                
                # Lógica simples para incluir na tabela automaticamente
                nova_linha = pd.DataFrame([{'Hora/Data': 'Ver resposta', 'Tarefa/Evento': comando, 'Status': 'Novo'}])
                st.session_state.agenda = pd.concat([st.session_state.agenda, nova_linha], ignore_index=True)

        # 3. A AGENDA INTERATIVA (Onde você edita e exclui)
        st.divider()
        st.subheader("📝 Registros e Agenda")
        st.write("Você pode clicar nas células para **editar** ou selecionar linhas para **excluir**.")
        
        # O data_editor é o que permite a edição e exclusão que você tinha no Studio AI
        st.session_state.agenda = st.data_editor(
            st.session_state.agenda,
            num_rows="dynamic", # Isso permite que você delete ou adicione linhas manualmente
            use_container_width=True
        )

    except Exception as e:
        st.error(f"Erro de conexão: {e}")
else:
    st.warning("Aguardando API Key para ativar o Omni.")
