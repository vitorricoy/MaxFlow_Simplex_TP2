# -*- coding: utf-8 -*-

import numpy as np

def lerEntrada():
    n, m = input().split()
    n = int(n)
    m = int(m)

    vetorCusto = input().split()
    vetorCusto = list(map(int, vetorCusto))

    restricoes = []
    for i in range(n):
        restricao = input().split()
        restricao = list(map(int, restricao))

        restricoes.append(restricao)

    vetorCusto = np.array(vetorCusto)
    restricoes = np.array(restricoes)
    return n, m, vetorCusto, restricoes
