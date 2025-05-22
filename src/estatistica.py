import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from typing import Tuple, Dict

class AnalisadorEstatistico:
    def __init__(self, dados: pd.DataFrame):
        self.dados = dados
        
    def calcular_estatisticas_descritivas(self) -> dict:
        """Calcula estatísticas descritivas dos tempos"""
        estatisticas = {}
        for coluna in self.dados.columns:
            estatisticas[coluna] = {
                'media': self.dados[coluna].mean(),
                'mediana': self.dados[coluna].median(),
                'moda': self.dados[coluna].mode().iloc[0],
                'variancia': self.dados[coluna].var(),
                'desvio_padrao': self.dados[coluna].std()
            }
        return estatisticas
    
    def calcular_intervalo_confianca(self, coluna: str, confianca: float = 0.95) -> Tuple[float, float]:
        """Calcula intervalo de confiança para uma coluna"""
        dados = self.dados[coluna]
        ic = stats.t.interval(confianca, len(dados)-1, loc=dados.mean(), scale=stats.sem(dados))
        return ic