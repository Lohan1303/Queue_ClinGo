import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Union, Dict, Optional
import math

class SimuladorFilas:
    def __init__(self, num_servidores: int):
        self.num_servidores = max(1, num_servidores)  # Garantir pelo menos 1 servidor
        self.tempos_chegada = []
        self.tempos_atendimento = []
        self.fila = []
        self.servidores = [0] * num_servidores
        self.dados_carregados = False
        
    def carregar_dados(self, dados: Union[str, pd.DataFrame]):
        """Carrega dados do arquivo CSV ou DataFrame"""
        try:
            if isinstance(dados, str):
                # Se for um caminho de arquivo (string)
                df = pd.read_csv(dados)
            else:
                # Se for um DataFrame
                df = dados.copy()
            
            # Validação dos dados
            if 'tempo_chegada' not in df.columns or 'tempo_atendimento' not in df.columns:
                raise ValueError("O DataFrame deve conter as colunas 'tempo_chegada' e 'tempo_atendimento'")
                
            # Remover valores nulos ou negativos
            df = df.dropna(subset=['tempo_chegada', 'tempo_atendimento'])
            df = df[(df['tempo_chegada'] > 0) & (df['tempo_atendimento'] > 0)]
            
            if df.empty:
                raise ValueError("Não há dados válidos após a filtragem")
                
            self.tempos_chegada = df['tempo_chegada'].values
            self.tempos_atendimento = df['tempo_atendimento'].values
            self.dados_carregados = True
            return True
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            self.dados_carregados = False
            return False
        
    def simular(self) -> dict:
        """Executa a simulação e retorna as métricas"""
        # Verificar se os dados foram carregados
        if not self.dados_carregados or len(self.tempos_chegada) == 0 or len(self.tempos_atendimento) == 0:
            return self._resultados_vazios()

        try:
            # Cálculo das taxas
            lambda_ = 1 / np.mean(self.tempos_chegada)  # Taxa de chegada (clientes por unidade de tempo)
            mu = 1 / np.mean(self.tempos_atendimento)   # Taxa de serviço por servidor
            c = self.num_servidores                     # Número de servidores

            # Intensidade de tráfego do sistema
            rho = lambda_ / (c * mu)  # Utilização por servidor

            # Verificar estabilidade do sistema
            if rho >= 1:
                return self._resultados_sistema_instavel()

            # Cálculo de P0 (Probabilidade do sistema estar vazio)
            sum_val = 0
            for n in range(c):
                sum_val += (lambda_ / mu)**n / math.factorial(n)
            
            # Termo adicional para P0
            term2 = (lambda_ / mu)**c / (math.factorial(c) * (1 - rho))
            P0 = 1 / (sum_val + term2)

            # Probabilidade de espera (Fórmula de Erlang C)
            P_espera = ((lambda_ / mu)**c / (math.factorial(c) * (1 - rho))) * P0
            
            # Número médio de clientes na fila (Lq)
            Lq = P_espera * (lambda_ / mu) * rho / (1 - rho)
            
            # Tempo médio de espera na fila (Wq)
            Wq = Lq / lambda_
            
            # Tempo médio no sistema (W)
            W = Wq + (1 / mu)
            
            # Número médio de clientes no sistema (L)
            L = lambda_ * W
            
            # Utilização do sistema
            utilizacao = lambda_ / (c * mu)
            
            resultados = {
                'P0': P0,                  # Probabilidade do sistema estar vazio
                'P_espera': P_espera,      # Probabilidade de espera
                'Lq': Lq,                  # Número médio na fila
                'Wq': Wq,                  # Tempo médio de espera
                'W': W,                     # Tempo médio no sistema
                'L': L,                     # Número médio no sistema
                'utilizacao': utilizacao,   # Utilização do sistema
                'lambda': lambda_,          # Taxa de chegada
                'mu': mu,                   # Taxa de serviço
                'rho': rho                  # Intensidade de tráfego por servidor
            }
            return resultados
        except Exception as e:
            print(f"Erro na simulação: {e}")
            return self._resultados_vazios()
    
    def _resultados_vazios(self) -> dict:
        """Retorna um dicionário com valores NaN para quando não há dados"""
        return {
            'P0': float('nan'),
            'P_espera': float('nan'),
            'Lq': float('nan'),
            'Wq': float('nan'),
            'W': float('nan'),
            'L': float('nan'),
            'utilizacao': float('nan'),
            'lambda': float('nan'),
            'mu': float('nan'),
            'rho': float('nan')
        }
    
    def _resultados_sistema_instavel(self) -> dict:
        """Retorna resultados para um sistema instável (rho >= 1)"""
        return {
            'P0': 0,                 # Sistema nunca está vazio
            'P_espera': 1,           # Sempre há espera
            'Lq': float('inf'),      # Fila infinita
            'Wq': float('inf'),      # Tempo de espera infinito
            'W': float('inf'),       # Tempo no sistema infinito
            'L': float('inf'),       # Número no sistema infinito
            'utilizacao': 1,         # Utilização total
            'lambda': 1 / np.mean(self.tempos_chegada),
            'mu': 1 / np.mean(self.tempos_atendimento),
            'rho': float('inf')      # Intensidade de tráfego infinita
        }
    
    def gerar_graficos(self):
        """Gera visualizações da simulação"""
        if not self.dados_carregados:
            return None
            
        # Implementação básica de gráficos
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Histograma dos tempos de chegada
        ax1.hist(self.tempos_chegada, bins=15, alpha=0.7, color='blue')
        ax1.set_title('Distribuição dos Tempos entre Chegadas')
        ax1.set_xlabel('Tempo (unidades)')
        ax1.set_ylabel('Frequência')
        
        # Histograma dos tempos de atendimento
        ax2.hist(self.tempos_atendimento, bins=15, alpha=0.7, color='green')
        ax2.set_title('Distribuição dos Tempos de Atendimento')
        ax2.set_xlabel('Tempo (unidades)')
        ax2.set_ylabel('Frequência')
        
        plt.tight_layout()
        return fig