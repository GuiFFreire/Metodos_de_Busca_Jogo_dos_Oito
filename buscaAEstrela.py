import heapq
from busca import Busca
from utils import matriz_to_string, string_to_matriz, movimentosPermitidos, movimentar

class AEstrela(Busca):
    def __init__(self, matriz_inicio, matriz_objetivo):
        super().__init__(matriz_inicio, matriz_objetivo)
        # Mapeia as posições corretas do objetivo para agilizar a heurística
        self.pos_objetivo = {}
        for l in range(3):
            for c in range(3):
                self.pos_objetivo[self.matriz_objetivo[l][c]] = (l, c)

    def heuristica_manhattan(self, matriz):
        """ Calcula a soma das distâncias de cada peça até sua posição final. """
        distancia = 0
        for l in range(3):
            for c in range(3):
                valor = matriz[l][c]
                if valor != 0: 
                    l_obj, c_obj = self.pos_objetivo[valor]
                    distancia += abs(l - l_obj) + abs(c - c_obj)
        return distancia

    def reconstruir_caminho(self, caminho_dict, estado_final):
        """ Reconstrói a lista de estados do início ao fim. """
        caminho = []
        atual = estado_final
        while atual is not None:
            caminho.append(atual)
            atual = caminho_dict[atual]
        caminho.reverse()
        return caminho[1:], len(caminho) - 1

    def executarBusca(self):
        """ Executa o algoritmo A* utilizando a Distância de Manhattan. """
        inicio_str = matriz_to_string(self.matriz_inicio)
        objetivo_str = matriz_to_string(self.matriz_objetivo)

        if inicio_str == objetivo_str:
            return [inicio_str], 0

        fila_prioridade = []
        h_inicial = self.heuristica_manhattan(self.matriz_inicio)
        heapq.heappush(fila_prioridade, (h_inicial, 0, inicio_str))

        caminho_pai = {inicio_str: None}
        custo_g = {inicio_str: 0}

        while fila_prioridade:
            # Pega o estado com menor f_score
            f, g, atual_str = heapq.heappop(fila_prioridade)

            if atual_str == objetivo_str:
                return self.reconstruir_caminho(caminho_pai, atual_str)

            matriz_atual = string_to_matriz(atual_str)
            movimentos, i, j = movimentosPermitidos(matriz_atual)

            for mov in movimentos:
                nova_matriz = movimentar(matriz_atual, mov, i, j)
                proximo_estado = matriz_to_string(nova_matriz)
                
                novo_g = g + 1 

                # Se o estado não foi visitado ou encontramos um caminho mais curto
                if proximo_estado not in custo_g or novo_g < custo_g[proximo_estado]:
                    custo_g[proximo_estado] = novo_g
                    f_total = novo_g + self.heuristica_manhattan(nova_matriz)
                    caminho_pai[proximo_estado] = atual_str
                    heapq.heappush(fila_prioridade, (f_total, novo_g, proximo_estado))

        return None, -1