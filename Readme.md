# Visualizador de Algoritmos de Busca em Matriz

Este projeto é uma implementação em Python de algoritmos de busca (como a Busca Bidirecional) aplicados à resolução do Jogo dos 8. Ele inclui uma interface gráfica interativa construída com Pygame para visualizar o passo a passo da solução.

## Estrutura do Projeto

* `interface.py`: Arquivo principal que gerencia a interface gráfica, botões e animações.
* `busca.py`: Classe abstrata e estrutura de dados base para os algoritmos.
* `buscaBiDirecional.py`: Implementação do algoritmo de Busca Bidirecional.
* `utils.py`: Funções auxiliares para manipulação da matriz e geração de estados válidos.

## Pré-requisitos

Certifique-se de ter o Python 3 instalado em sua máquina. Recomendado Python 3.12 devido a biblioteca do Pygame.

## Como Executar

1. Crie o ambiente virtual:
```bash
python -m venv venv
```

2. Ative o ambiente virtual:

**No Windows:**
```cmd
venv\Scripts\activate
```

**No Linux ou Mac:**
```bash
source venv/bin/activate
```

3. Instale as dependências necessárias:
```bash
pip install -r requirements.txt
```

4. Execute a interface gráfica:

**No Windows:**
```cmd
python interface.py
```

**No Linux, Mac ou WSL:**
```bash
python3 interface.py
```

## Como Usar a Interface

* **Embaralhar Nova**: Gera um novo estado inicial aleatório.
* **Executar Busca**: Calcula a rota da solução em segundo plano e inicia a animação da matriz se resolvendo passo a passo.