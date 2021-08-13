import numpy as np
from simplex.main import resolverPL
import simplex.constantes as constantes

n, m = input().split()
n = int(n)
m = int(m)

capacidades = input().split()
capacidades = list(map(int, capacidades))
matrizIncidencia = []
for i in range(n):
    linhaMatriz = input().split()
    linhaMatriz = list(map(int, linhaMatriz))
    matrizIncidencia.append(linhaMatriz)

matrizIncidencia = np.array(matrizIncidencia)

vetorCusto = [0 for _ in range(2*(n-2))]
vetorCusto.extend(capacidades.copy())
vetorCusto = np.negative(np.array(vetorCusto))

restricoes = []
for linha in matrizIncidencia[1:-1].T:
    novaLinha = []
    for elemento in linha:
        novaLinha.append(-elemento)
        novaLinha.append(elemento)
    restricoes.append(novaLinha)

restricoes = np.array(restricoes)

# Adiciona a matriz identidade na lateral
restricoes = np.concatenate((restricoes, np.negative(np.identity(m))), axis = 1)

# Adiciona o vetor b na lateral da matriz de restrições
vetorB = np.array([matrizIncidencia[0]]).T
restricoes = np.concatenate((restricoes, vetorB), axis = 1)

nRestricoes = len(restricoes)
nVariaveis = len(vetorCusto)

resultado = resolverPL(nRestricoes, nVariaveis, vetorCusto, restricoes)

if resultado[0] != constantes.OTIMA:
    raise 'PL gerada não tem valor ótimo. Erro!'
else:
    msgOtima, valorOtimo, solucao, certificado = resultado
    # Tratar solução com variáveis livres
    solucaoReal = []
    for ind in range(0, 2*(n-2), 2):
        if ind < 2*(n-2):
            solucaoReal.append(solucao[ind]-solucao[ind+1])
            ind+=1
    for ind in range(2*(n-2), len(solucao)):
        solucaoReal.append(solucao[ind])
    print(-int(round(valorOtimo)))
    for el in certificado:
        print(int(round(el)), end=' ')
    print()
    print(1, end = ' ')
    for el in solucaoReal[:n-2]:
        print(int(round(el)>=1), end=' ')
    print(0)
