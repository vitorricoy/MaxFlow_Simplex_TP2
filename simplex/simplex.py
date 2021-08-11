# -*- coding: utf-8 -*-

import numpy as np
import math
from . import constantes
from . import util

def verificaIlimitado(tableau, n, m):
    # Valores de c no tableau
    coeficientes = tableau[0, n:n+m]
    colunaPivo = -1
    for c in range(len(coeficientes)):
        # Verifica se o valor de c dessa coluna é negativo
        if util.menor(coeficientes[c], 0):
            # Salva a coluna que será pivoteada, caso ela não tenha sido encontrada ainda
            if colunaPivo == -1:
                colunaPivo = c
                
            # Determina se a PL é ilimitada verificando se a coluna possui apenas números
            # não positivos
            coluna = tableau[1:, n+c]
            achouAlgumPositivo = False
            for l in range(len(coluna)):
                if util.maior(coluna[l], 0):
                    achouAlgumPositivo = True
                    break
            if not achouAlgumPositivo:
                return constantes.ILIMITADA, tableau
    # Continua a execução do simplex, caso a PL não seja ilimitada
    return constantes.PASSO, colunaPivo

def escolheLinhaPivoteamento(tableau, n, m, colunaPivo):
    # Linha do elemento que será pivoteado
    linhaPivo = -1
    # Inicialmente, a razão é infinita, pois devemos encontrar a menor
    valorEscolhido = math.inf
    for l in range(n):
        # Se o elemento da coluna nessa linha for maior que zero
        if util.maior(tableau[l+1, colunaPivo], 0):
            # Calcula a razão entre ele e o valor de b na linha
            razao = tableau[l+1, -1]/tableau[l+1, colunaPivo]
            # Se a razão for a menor, essa linha será pivoteada
            if util.menor(razao, valorEscolhido):
                valorEscolhido = razao
                linhaPivo = l+1
    return linhaPivo

def passoSimplex(tableau, n, m):

    resultado, retorno = verificaIlimitado(tableau, n, m)
    # Se a PL for ilimitada, para o simplex e retorna essa informação
    if resultado == constantes.ILIMITADA:
        return resultado, retorno
    
    # Se a verificação de ilimitada não retornou uma coluna com o
    # valor de c negativo, o tableau está em estado de ótimo
    if retorno == -1:
        return constantes.OTIMA, tableau
    
    # Se a PL não é ilimitada, nem está em estado de ótimo, executa uma
    # iteração do simplex
    colunaPivo = retorno+n

    linhaPivo = escolheLinhaPivoteamento(tableau, n, m, colunaPivo)
    
    # Pivoteia o elemento escolhido pelo algoritmo
    tableau = util.pivotearElemento(tableau, linhaPivo, colunaPivo)
    return constantes.PASSO, tableau

def resolverSimplex(tableau, n, m):
    # Inicializa com necessidade de realizar um passo do simplex
    resultado = constantes.PASSO
    while resultado == constantes.PASSO:
        resultado, tableau = passoSimplex(tableau, n, m)
    return resultado, tableau
