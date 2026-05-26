from busca import Busca, EstruturaBusca
from utils import  matriz_to_string, string_to_matriz, movimentosPermitidos, movimentar

class BiDirecional(Busca):
    def reconstruir_caminho_total(self, ponto_encontro, cam_inicio, cam_fim):
        """ Reconstrói o caminho retornando as matrizes que fazem parte dele. """

        # Busca do ponto de encontro até o inicial
        caminho_da_origem = []
        atual = ponto_encontro
        while atual is not None:
            caminho_da_origem.append(atual)
            atual = cam_inicio.caminho[atual]
        # Reverte para ficar na ordem da busca
        caminho_da_origem.reverse() 

        # Busca do ponto de encointro até o final
        caminho_ao_destino = []
        atual = cam_fim.caminho[ponto_encontro] 
        while atual is not None:
            caminho_ao_destino.append(atual)
            atual = cam_fim.caminho[atual]

        # Retorna o caminho completo, na ordem de execução das peças
        return caminho_da_origem + caminho_ao_destino

    def executarBusca(self):
        """ Executa busca bidirecional. """
        inicio = matriz_to_string(self.matriz_inicio)
        objetivo = matriz_to_string(self.matriz_objetivo)

        # Verifica se já está resolvido
        if inicio == objetivo:
            return [inicio], 0

        frente_inicio = EstruturaBusca()
        frente_inicio.adicionar(inicio, pai=None)

        frente_fim = EstruturaBusca()
        frente_fim.adicionar(objetivo, pai=None)

        while frente_inicio.fila and frente_fim.fila:

            # Obtém a matriz atual a partir do início
            atual_ini = frente_inicio.fila.popleft()
            matriz_atual_ini = string_to_matriz(atual_ini) 
            
            # Testa todos os movimentos permitidos para a matriz a partir do início
            movimentos, i, j = movimentosPermitidos(matriz=matriz_atual_ini)
            for mov in movimentos:
                nova_matriz = movimentar(matriz=matriz_atual_ini, movimento=mov, i=i, j=j)
                novo_estado = matriz_to_string(nova_matriz)
                
                # Se estiver no caminho a partir do fim, encontrou o resultado
                if novo_estado in frente_fim.caminho:
                    frente_inicio.adicionar(novo_estado, pai=atual_ini)
                    caminho_completo = self.reconstruir_caminho_total(novo_estado, frente_inicio, frente_fim)

                    caminho_final = caminho_completo[1:]
                    return caminho_final, len(caminho_final)
                
                frente_inicio.adicionar(novo_estado, pai=atual_ini)

            # Testa todos os movimentos permitidos para a matriz a partir do fim
            atual_fim = frente_fim.fila.popleft()
            matriz_atual_fim = string_to_matriz(atual_fim)
            
            movimentos, i, j = movimentosPermitidos(matriz=matriz_atual_fim)
            for mov in movimentos:
                
                nova_matriz = movimentar(matriz=matriz_atual_fim, movimento=mov, i=i, j=j)
                novo_estado = matriz_to_string(nova_matriz)
                
                # Se estiver no caminho a partir do início, encontrou o resultado
                if novo_estado in frente_inicio.caminho:
                    frente_fim.adicionar(novo_estado, pai=atual_fim)
                    caminho_completo = self.reconstruir_caminho_total(novo_estado, frente_inicio, frente_fim)

                    caminho_final = caminho_completo[1:]
                    return caminho_final, len(caminho_final)
                
                frente_fim.adicionar(novo_estado, pai=atual_fim)

        # Se não encontrar um caminho
        return None, -1