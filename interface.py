import pygame
import sys
from utils import string_to_matriz, gerar_matriz_embaralhada
from buscaBiDirecional import BiDirecional
from buscaAEstrela import AEstrela

# Configurações Iniciais
pygame.init()
LARGURA_MATRIZ = 600
LARGURA_PAINEL = 300 
TELA_LARGURA = LARGURA_MATRIZ + LARGURA_PAINEL
TELA_ALTURA = 600
TAMANHO_CELULA = LARGURA_MATRIZ // 3

tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
pygame.display.set_caption("Visualizador de Buscas IA")
relogio = pygame.time.Clock()

# Fontes e Cores
fonte_numeros = pygame.font.Font(None, 80)
fonte_botoes = pygame.font.Font(None, 36)
fonte_status = pygame.font.Font(None, 28)

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
FUNDO = (30, 30, 30)
CINZA_ESCURO = (50, 50, 50)
AZUL_PECA = (50, 150, 255)
VERDE_BOTAO = (46, 204, 113)
VERDE_BOTAO_HOVER = (39, 174, 96)
VERMELHO_BOTAO = (231, 76, 60)
VERMELHO_BOTAO_HOVER = (192, 57, 43)

# Classe para controle dos botões na tela
class Botao:
    def __init__(self, x, y, largura, altura, texto, cor, cor_hover):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.cor = cor
        self.cor_hover = cor_hover
        self.is_hovered = False

    def desenhar(self, surface):
        # Muda a cor se o mouse estiver em cima
        cor_atual = self.cor_hover if self.is_hovered else self.cor
        pygame.draw.rect(surface, cor_atual, self.rect, border_radius=8)
        
        # Desenha o texto centralizado
        texto_surf = fonte_botoes.render(self.texto, True, BRANCO)
        texto_rect = texto_surf.get_rect(center=self.rect.center)
        surface.blit(texto_surf, texto_rect)

    def checar_hover(self, pos_mouse):
        self.is_hovered = self.rect.collidepoint(pos_mouse)

    def checar_clique(self, pos_mouse):
        return self.rect.collidepoint(pos_mouse)

# Estado inicial da matriz
matriz_objetivo = [[1, 2, 3], [8, 0, 4], [7, 6, 5]]
matriz_estado_atual = gerar_matriz_embaralhada(matriz_objetivo, passos=20)

# Variáveis de Controle
estado_sistema = "AGUARDANDO"
algoritmo_selecionado = "BiDirecional"
caminho_calculado = []
indice_passo = 0
tempo_ultimo_movimento = 0
INTERVALO_ANIMACAO = 1000 # Milissegundos

# Criando os botões no painel
btn_executar = Botao(625, 50, 250, 50, "Executar Busca", VERDE_BOTAO, VERDE_BOTAO_HOVER)
btn_embaralhar = Botao(625, 120, 250, 50, "Embaralhar Nova", VERMELHO_BOTAO, VERMELHO_BOTAO_HOVER)
btn_algoritmo = Botao(625, 190, 250, 50, f"Alg: {algoritmo_selecionado}", CINZA_ESCURO, CINZA_ESCURO)

rodando = True
while rodando:
    tempo_atual = pygame.time.get_ticks()
    pos_mouse = pygame.mouse.get_pos()

    # Checa eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
            
        # Atualiza o hover
        if evento.type == pygame.MOUSEMOTION:
            btn_executar.checar_hover(pos_mouse)
            btn_embaralhar.checar_hover(pos_mouse)
            btn_algoritmo.checar_hover(pos_mouse)

        # Verifica os cliques na tela
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1: # Botão esquerdo
            
            # Clique em EMBARALHAR
            if btn_embaralhar.checar_clique(pos_mouse):
                matriz_estado_atual = gerar_matriz_embaralhada(matriz_objetivo)
                estado_sistema = "AGUARDANDO"
                caminho_calculado = []

            # Clique em EXECUTAR
            elif btn_executar.checar_clique(pos_mouse) and estado_sistema == "AGUARDANDO":
                
                # Algoritmo BiDirecional
                if algoritmo_selecionado == "BiDirecional":
                    busca = BiDirecional(matriz_estado_atual, matriz_objetivo)           
                else:
                    # Certifique-se de ter feito 'from buscaAEstrela import AEstrela' no topo
                    busca = AEstrela(matriz_estado_atual, matriz_objetivo)
                    
                caminho_calculado, qtd = busca.executarBusca()    

                
                if caminho_calculado:
                    estado_sistema = "ANIMANDO"
                    indice_passo = 0
                    tempo_ultimo_movimento = tempo_atual

            # Alternador de algoritmo
            elif btn_algoritmo.checar_clique(pos_mouse):
                if algoritmo_selecionado == "BiDirecional":
                    algoritmo_selecionado = "AEstrela"
                else:
                    algoritmo_selecionado = "BiDirecional"

                btn_algoritmo.texto = f"Alg: {algoritmo_selecionado}"

    # Animação dos passos
    if estado_sistema == "ANIMANDO":
        if tempo_atual - tempo_ultimo_movimento > INTERVALO_ANIMACAO:
            if indice_passo < len(caminho_calculado):
                matriz_estado_atual = string_to_matriz(caminho_calculado[indice_passo])
                indice_passo += 1
                tempo_ultimo_movimento = tempo_atual
            else:
                estado_sistema = "FINALIZADO"

    # Desenho do fundo
    tela.fill(FUNDO)

    # Desenha a Divisória do Painel
    pygame.draw.line(tela, BRANCO, (LARGURA_MATRIZ, 0), (LARGURA_MATRIZ, TELA_ALTURA), 2)

    # Desenha a Matriz
    for l in range(3):
        for c in range(3):
            valor = matriz_estado_atual[l][c]
            x = c * TAMANHO_CELULA
            y = l * TAMANHO_CELULA
            
            if valor != 0:
                retangulo = pygame.Rect(x + 5, y + 5, TAMANHO_CELULA - 10, TAMANHO_CELULA - 10)
                pygame.draw.rect(tela, AZUL_PECA, retangulo, border_radius=15)
                
                texto = fonte_numeros.render(str(valor), True, BRANCO)
                texto_rect = texto.get_rect(center=(x + TAMANHO_CELULA//2, y + TAMANHO_CELULA//2))
                tela.blit(texto, texto_rect)

    # Desenha os Botões
    btn_executar.desenhar(tela)
    btn_embaralhar.desenhar(tela)
    btn_algoritmo.desenhar(tela)

    # Desenha o Status do Sistema
    texto_status = fonte_status.render(f"Status: {estado_sistema}", True, BRANCO)
    tela.blit(texto_status, (625, 270))
    
    if estado_sistema in ["ANIMANDO", "FINALIZADO"]:
        passos_txt = fonte_status.render(f"Passos: {indice_passo} / {len(caminho_calculado)}", True, BRANCO)
        tela.blit(passos_txt, (625, 300))

    # ATtualiza o display
    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
sys.exit()