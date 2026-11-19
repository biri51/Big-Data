"""Trabalho Prático DGT2823 — tratamento de dados com Pandas."""
from pathlib import Path
import pandas as pd

ARQUIVO = Path(__file__).with_name('dados.csv')
original = pd.read_csv(ARQUIVO, sep=';', engine='python', encoding='utf-8')
print('=== INFORMAÇÕES DO DATAFRAME ORIGINAL ===')
original.info()
print('\n=== PRIMEIRAS 10 LINHAS ===')
print(original.head(10).to_string(index=False))
print('\n=== ÚLTIMAS 10 LINHAS ===')
print(original.tail(10).to_string(index=False))

tratado = original.copy()
tratado['Calories'] = tratado['Calories'].fillna(0)
print('\n=== CALORIES: NULOS SUBSTITUÍDOS POR ZERO ===')
print(tratado.to_string(index=False))

tratado['Date'] = tratado['Date'].fillna('1900/01/01')
print('\n=== DATE: NULOS SUBSTITUÍDOS POR 1900/01/01 ===')
print(tratado.to_string(index=False))

# O enunciado solicita observar a falha de conversão antes de corrigir os dados.
# As aspas simples que fazem parte dos valores CSV são retiradas primeiro.
tratado['Date'] = tratado['Date'].astype(str).str.strip("'")
try:
    pd.to_datetime(tratado['Date'], format='%Y/%m/%d', errors='raise')
except (ValueError, TypeError) as erro:
    print('\n=== ERRO ESPERADO NA CONVERSÃO INICIAL ===')
    print(erro)

tratado['Date'] = tratado['Date'].replace('1900/01/01', pd.NA)
print('\n=== DATA SENTINELA SUBSTITUÍDA POR NULO ===')
print(tratado.to_string(index=False))

# Converte o valor fora do padrão, 20201226, usando replace e to_datetime.
tratado['Date'] = tratado['Date'].replace(
    {'20201226': pd.to_datetime('20201226', format='%Y%m%d')}
)
# Converte as demais datas preservando o valor datetime já corrigido.
tratado['Date'] = pd.to_datetime(tratado['Date'], format='mixed', errors='raise')
print('\n=== DATAS CONVERTIDAS ===')
print(tratado.to_string(index=False))

tratado = tratado.dropna(subset=['Date']).copy()
tratado.to_csv(Path(__file__).with_name('dados_tratados.csv'), sep=';', index=False,
               date_format='%Y-%m-%d', encoding='utf-8')
print('\n=== DATAFRAME FINAL, SEM DATAS NULAS ===')
print(tratado.to_string(index=False))
print(f'\nRegistros finais: {len(tratado)} (de {len(original)} originais).')
print('Arquivo dados_tratados.csv gerado com sucesso.')
