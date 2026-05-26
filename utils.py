import copy
import random

def matriz_to_string(matriz):
    """ Transforma a matriz em string do estado atual. """
    return "|".join(",".join(str(item) for item in linha) for linha in matriz)


def string_to_matriz(estado_str):
    """ Transforma uma string do estado atual em uma matriz. """
    return [[int(item) for item in linha.split(",")] for linha in estado_str.split("|")]


def movimentosPermitidos(matriz):
    """ Retorna os movimentos permitidos e a posição 'vazia' na matriz. """

    linhas = len(matriz)
    colunas = len(matriz[0]) if linhas > 0 else 0
    i, j = -1, -1
    
    for l in range(linhas):
        for c in range(colunas):
            if matriz[l][c] == 0:
                i, j = l, c
                break
        if i != -1:
            break

    movimentos = []
    if i > 0: movimentos.append("CIMA")
    if i < linhas - 1: movimentos.append("BAIXO")
    if j > 0: movimentos.append("ESQUERDA")
    if j < colunas - 1: movimentos.append("DIREITA")

    return movimentos, i, j


def movimentar(matriz, movimento, i, j):
    """ Realiza o movimento na matriz e retorna o seu resultado."""

    nova_matriz = copy.deepcopy(matriz)
    if movimento == "CIMA":
        nova_matriz[i][j], nova_matriz[i-1][j] = nova_matriz[i-1][j], nova_matriz[i][j]
    elif movimento == "BAIXO":
        nova_matriz[i][j], nova_matriz[i+1][j] = nova_matriz[i+1][j], nova_matriz[i][j]
    elif movimento == "ESQUERDA":
        nova_matriz[i][j], nova_matriz[i][j-1] = nova_matriz[i][j-1], nova_matriz[i][j]
    elif movimento == "DIREITA":
        nova_matriz[i][j], nova_matriz[i][j+1] = nova_matriz[i][j+1], nova_matriz[i][j]
        
    return nova_matriz

def contar_inversoes(matriz):
    """
    Transforma a matriz em uma lista (ignorando o 0) e conta quantas 
    vezes um número maior aparece antes de um número menor.
    """
    lista = []
    for linha in matriz:
        for num in linha:
            if num != 0:
                lista.append(num)
                
    inversoes = 0
    for i in range(len(lista)):
        for j in range(i + 1, len(lista)):
            if lista[i] > lista[j]:
                inversoes += 1
                
    return inversoes

def gerar_matriz_embaralhada(matriz_objetivo, passos=30):
    """
    Gera uma matriz completamente aleatória, garantindo que seja
    matematicamente possível chegar ao objetivo.
    """
    # Descobre se o objetivo tem paridade par ou ímpar
    inversoes_objetivo = contar_inversoes(matriz_objetivo)
    paridade_objetivo = inversoes_objetivo % 2
    
    numeros = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    
    while True:
        # Embaralha os números de forma totalmente aleatória
        random.shuffle(numeros)
        
        # Monta a matriz 3x3
        nova_matriz = [
            [numeros[0], numeros[1], numeros[2]],
            [numeros[3], numeros[4], numeros[5]],
            [numeros[6], numeros[7], numeros[8]]
        ]
        
        # Se a paridade for igual, o quebra-cabeça tem solução!
        inversoes_nova = contar_inversoes(nova_matriz)
        if inversoes_nova % 2 == paridade_objetivo:
            return nova_matriz