import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from typing import Tuple, Dict, List, Optional

class AnalisadorEstatistico:
    def __init__(self, dados: pd.DataFrame):
        # Fazer uma cópia para não modificar o DataFrame original
        self.dados = dados.copy()
        self._validar_dados()
        
    def _validar_dados(self):
        """Valida os dados de entrada e trata valores ausentes ou inválidos"""
        # Remover valores nulos ou negativos
        self.dados = self.dados.dropna()
        for coluna in self.dados.columns:
            self.dados = self.dados[self.dados[coluna] > 0]
        
    def calcular_estatisticas_descritivas(self) -> dict:
        """Calcula estatísticas descritivas dos tempos"""
        if self.dados.empty:
            return {col: {stat: float('nan') for stat in ['media', 'mediana', 'moda', 'variancia', 'desvio_padrao', 
                                                         'min', 'max', 'amplitude', 'coef_variacao']} 
                    for col in self.dados.columns}
        
        estatisticas = {}
        for coluna in self.dados.columns:
            # Converter para lista para garantir cálculos corretos
            valores = self.dados[coluna].tolist()
            
            # Cálculos básicos usando métodos nativos do Python
            media = sum(valores) / len(valores)
            valores_ordenados = sorted(valores)
            n = len(valores)
            
            # Cálculo da mediana
            if n % 2 == 0:
                mediana = (valores_ordenados[n//2 - 1] + valores_ordenados[n//2]) / 2
            else:
                mediana = valores_ordenados[n//2]
            
            # Cálculo da moda
            contagem = {}
            for valor in valores:
                contagem[valor] = contagem.get(valor, 0) + 1
            max_contagem = max(contagem.values())
            moda = [k for k, v in contagem.items() if v == max_contagem][0]
            
            # Cálculo da variância e desvio padrão
            variancia = sum((x - media) ** 2 for x in valores) / (len(valores) - 1)  # Variância amostral
            desvio_padrao = variancia ** 0.5
            
            estatisticas[coluna] = {
                'media': media,
                'mediana': mediana,
                'moda': moda,
                'variancia': variancia,
                'desvio_padrao': desvio_padrao,
                'min': min(valores),
                'max': max(valores),
                'amplitude': max(valores) - min(valores),
                'coef_variacao': (desvio_padrao / media) * 100 if media > 0 else float('nan')  # CV em percentual
            }
        return estatisticas
    
    def calcular_intervalo_confianca(self, coluna: str, confianca: float = 0.95) -> Tuple[float, float]:
        """Calcula intervalo de confiança para uma coluna usando distribuição t-Student"""
        if coluna not in self.dados.columns or self.dados.empty:
            return (float('nan'), float('nan'))
            
        # Converter para lista
        dados = self.dados[coluna].tolist()
        if len(dados) < 2:  # Precisa de pelo menos 2 pontos para calcular o intervalo
            return (float('nan'), float('nan'))
            
        # Cálculos usando métodos nativos do Python
        n = len(dados)
        media = sum(dados) / n
        variancia = sum((x - media) ** 2 for x in dados) / (n - 1)
        desvio_padrao = variancia ** 0.5
        erro_padrao = desvio_padrao / (n ** 0.5)
        
        # Valor crítico da distribuição t
        t_crit = stats.t.ppf((1 + confianca) / 2, n - 1)
        
        # Margem de erro
        margem_erro = t_crit * erro_padrao
        
        return (media - margem_erro, media + margem_erro)
    
    def testar_normalidade(self, coluna: str) -> Dict[str, float]:
        """Testa se os dados seguem uma distribuição normal usando múltiplos testes"""
        if coluna not in self.dados.columns or self.dados.empty:
            return {'shapiro_p': float('nan'), 'ks_p': float('nan')}
            
        dados = self.dados[coluna].dropna().tolist()
        if len(dados) < 3:  # Precisa de pelo menos 3 pontos para os testes
            return {'shapiro_p': float('nan'), 'ks_p': float('nan')}
        
        # Teste de Shapiro-Wilk (melhor para amostras pequenas)
        shapiro_stat, shapiro_p = stats.shapiro(dados)
        
        # Teste de Kolmogorov-Smirnov
        ks_stat, ks_p = stats.kstest(dados, 'norm', args=(sum(dados)/len(dados), 
                                                         (sum((x - sum(dados)/len(dados)) ** 2 for x in dados) / (len(dados) - 1)) ** 0.5))
        
        return {
            'shapiro_p': shapiro_p,
            'ks_p': ks_p,
            'e_normal': shapiro_p > 0.05 and ks_p > 0.05  # Consideramos normal se ambos os p-valores > 0.05
        }
    
    def calcular_correlacao(self) -> Optional[float]:
        """Calcula a correlação entre as colunas do DataFrame"""
        if len(self.dados.columns) < 2 or self.dados.empty:
            return None
            
        # Assumindo que queremos a correlação entre as duas primeiras colunas
        col1, col2 = self.dados.columns[0], self.dados.columns[1]
        
        # Converter para listas
        x = self.dados[col1].tolist()
        y = self.dados[col2].tolist()
        
        # Cálculo da correlação de Pearson
        n = len(x)
        media_x = sum(x) / n
        media_y = sum(y) / n
        
        # Cálculo da covariância
        cov = sum((x[i] - media_x) * (y[i] - media_y) for i in range(n)) / (n - 1)
        
        # Cálculo dos desvios padrão
        std_x = (sum((val - media_x) ** 2 for val in x) / (n - 1)) ** 0.5
        std_y = (sum((val - media_y) ** 2 for val in y) / (n - 1)) ** 0.5
        
        # Correlação de Pearson
        if std_x > 0 and std_y > 0:
            return cov / (std_x * std_y)
        else:
            return 0.0