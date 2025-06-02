import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from simulacao import SimuladorFilas
from estatistica import AnalisadorEstatistico
import os

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
        caminho_arquivo = os.path.join(os.path.dirname(__file__), "..", "data", arquivo_exemplo)
        dados_df = pd.read_csv(caminho_arquivo)
        st.success(f"Arquivo de exemplo '{arquivo_exemplo}' carregado com sucesso!")
    
    # Se um arquivo foi carregado pelo uploader, ele tem prioridade
    if uploaded_file is not None:
        try:
            print("\n[LOG] Arquivo carregado pelo usuário:")
            print(f"[LOG] Nome do arquivo: {uploaded_file.name}")
            dados_df = pd.read_csv(uploaded_file)
            print("[LOG] Dados carregados do CSV:")
            print(dados_df.head())
            print(f"[LOG] Dimensões do DataFrame: {dados_df.shape}")
            if dados_df.empty:
                st.error("O arquivo CSV está vazio.")
                print("[LOG] ERRO: O arquivo CSV está vazio.")
                dados_df = None
            if not {'tempo_chegada', 'tempo_atendimento'}.issubset(dados_df.columns):
                st.error("O arquivo CSV deve conter as colunas 'tempo_chegada' e 'tempo_atendimento'.")
                print("[LOG] ERRO: Colunas necessárias não encontradas.")
                print(f"[LOG] Colunas encontradas: {dados_df.columns.tolist()}")
                dados_df = None
        except pd.errors.EmptyDataError:
            st.error("Erro ao ler o arquivo CSV: Nenhuma coluna para analisar. Verifique o formato do arquivo.")
            print("[LOG] ERRO: Arquivo CSV vazio ou mal formatado.")
            dados_df = None
        except Exception as e:
            st.error(f"Erro ao processar o arquivo CSV: {e}")
            print(f"[LOG] ERRO ao processar o arquivo CSV: {e}")
            dados_df = None

    if dados_df is not None:
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
                    st.metric("Tempo Médio de Espera", f"{resultados['Wq']:.3f} min")
                    st.metric("Número Médio na Fila", f"{resultados['Lq']:.3f}")
                with col2:
                    st.metric("Probabilidade de Espera", f"{resultados['P_espera']:.2%}")
                    st.metric("Tempo Médio no Sistema", f"{resultados['W']:.3f} min")
                    st.metric("Número Médio no Sistema", f"{resultados['L']:.3f}")

                # Botão para exportar resultados da simulação
                # Criar um DataFrame a partir do dicionário de resultados
                resultados_df = pd.DataFrame([resultados])
                csv_simulacao_data = resultados_df.to_csv(index=False, sep=';', decimal=',')
                st.download_button(
                    label="Exportar Resultados da Simulação para CSV",
                    data=csv_simulacao_data,
                    file_name="resultados.csv",
                    mime="text/csv",
                )
        
        with tab2:
            st.header("Análise Estatística")
            print("\n[LOG] Iniciando análise estatística")
            analisador = AnalisadorEstatistico(dados_df) # Passar o DataFrame
            estatisticas = analisador.calcular_estatisticas_descritivas()
            
            print("\n[LOG] Estatísticas calculadas:")
            print(estatisticas)
            
            st.subheader("Estatísticas Descritivas")
            st.dataframe(pd.DataFrame(estatisticas))

            # Botão para exportar estatísticas descritivas
            estatisticas_df = pd.DataFrame(estatisticas).reset_index()
            estatisticas_df = estatisticas_df.rename(columns={'index': 'Estatística'})
            csv_data = estatisticas_df.to_csv(index=False, sep=';', decimal=',')
            st.download_button(
                label="Exportar Estatísticas Descritivas para CSV",
                data=csv_data,
                file_name="resultado_estatistica.csv",
                mime="text/csv",
            )
            
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

            # --- NOVOS GRÁFICOS ---
            # graficos = {'hist_chegada_atendimento': fig}

            # 1. Tempo de espera por cliente
            import numpy as np
            tempos_chegada = np.cumsum(dados_df['tempo_chegada'].values)
            tempos_atendimento = dados_df['tempo_atendimento'].values
            inicio_atendimento = np.zeros_like(tempos_chegada)
            fim_atendimento = np.zeros_like(tempos_chegada)
            tempo_espera = np.zeros_like(tempos_chegada)

            # Controle do tempo de liberação de cada servidor
            servidores_fim = np.zeros(num_servidores)

            for i in range(len(tempos_chegada)):
                # Encontra o servidor que ficará livre primeiro
                idx_servidor = np.argmin(servidores_fim)
                inicio_atendimento[i] = max(tempos_chegada[i], servidores_fim[idx_servidor])
                tempo_espera[i] = inicio_atendimento[i] - tempos_chegada[i]
                fim_atendimento[i] = inicio_atendimento[i] + tempos_atendimento[i]
                servidores_fim[idx_servidor] = fim_atendimento[i]

            fig3, ax3 = plt.subplots(figsize=(8, 4))
            ax3.plot(range(1, len(tempo_espera)+1), tempo_espera, marker='o', linestyle='-', color='purple')
            ax3.set_title('Tempo de Espera por Cliente')
            ax3.set_xlabel('Cliente')
            ax3.set_ylabel('Tempo de Espera (min)')
            # graficos['tempo_espera_cliente'] = fig3
            st.pyplot(fig3)
            eventos = []
            for i in range(len(tempos_chegada)):
                eventos.append((tempos_chegada[i], 'chegada'))
                eventos.append((fim_atendimento[i], 'saida'))
            eventos.sort()

            fila_tempo = []
            fila_atual = 0
            tempo_eventos = []
            for tempo, tipo in eventos:
                if tipo == 'chegada':
                    fila_atual += 1
                else:
                    fila_atual -= 1
                tempo_eventos.append(tempo)
                fila_tempo.append(max(fila_atual - num_servidores, 0))  # fila = clientes além dos servidores
                tempo_eventos.append(tempo)
                fila_tempo.append(max(fila_atual - num_servidores, 0))  # fila = clientes além dos servidores

            fig4, ax4 = plt.subplots(figsize=(8, 4))
            ax4.step(tempo_eventos, fila_tempo, where='post', color='orange')
            ax4.set_title('Tamanho da Fila ao Longo do Tempo')
            ax4.set_xlabel('Tempo (min)')
            ax4.set_ylabel('Tamanho da Fila')
            # graficos['fila_ao_longo_tempo'] = fig4
            st.pyplot(fig4)
            ocupacao_servidores = np.zeros(num_servidores)
            servidores_fim = [0] * num_servidores

            for i in range(len(tempos_chegada)):
                # Atribui o cliente ao primeiro servidor livre
                idx_servidor = np.argmin(servidores_fim)
                inicio = max(tempos_chegada[i], servidores_fim[idx_servidor])
                fim = inicio + tempos_atendimento[i]
                ocupacao_servidores[idx_servidor] += tempos_atendimento[i]
                servidores_fim[idx_servidor] = fim

            fig5, ax5 = plt.subplots(figsize=(8, 4))
            ax5.bar(range(1, num_servidores+1), ocupacao_servidores, color='teal')
            ax5.set_title('Tempo de Ocupação dos Servidores')
            ax5.set_xlabel('Servidor')
            ax5.set_ylabel('Tempo Ocupado (min)')
            st.pyplot(fig5)

if __name__ == "__main__":
    st.set_page_config(
        page_title="Simulador de Filas - Clínica Médica",
        page_icon="🏥",
        layout="wide"
    )
    main()
