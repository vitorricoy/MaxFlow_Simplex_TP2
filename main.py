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

def construirVetorCusto(matrizIncidencia):
    # Preenche o vetor de custo com a primeira linha da matriz de incidência negada
    # Isso é feito pois é maximizado o fluxo que sai do source
    vetorCusto = [-x for x in matrizIncidencia[0]]
    vetorCusto = np.array(vetorCusto)

    # Retorna o vetor de custo
    return vetorCusto

def construirMatrizRestricoes(m, capacidades, matrizIncidencia):
    # Constrói a matriz de restrições no formato A|b
    restricoes = []

    # Percorre as linhas da matriz de incidência que correspondem aos vértices diferentes do source e sink
    for linha in matrizIncidencia[1:-1]:
        novaRestricao = linha.copy().tolist()
        novaRestricaoNegada = [-x for x in linha]
        
        # Insere 0, pois o vetor b dos vértices é igual a 0
        novaRestricao.append(0)
        novaRestricaoNegada.append(0)
        # Insere cada linha da matriz de incidência como restrição duas vezes: uma vez normal e outra negada. 
        # Isso é feito para  que a restrição de igualdade seja representada como duas restrições: uma de <= e uma
        # de >=. Como o simplex recebe apenas <=, a restrição de >= é negada
        restricoes.append(novaRestricao)
        restricoes.append(novaRestricaoNegada)
    
    for aresta in range(m):
        # Adiciona as restrições de capacidade das arestas
        novaRestricao = np.zeros(m+1)
        novaRestricao[aresta] = 1
        novaRestricao[-1] = capacidades[aresta]
        restricoes.append(novaRestricao)

    # Retorna a matriz de restrições
    restricoes = np.array(restricoes)
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
        raise Exception('PL gerada não tem valor ótimo. Erro!')
    else:
        # Caso a PL seja ótima, separa as variáveis de valor ótimo, solução e certificado
        msgOtima, valorOtimo, solucao, certificado = resultado

        # Calcula o valor real do certificado, já que existem restrições extras, correspondentes às variáveis
        # livres do dual
        certificadoReal = []

        # Percorre os certificados das restrições correspondentes aos vértices, que são duplicadas aos pares
        for ind in range(0, 2*(n-2), 2):
            # Calcula o valor da solução dual y com os valores de y+ e y-, sendo que y = y+ - y-
            certificadoReal.append(certificado[ind]-certificado[ind+1])

        # Percorre a solução das restrições correspondentes às arestas
        for ind in range(2*(n-2), len(certificado)):
            certificadoReal.append(certificado[ind])

        # Imprime o valor ótimo encontrado. Como a PL é de máximo o resultado encontrado já é correto
        # O valor é arredondado para inteiro para evitar possíveis erros de precisão
        print(int(round(valorOtimo)))

        # Imprime os valores de fluxos encontrados, equivalente à solução da PL primal do problema de max flow
        # e ao certificado de ótimo da dual
        for el in solucao:
            # Os valores são arredondados para inteiros para evitar possíveis erros de precisão
            print(int(round(el)), end=' ')
        print()
        
        # Imprime a indicação de que o source pertence ao corte
        print(1, end = ' ')

        # Imprime as indicações dos cortes, que é a solução da PL dual
        # São percorridos apenas os valores das restrições correspondentes aos vértices
        for el in certificadoReal[:n-2]:
            # Os valores são arredondados para inteiros para evitar possíveis erros de precisão
            # Também, é verificado se o valor é >=1 para reproduzir o comportamento descrito em aula, em que
            # é verificado se a variável é maior ou igual a 1, e caso seja, 1 é atribuído a ela
            print(int(round(el)>=1), end=' ')
        
        # Imprime a indicação de que o sink não pertence ao corte
        print(0)

if __name__ == '__main__':
    n, m, capacidades, matrizIncidencia = lerEntrada()
    vetorCusto = construirVetorCusto(matrizIncidencia)
    restricoes = construirMatrizRestricoes(m, capacidades, matrizIncidencia)
    resultado = executarSimplex(vetorCusto, restricoes)
    tratarResultadoSimplex(n, resultado)