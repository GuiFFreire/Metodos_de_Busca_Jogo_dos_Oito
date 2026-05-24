from collections import deque
from abc import ABC, abstractmethod
import copy

class EstruturaBusca:
    """ Armazena o caminho da busca. """
    def __init__(self):
        self.caminho = {}
        self.fila = deque()

    def adicionar(self, estado, pai=None):
        """ Adiciona um estado no caminho. """

        # Não deixa adicionar estado que já foi verificado
        if estado not in self.caminho:
            self.caminho[estado] = pai
            self.fila.append(estado)
            return True
        return False

class Busca(ABC):
    def __init__(self, matriz_inicio, matriz_objetivo):
        self.matriz_inicio = matriz_inicio
        self.matriz_objetivo = matriz_objetivo
    
    @abstractmethod
    def executarBusca(self):
        pass
    
