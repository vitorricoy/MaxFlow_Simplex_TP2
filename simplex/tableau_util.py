# -*- coding: utf-8 -*-

from . import util
import numpy as np

def montarTableauFormaCanonica(n, m, restricoes, vetorCusto):
    tableau = np.zeros((n+1, n+m+n+1))
    # Matriz auxiliar do VERO
    tableau[1:, :n] = np.identity(n)
    # Adiciona as restrições
    for indice, restricao in enumerate(restricoes):
        coeficientes = restricao[:-1]
        valorB = restricao[-1]
        tableau[indice+1, n+m+indice] = 1
        tableau[indice+1, n:n+m] = coeficientes
        tableau[indice+1, -1] = valorB
    # Adiciona o objetivo
    tableau[0, n:n+m] = -vetorCusto
    return tableau

def montarTableauAuxiliar(n, m, restricoes, vetorCusto):
    tableau = np.zeros((n+1, n+m+n+n+1))
    # Matriz auxiliar do VERO
    tableau[1:, :n] = np.identity(n)
    # Adiciona as restrições
    for indice, restricao in enumerate(restricoes):
        coeficientes = restricao[:-1]
        valorB = restricao[-1]
        tableau[indice+1, n+m+indice] = 1
        tableau[indice+1, n:n+m] = coeficientes
        tableau[indice+1, -1] = valorB
    # Deixa o vetor b positivo
    for l in range(n):
        if util.menor(tableau[l+1, -1], 0):
            tableau[l+1:] *=-1
    # Adiciona as variaveis auxiliares
    tableau[1:, n+m+n:n+m+n+n] = np.identity(n)
    # Adiciona o objetivo nas variáveis auxiliares
    tableau[0, n+m+n:n+m+n+n] = np.ones(n)
    # Coloca o tableau em formato canônico
    for l in range(n):
        tableau[0][:] -= tableau[l+1][:]
    return tableau

def tratarVariavelAuxiliarBasica(elementosBases, linhasComBase, colunasBasicas, n, m, tableau):
    # Trata o caso em que uma variável auxiliar era básica
    # Isso só acontece se algum valor de b se torna 0
    # Logo, basta pivotear uma coluna não básica para cada variável auxiliar básica
    if len(elementosBases) != n:
        for l in range(n):
            # A linha não tem uma base
            if l+1 not in linhasComBase:
                for c in range(m+n):
                    # A coluna não é básica e não tem o elemento na linha l igual a 0
                    if not util.igual(tableau[l+1, n+c], 0) and n+c not in colunasBasicas:
                        # Salva que a coluna c agora é básica
                        linhasComBase.append(l+1)
                        colunasBasicas.append(n+c)
                        elementosBases.append((l+1, n+c))
                        # Pivoteia o elemento na linha l e coluna c
                        tableau = util.pivotearElemento(tableau, l+1, n+c)
                        break
                        
    return elementosBases

def identificarColunasBasicas(tableau, n, m):
    
    # Inicializa a lista que guarda a posição dos elementos 1
    # das colunas básicas
    elementosBases = []
    
    # Inicializa a lista que guarda as linhas que possuem um elemento igual a 1
    # em uma coluna básica
    linhasComBase = []

    # Inicializa a lista que guarda as colunas básicas
    colunasBasicas = []

    for i in range(m+n):
        # Se a entrada do vetor c do tableau é igual a 0
        if util.igual(tableau[0, n+i], 0): 
            # Se a coluna possui apenas um elemento diferente de 0
            if np.count_nonzero(tableau[1:, n+i]) == 1:
                for j in range(n):
                    # Se o elemento diferente de zero da coluna é igual a 1
                    # Esse elemento está em uma coluna básica
                    if util.igual(tableau[j+1, n+i], 1):
                        # Se já não achamos a base para a linha
                        if j+1 not in linhasComBase:
                            # Salva as informações do elemento
                            elementosBases.append((j+1, n+i))
                            linhasComBase.append(j+1)
                            colunasBasicas.append(n+i)

    # Trata o caso em que uma coluna de uma variavel auxiliar era básica
    elementosBases = tratarVariavelAuxiliarBasica(elementosBases, linhasComBase, colunasBasicas, n, m, tableau)

    # Retorna a posição dos elementos igual a 1 das colunas básicas
    return elementosBases



def converterTableauAuxiliar(tableau, n, m, vetorCusto):
    # Deletar variáveis auxiliares do tableau
    for i in range(n):
        tableau = np.delete(tableau, n+m+n, axis = 1)
    
    # Identifica as colunas bases do tableau
    elementosBases = identificarColunasBasicas(tableau, n, m)
    
    # Coloca o vetor c original no tableau
    tableau[0, n:n+m] = -vetorCusto
    # Zera os valores de c no tableau das variáveis de folga
    tableau[0, n+m:n+n+m] = 0
    # Pivoteia as colunas básicas para que o vetor c do tableau tenha
    # entradas iguais a 0 nessas colunas
    for linha, coluna in elementosBases:
        tableau[0, :] -= tableau[0, coluna]*tableau[linha, :]
    return tableau
