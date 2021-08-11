# -*- coding: utf-8 -*-

import numpy as np

def pivotearElemento(tableau, linha, coluna):
    # Normaliza a linha para que o elemento pivoteado seja igual a 1
    tableau[linha, :]/=tableau[linha, coluna]
    # Transforma todas as entradas na mesma coluna do elemento pivoteado, 
    # com exceção do próprio elemento, em 0
    for l in range(len(tableau)):
        if l != linha:
            tableau[l, :] -= tableau[l, coluna]*tableau[linha, :]
    return tableau

def igual(valor1, valor2):
    # Verifica se dois valores são iguais, considerando precisão padrão do numpy.isclose
    return np.all(np.isclose(valor1, valor2))

def maiorIgual(valor1, valor2):
    # Verifica se o primeiro valor é maior ou igual ao segundo, considerando precisão padrão do numpy.isclose
    return np.all(valor1 > valor2) or np.all(np.isclose(valor1, valor2))

def menor(valor1, valor2):
    # Verifica se o primeiro valor é menor que o segundo, considerando precisão padrão do numpy.isclose
    return np.all(valor1 < valor2) and not np.all(np.isclose(valor1, valor2))

def maior(valor1, valor2):
    # Verifica se o primeiro valor é maior que o segundo, considerando precisão padrão do numpy.isclose
    return np.all(valor1 > valor2) and not np.all(np.isclose(valor1, valor2))

def menorIgual(valor1, valor2):
    # Verifica se o primeiro valor é menor ou igual ao segundo, considerando precisão padrão do numpy.isclose
    return np.all(valor1 < valor2) or np.all(np.isclose(valor1, valor2))
