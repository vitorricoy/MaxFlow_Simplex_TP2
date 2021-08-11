# -*- coding: utf-8 -*-

import numpy as np
from . import constantes
from . import util

def exibirSaidaOtima(tableau, n, m):
    # Obtém o certificado de ótima a partir do tableau
    certificadoOtima = tableau[0, 0:n]

    # Inicializa o vetor de solução com zeros
    solucao = np.zeros(m)

    # Salvas as linhas que já atribuímos uma solução
    variavelBasicaLinha = []

    # Percorre as colunas das variáveis originais da PL
    for c in range(m):
        # Se a coluna tem o vetor c igual a 0 no tableau
        if util.igual(tableau[0, n+c], 0):
            # Verifica se a coluna possui apenas um elemento diferente de zero
            if np.count_nonzero(tableau[1:, n+c]) == 1:
                # Percorre as linhas de restrições do tableau
                for l in range(n):
                    if l not in variavelBasicaLinha:
                        # Se o elemento diferente de zero da coluna é 1
                        # Essa coluna é uma coluna básica
                        if util.igual(tableau[l+1, n+c], 1):
                            # Salva que já achamos a variável básica da linha
                            variavelBasicaLinha.append(l)
                            # Salva o valor da variável básica correspondente à coluna
                            # como solução
                            solucao[c] = tableau[l+1, -1]
    
    # Obtém o valor objetivo ótimo a partir do tableau
    valorOtimo = tableau[0, -1]

    # Imprime o resultado no formato pedido
    print('otima')
    print("{:.7f}".format(valorOtimo), end = ' ')
    print()
    for el in solucao:
        print("{:.7f}".format(el), end = ' ')
    print()
    for el in certificadoOtima:
        print("{:.7f}".format(el), end = ' ')
    print()

def exibirSaidaIlimitada(tableau, n, m):
    # Procura o índice da coluna que gera o certificado de ilimitada
    # Inicialmente o índice é -1 (desconhecido)
    colunaIlimitada = -1

    # Percorre as colunas das variáveis originais e de folga da PL
    for c in range(m+n):
        # Se a entrada do vetor c da coluna é negativa
        if util.menor(tableau[0, n+c], 0):
            # Conta os elementos não positivos na coluna
            naoPositivos = 0
            for el in tableau[1:, n+c]:
            	if util.menorIgual(el, 0):
            	    naoPositivos+=1
            # Se todos os elementos são não negativos, a coluna gera
            # o certificado de ilimitada
            if naoPositivos == n:
                # Salva o índice da coluna
                colunaIlimitada = n+c
                break
    # Inicializa o certificado de ilimitada com zeros
    certificadoIlimitada = np.zeros(m+n)
    # Inicializa a solução com zeros
    solucao = np.zeros(m)
    # Salvas as linhas que já atribuímos uma solução
    variavelBasicaLinha = []
    # Percorre as variáveis originais e de folga
    for c in range(m+n):
        # Se a coluna tem o vetor c igual a 0 no tableau
        if util.igual(tableau[0, n+c], 0):
            # Verifica se a coluna possui apenas um elemento diferente de zero
            if np.count_nonzero(tableau[1:, n+c]) == 1:
                # Percorre as linhas de restrições do tableau
                for l in range(n):
                    if l not in variavelBasicaLinha:
                        # Se o elemento diferente de zero da coluna é 1
                        # Essa coluna é uma coluna básica
                        if util.igual(tableau[l+1, n+c], 1):
                            # Salva que já achamos a variável básica da linha
                            variavelBasicaLinha.append(l)
                            # Salva o valor dessa coluna no certificado de ilimitabilidade
                            certificadoIlimitada[c] = -tableau[l+1, colunaIlimitada]
                            # Se a coluna é de uma variável original
                            if c < m:
                                # Salva o valor da solução viável para essa variável
                                solucao[c] = tableau[l+1, -1]
    
    certificadoIlimitada[colunaIlimitada-n] = 1
    # Imprime o resultado no formato pedido
    print('ilimitada')
    for el in solucao:
        print("{:.7f}".format(el), end = ' ')
    print()
    for el in certificadoIlimitada:
        print("{:.7f}".format(el), end = ' ')
    print()

def exibirSaidaInviavel(tableau, n):
    # Obtém o certificado de inviabilidade a partir do tableau da PL auxiliar
    certificadoInviabilidade = tableau[0, 0:n]

    # Imprime o resultado no formato pedido
    print('inviavel')
    for el in certificadoInviabilidade:
        print("{:.7f}".format(el), end = ' ')
    print()

def saidaSimplex(resultado, tableau, n, m):
    if resultado == constantes.OTIMA:
        exibirSaidaOtima(tableau, n, m)
    else:
        if resultado == constantes.ILIMITADA:
            exibirSaidaIlimitada(tableau, n, m)
        else:
            exibirSaidaInviavel(tableau, n)
