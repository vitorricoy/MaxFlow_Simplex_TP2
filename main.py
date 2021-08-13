import numpy as np
from simplex.main import resolverPL
import simplex.constantes as constantes

def lerEntrada():
    # Lê os valores de n e m
    n, m = input().split()
    n = int(n)
    m = int(m)

    # Lê a lista de capacidades
    capacidades = input().split()
    capacidades = list(map(int, capacidades))

    # Lê a matriz de incidência
    matrizIncidencia = []
    for i in range(n):
        linhaMatriz = input().split()
        linhaMatriz = list(map(int, linhaMatriz))
        matrizIncidencia.append(linhaMatriz)

    # Converte as listas e listas de listas para arrays do numpy
    matrizIncidencia = np.array(matrizIncidencia)
    capacidades = np.array(capacidades)

    # Retorna os valores lidos
    return n, m, capacidades, matrizIncidencia

def construirVetorCusto(n, capacidades):
    # Preenche o vetor de custo com 0s para as variáveis correspondentes aos vértices
    # Como as variáveis são livres são criadas y+ e y-
    vetorCusto = [0 for _ in range(2*(n-2))]

    # Preenche o vetor de custo das variáveis restantes com as capacidades de cada aresta
    vetorCusto.extend(capacidades.copy().tolist())

    # Nega o vetor de custos, já que esse é um problema de mínimo e deve ser convertido para um problema de máximo
    vetorCusto = np.negative(np.array(vetorCusto))

    # Retorna o vetor de custo
    return vetorCusto

def construirMatrizRestricoes(m, matrizIncidencia):
    # Constrói a matriz de restrições no formato A|b
    restricoes = []

    # Percorre as linhas da matriz de incidência que correspondem aos vértices diferentes do source e sink
    for linha in matrizIncidencia[1:-1].T:
        novaLinha = []

        # Insere os elementos de cada linha da matriz de incidência duas vezes: uma vez normal e outra negado
        # Isso é feito pois as variáveis correspondentes à matriz de incidência são livres, logo é usada a
        # definição y = y+ - y- sendo que y+ >= 0 e y- >= 0
        for elemento in linha:
            novaLinha.append(elemento)
            novaLinha.append(-elemento)

        # Adiciona a nova linha na lista de restrições
        restricoes.append(novaLinha)
    
    # Nega os valores adicionados para transformar a restrição de >= em <=
    restricoes = np.negative(np.array(restricoes))

    # Adiciona a matriz identidade na lateral, negando seus valores para transformar a restrição de >= em <=
    restricoes = np.concatenate((restricoes, np.negative(np.identity(m))), axis = 1)

    # Adiciona o vetor b na lateral da matriz de restrições, sendo que esse vetor b é igual à primeira linha
    # da matriz de incidência negada, pois deve ser igual a 1 para cada aresta que sai do source
    vetorB = np.array([matrizIncidencia[0]]).T
    restricoes = np.concatenate((restricoes, vetorB), axis = 1)

    # Retorna a matriz de restrições
    return restricoes

def executarSimplex(vetorCusto, restricoes):
    # Executa o simplex para o vetor custo e restrições definidas
    # Vale notar que o problema do simplex usado é no formato:
    # max c^T x
    # sujeita a Ax <= b
    # x >= 0
    nRestricoes = len(restricoes)
    nVariaveis = len(vetorCusto)
    resultado = resolverPL(nRestricoes, nVariaveis, vetorCusto, restricoes)
    return resultado

def tratarResultadoSimplex(n, resultado):
    # Caso a PL não tenha solução ótima, algum erro aconteceu na geração do problema para o módulo do Simplex
    if resultado[0] != constantes.OTIMA:
        raise 'PL gerada não tem valor ótimo. Erro!'
    else:
        # Caso a PL seja ótima, separa as variáveis de valor ótimo, solução e certificado
        msgOtima, valorOtimo, solucao, certificado = resultado

        # Calcula o valor real da solução, já que existem variáveis livres
        solucaoReal = []

        # Percorre a solução das variáveis correspondentes aos vértices, que são livres
        for ind in range(0, 2*(n-2), 2):
            # Calcula o valor de y com os valores de y+ e y-, sendo que y = y+ - y-
            solucaoReal.append(solucao[ind]-solucao[ind+1])

        # Percorre a solução das variáveis que não são livres
        for ind in range(2*(n-2), len(solucao)):
            solucaoReal.append(solucao[ind])

        # Imprime o valor ótimo encontrado. Como a PL é de mínimo o resultado encontrado é negado
        # O valor é arredondado para inteiro para evitar possíveis erros de precisão
        print(-int(round(valorOtimo)))

        # Imprime os valores de fluxos encontados, equivalente à solução da PL primal do problema de max flow
        for el in certificado:
            # Os valores são arredondados para inteiros para evitar possíveis erros de precisão
            print(int(round(el)), end=' ')
        print()
        
        # Imprime a indicação de que o source pertence ao corte
        print(1, end = ' ')
        for el in solucaoReal[:n-2]:
            # Os valores são arredondados para inteiros para evitar possíveis erros de precisão
            # Também, é verificado se o valor é >=1 para reproduzir o comportamento descrito em aula, em que
            # é verificado se a variável é maior ou igual a 1, e caso seja 1 é atribuído a ela
            print(int(round(el)>=1), end=' ')
        
        # Imprime a indicação de que o sink não pertence ao corte
        print(0)

if __name__ == '__main__':
    n, m, capacidades, matrizIncidencia = lerEntrada()
    vetorCusto = construirVetorCusto(n, capacidades)
    restricoes = construirMatrizRestricoes(m, matrizIncidencia)
    resultado = executarSimplex(vetorCusto, restricoes)
    tratarResultadoSimplex(n, resultado)