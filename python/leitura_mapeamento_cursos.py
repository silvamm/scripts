#import csv
import pandas as pd
data = pd.read_csv('mapeamento-cursos.csv', header= 1)
#print(data['Código'].to_string())
#print(data.to_string())

#print(data['Código'].to_string() )

resultado = {}

def getValor(cabecalho, busca, linha):
    if linha[cabecalho] == busca and linha['Situação'] == 'ATIVO':
        return True
    return False
        
for num_linha, linha in data.iterrows():
    if not linha['Situação'] == 'ATIVO' :
        continue

    descricao = linha['Descrição']
    if not descricao in resultado:
        resultado[descricao] = []
    else:
        lista = resultado[descricao]
        lista.append(linha)
        resultado[descricao] = lista
    #if getValor('Descrição Completa', 'ADMINISTRAÇÃO', linha):
     #   print(linha)
    
print(resultado['ADMINISTRAÇÃO (BACHARELADO)'])