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

def gerar_matriz_embaralhada(matriz_objetivo, passos=30):
    """ Gera uma matriz inicial. """
    
    matriz_atual = copy.deepcopy(matriz_objetivo)
    
    for _ in range(passos):
        movimentos, i, j = movimentosPermitidos(matriz_atual)
        movimento_escolhido = random.choice(movimentos)
        matriz_atual = movimentar(matriz_atual, movimento_escolhido, i, j)
        
    return matriz_atual