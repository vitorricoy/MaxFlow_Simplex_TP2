import numpy as np
from simplex.main import resolverPL

n, m = input().split()
n = int(n)
m = int(m)

capacidades = input().split()
capacidades = list(map(int, capacidades))
matrizIncidencia = []
for i in range(n):
    restricao = input().split()
    restricao = list(map(int, restricao))
    matrizIncidencia.append(restricao)

vetorCusto = [-x for x in matrizIncidencia[0]]
restricoes = []
for linha in matrizIncidencia[1:-1]:
    novaLinha = linha.copy()
    novaLinha.append(0)
    restricoes.append(novaLinha)
    restricoes.append([-x for x in novaLinha])

for i in range(m):
    vetorTemp = np.zeros(m+1)
    vetorTemp[i] = 1
    vetorTemp[-1] = capacidades[i]
    restricoes.append(vetorTemp)

vetorCusto = np.array(vetorCusto)
restricoes = np.array(restricoes)

nRestricoes = len(restricoes)
nVariaveis = m

resolverPL(nRestricoes, nVariaveis, vetorCusto, restricoes)
