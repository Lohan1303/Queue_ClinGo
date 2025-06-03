# 🏥 Sistema de Simulação de Filas - Clínica Médica 📊

Este projeto é um sistema interativo para simular o comportamento de filas em uma clínica médica, permitindo a análise de tempos de chegada e atendimento de pacientes. A aplicação oferece funcionalidades para configurar o número de servidores, carregar dados de exemplo ou personalizados, executar simulações, analisar estatísticas descritivas e visualizar os resultados através de gráficos.

## ✨ Funcionalidades

*   **Simulação de Filas:** 📈 Simula o fluxo de pacientes em uma clínica, calculando métricas importantes como probabilidade de sistema vazio, tempo médio de espera, número médio na fila, probabilidade de espera, tempo médio no sistema e número médio no sistema.
*   **Análise Estatística Descritiva:** 🔬 Calcula e exibe estatísticas descritivas para os tempos de chegada e atendimento, incluindo média, mediana, moda, variância, desvio padrão, mínimo, máximo, amplitude e coeficiente de variação.
*   **Intervalos de Confiança:** 📊 Calcula intervalos de confiança para as métricas de tempo de chegada e atendimento.
*   **Visualizações Gráficas:** 📉 Apresenta histogramas, boxplots, gráficos de tempo de espera por cliente, tamanho da fila ao longo do tempo e tempo de ocupação dos servidores para uma compreensão visual dos dados e resultados da simulação.
*   **Exportação de Dados:** 📥 Permite exportar as estatísticas descritivas e os resultados da simulação para arquivos CSV, com separador `;` e vírgula como decimal, facilitando a análise externa.
*   **Carregamento de Dados Flexível:** 📂 Suporta o carregamento de arquivos CSV personalizados ou a utilização de arquivos de exemplo pré-definidos.

## 🚀 Como Executar

Para rodar a aplicação, siga os passos abaixo:

1.  **Pré-requisitos:** Certifique-se de ter o Python instalado (versão 3.7 ou superior é recomendada).

2.  **Instalar Dependências:** Navegue até o diretório raiz do projeto (`Queue_ClinGo`) no seu terminal e instale todas as bibliotecas necessárias. É altamente recomendado usar um ambiente virtual para gerenciar as dependências do projeto.

    ```bash
    # Opcional: Criar e ativar um ambiente virtual
    python -m venv venv
    # No Windows
    .\venv\Scripts\activate
    # No macOS/Linux
    source venv/bin/activate
    
    # Instalar as bibliotecas
    pip install streamlit pandas matplotlib numpy seaborn scipy
    ```

3.  **Executar a Aplicação:** Após a instalação das dependências, execute o aplicativo Streamlit a partir do diretório raiz do projeto:
    ```bash
    streamlit run src/interface.py
    ```
    Isso abrirá a aplicação no seu navegador padrão.

## 📁 Estrutura do Projeto

*   `src/`: Contém os arquivos de código-fonte principais.
    *   `interface.py`: O arquivo principal da aplicação Streamlit, responsável pela interface do usuário e orquestração das funcionalidades.
    *   `simulacao.py`: Contém a lógica para a simulação de filas.
    *   `estatistica.py`: Contém as funções para análise estatística.
*   `data/`: Contém arquivos CSV de exemplo (`input.csv`, `input2.csv`) para testes e demonstração.
*   `README.md`: Este arquivo, fornecendo uma visão geral do projeto.

## 🛠️ Tecnologias Utilizadas

*   Python
*   Streamlit
*   Pandas
*   Matplotlib
*   NumPy
*   Seaborn
*   SciPy

## 🧑‍💻 Autores

*   Guilherme Garcia [![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/guigarciag)
*   Lohan Batista [![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Lohan1303)
*   Paulo Henrique Tristão [![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/PauloTristao)
*   Rodrigo Puertas [![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/RodrigoPuertas)
