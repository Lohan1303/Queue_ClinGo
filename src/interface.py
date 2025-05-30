import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from simulacao import SimuladorFilas
from estatistica import AnalisadorEstatistico

def criar_sidebar():
    st.sidebar.title("Configurações")
    num_servidores = st.sidebar.slider("Número de Servidores", 1, 10, 3)
    nivel_confianca = st.sidebar.slider("Nível de Confiança", 0.8, 0.99, 0.95)
    
    # Adicionar opção para selecionar arquivo de exemplo
    arquivo_exemplo = st.sidebar.selectbox(
        "Selecionar arquivo de exemplo",
        ["Nenhum", "input.csv", "input2.csv"]
    )
    
    return num_servidores, nivel_confianca, arquivo_exemplo

def main():
    st.title("Sistema de Simulação de Filas - Clínica Médica")
    
    # Configurações na barra lateral
    num_servidores, nivel_confianca, arquivo_exemplo = criar_sidebar()
    
    # Upload de arquivo
    uploaded_file = st.file_uploader("Carregar arquivo CSV com dados", type=['csv'])
    
    dados_df = None
    
    # Verificar se um arquivo de exemplo foi selecionado
    if arquivo_exemplo != "Nenhum":
        caminho_arquivo = f"C:\\Users\\lobat_1o2ktb6\\OneDrive\\Área de Trabalho\\Queue_ClinGo\\data\\{arquivo_exemplo}"
        dados_df = pd.read_csv(caminho_arquivo)
        st.success(f"Arquivo de exemplo '{arquivo_exemplo}' carregado com sucesso!")
    
    # Se um arquivo foi carregado pelo uploader, ele tem prioridade
    if uploaded_file is not None:
        try:
            print("\n[LOG] Arquivo carregado pelo usuário:")
            print(f"[LOG] Nome do arquivo: {uploaded_file.name}")
            
            dados_df = pd.read_csv(uploaded_file) # Ler o CSV para DataFrame aqui
            print("[LOG] Dados carregados do CSV:")
            print(dados_df.head())
            print(f"[LOG] Dimensões do DataFrame: {dados_df.shape}")
            
            # Verificar se o DataFrame não está vazio e tem as colunas esperadas
            if dados_df.empty:
                st.error("O arquivo CSV está vazio.")
                print("[LOG] ERRO: O arquivo CSV está vazio.")
                return
            if not {'tempo_chegada', 'tempo_atendimento'}.issubset(dados_df.columns):
                st.error("O arquivo CSV deve conter as colunas 'tempo_chegada' e 'tempo_atendimento'.")
                print("[LOG] ERRO: Colunas necessárias não encontradas.")
                print(f"[LOG] Colunas encontradas: {dados_df.columns.tolist()}")
                return

        except pd.errors.EmptyDataError:
            st.error("Erro ao ler o arquivo CSV: Nenhuma coluna para analisar. Verifique o formato do arquivo.")
            print("[LOG] ERRO: Arquivo CSV vazio ou mal formatado.")
            return
        except Exception as e:
            st.error(f"Erro ao processar o arquivo CSV: {e}")
            print(f"[LOG] ERRO ao processar o arquivo CSV: {e}")
            return

        # Tabs para organizar o conteúdo
        tab1, tab2, tab3 = st.tabs(["Simulação", "Estatísticas", "Visualizações"])
        
        with tab1:
            st.header("Simulação da Fila")
            if st.button("Executar Simulação"):
                simulador = SimuladorFilas(num_servidores)
                simulador.carregar_dados(dados_df) # Passar o DataFrame
                resultados = simulador.simular()
                
                # Exibir resultados
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Probabilidade Sistema Vazio", f"{resultados['P0']:.2%}")
                    st.metric("Tempo Médio de Espera", f"{resultados['Wq']:.2f} min")
                    st.metric("Número Médio na Fila", f"{resultados['Lq']:.2f}")
                with col2:
                    st.metric("Probabilidade de Espera", f"{resultados['P_espera']:.2%}")
                    st.metric("Tempo Médio no Sistema", f"{resultados['W']:.2f} min")
                    st.metric("Número Médio no Sistema", f"{resultados['L']:.2f}")
        
        with tab2:
            st.header("Análise Estatística")
            print("\n[LOG] Iniciando análise estatística")
            analisador = AnalisadorEstatistico(dados_df) # Passar o DataFrame
            estatisticas = analisador.calcular_estatisticas_descritivas()
            
            print("\n[LOG] Estatísticas calculadas:")
            print(estatisticas)
            
            st.subheader("Estatísticas Descritivas")
            st.dataframe(pd.DataFrame(estatisticas))
            
            st.subheader("Intervalos de Confiança")
            # Corrigindo o problema - garantindo que estamos iterando sobre uma lista de strings
            colunas = list(dados_df.columns)
            for coluna in colunas:
                ic = analisador.calcular_intervalo_confianca(coluna, nivel_confianca)
                st.write(f"{coluna}: [{ic[0]:.2f}, {ic[1]:.2f}]")
        
        with tab3:
            st.header("Visualizações")
            
            # Histogramas
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
            ax1.hist(dados_df['tempo_chegada'], bins=20, color='skyblue', edgecolor='black')
            ax1.set_title('Distribuição dos Tempos de Chegada')
            ax1.set_xlabel('Tempo entre Chegadas (min)')
            ax1.set_ylabel('Frequência')

            ax2.hist(dados_df['tempo_atendimento'], bins=20, color='lightcoral', edgecolor='black')
            ax2.set_title('Distribuição dos Tempos de Atendimento')
            ax2.set_xlabel('Tempo de Atendimento (min)')
            ax2.set_ylabel('Frequência')
            st.pyplot(fig)
            
            # Boxplot
            fig2, ax = plt.subplots(figsize=(8, 4))
            dados_df.boxplot(column=['tempo_chegada', 'tempo_atendimento'], ax=ax, patch_artist=True)
            ax.set_title('Comparação dos Tempos de Chegada e Atendimento')
            ax.set_ylabel('Tempo (min)')
            st.pyplot(fig2)

if __name__ == "__main__":
    st.set_page_config(
        page_title="Simulador de Filas - Clínica Médica",
        page_icon="🏥",
        layout="wide"
    )
    main()