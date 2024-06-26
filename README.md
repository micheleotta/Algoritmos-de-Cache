# Algoritmos-de-Cache
Trabalho por: Artur Pandolfo Meneghete, Leonardo Min Woo Chung, Michele Cristina Otta e Yejin Chung

Programa em python que simula um aplicativo de leitura de textos com memória cache. Desenvolvido para a matéria Performance em Sistemas Ciberfísicos - PUCPR.

# Como funciona
Ao rodar, o programa aguarda um número de entrada, que pode ser:

1-100 = abre e apresenta em tela o texto identificado pelo número para leitura.

0 = o programa é ser encerrado. 

-1 = o programa entra em modo de simulação.

# Textos
Os 100 textos do programa são gerados no início do código e contemplam, cada um, pelo menos 1000 palavras.

# Modo de simulação
Simula o funcionamento dos algoritmos de cache LFU (Least Frequently Used), LRU (Least Recently Used) e FIFO (First In First Out). 

Para 200 solicitações de 3 usuários diferentes, com o número do texto sendo escolhido de 3 maneiras diferentes: aleatório puro
e simples, aleatório com distribuição de Poisson e aleatório de forma que textos numerados entre 30 e 40 tenham 33% de chance de serem sorteados.

Ao final, é gerado um relatório em forma de texto que apresenta cada um dos usuários,
cada um dos algoritmos de cache, os tempos de apresentação de cada texto e o número de vezes
que o arquivo solicitado não estava no cache (cache miss) e o número de vezes em que o arquivo estava no cache (cache hit).
