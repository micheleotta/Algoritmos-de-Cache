# RA1 - Grupo 12
# Artur Pandolfo Meneghete | Leonardo Min Woo Chung | Michele Cristina Otta | Yejin Chung


import time
import random
from random import choices
from scipy.stats import poisson


# Função para dividir o arquivo em partes de 1000 palavras (100 textos) ***
def dividir_livro(filename):
  with open(filename, 'r', encoding='utf-8') as f:
    content = f.read()
    palavras = content.split()
    num_palavras_por_parte = 1000
    num_partes_desejadas = 100

    # Calcular o número de partes com base no limite 
    # de palavras por parte e no total de palavras
    num_partes = min(num_partes_desejadas, len(palavras) // num_palavras_por_parte + 1)

    # Dividindo o livro em partes de 1000 palavras
    partes = []
    for i in range(num_partes):
      indice_inicial = i * num_palavras_por_parte
      indice_final = (i + 1) * num_palavras_por_parte
      conteudo_parte = ' '.join(palavras[indice_inicial:indice_final])
      partes.append(conteudo_parte)

    # Salvar em arquivos separados
    for i, parte in enumerate(partes):
      nome_parte = f"{i + 1}.txt"
      with open(nome_parte, 'w', encoding='utf-8') as parte_arquivo:
        parte_arquivo.write(parte)


filename = 'donquixote.txt'
dividir_livro(filename)


# Função que retorna o conteúdo do .txt com base no número passado por parâmetro
def carrega_texto(num_texto):
  with open(f"{num_texto}.txt", 'r', encoding='utf-8') as f:
    return f.readlines()


# Escolhas aleatórias feitas pelos usuários
def escolha_aleatoria(escolha):
  match escolha:
    case 1: 
      # Aleatório, puro e simples 
      return random.randint(1, 100)

    case 2:
      # Utilizando a distribuição de poisson
      # A média do poisson: mu (o número significa mu)
      x = poisson(50)     
      return (x.rvs(1))[0]   

    case 3:
      # Escolha aleatória em que numeros entre 30 e 40 
      # tenham 33% de chance de serem sorteados
      population = list(range(1, 101))
      weights = [33 if 30 <= x <= 40 else 1 for x in population]
      return choices(population, weights, k=1)[0]


cache_max = 10
solicitacoes = 200

# LFU - Least Frequently Used *************************************
def LFU(usuario):
  for aleatoria in range(3):
    cache_hit = 0
    cache_miss = 0
    tempo_total = 0

    cache = {}
    '''
    cache [numero do texto] = [0] texto em .txt  [1] frequência
    '''

    for i in range(solicitacoes):

      numero = escolha_aleatoria(aleatoria + 1)
      tempo_inicio = time.time()

      if numero in cache:
        cache_hit += 1
        # Na ocorrência de cache hit, incrementa na frequência
        cache[numero][1] += 1

      else:
        cache_miss += 1
        if(len(cache) == cache_max):
          # Remove o menos frequente, se o cache estiver lotado
          posicao_menor = min(cache, key=lambda x: cache[x][1])
          del cache[posicao_menor]
        # Em caso de cache miss, adiciona no cache
        cache[numero] = [carrega_texto(numero), 1]
      print(" ".join(cache[numero][0]))
      tempo_total += time.time() - tempo_inicio

    # Gerar o relatório
    with open("relatorio.txt", 'a', encoding='utf-8') as arquivo:
      arquivo.write(f"\n\nUser {usuario}   LFU   modo aleatório {aleatoria + 1}")
      arquivo.write(f"\ncache hit = {cache_hit}")
      arquivo.write(f"\ncache miss = {cache_miss}")
      arquivo.write(f"\ntempo médio = {tempo_total / solicitacoes}")


# LRU - Least Recently Used ***************************************
def LRU(usuario):
  for aleatoria in range(3):
    cache_hit = 0
    cache_miss = 0
    tempo_total = 0

    cache = []
    '''
    [0] número do texto [1] texto em .txt
    '''

    for i in range(solicitacoes):

      numero = escolha_aleatoria(aleatoria + 1)
      tempo_inicio = time.time()

      if numero in (x[0] for x in cache):
        cache_hit += 1
        # Quando uma linha é referenciada, ela move à frente da lista
        if numero != cache[0][0]: 
          cache = [x for x in cache if x[0] != numero]
          cache.insert(0, [numero, carrega_texto(numero)])
      else:
        cache_miss += 1
        if len(cache) == cache_max:
          # Para acomodar um novo bloco, a linha no final (com o menos acessado 
          # recentemente) da lista é substituída
          cache.pop()
        cache.insert(0, [numero, carrega_texto(numero)])

      txt = next((x for x in cache if x[0] == numero))
      print(" ".join(txt[1]))
      tempo_total += time.time() - tempo_inicio

    # Gerar o relatório
    with open("relatorio.txt", 'a', encoding='utf-8') as arquivo:
      arquivo.write(f"\n\nUser {usuario}   LRU   modo aleatório {aleatoria + 1}")
      arquivo.write(f"\ncache hit = {cache_hit}")
      arquivo.write(f"\ncache miss = {cache_miss}")
      arquivo.write(f"\ntempo médio = {tempo_total / solicitacoes}")


# FIFO - First In First Out ***************************************
def FIFO(usuario):
  for aleatoria in range(3):
    cache_hit = 0
    cache_miss = 0
    tempo_total = 0

    cache = []

    for i in range(solicitacoes):

      numero = escolha_aleatoria(aleatoria + 1)
      tempo_inicio = time.time()

      if numero in (x[0] for x in cache):
        cache_hit += 1

      else:
        cache_miss += 1
        if(len(cache) == cache_max):
          # Caso o cache esteja cheio, remove o primeiro que entrou
          cache.pop(0)
        # Adiciona o novo elemento no final
        cache.append([numero, carrega_texto(numero)])   

      txt = next((x for x in cache if x[0] == numero))
      print(" ".join(txt[1]))
      tempo_total += time.time() - tempo_inicio
    # Gerar o relatório
    with open("relatorio.txt", 'a', encoding='utf-8') as arquivo:
      arquivo.write(f"\n\nUser {usuario}   FIFO   modo aleatório {aleatoria + 1}")
      arquivo.write(f"\ncache hit = {cache_hit}")
      arquivo.write(f"\ncache miss = {cache_miss}")
      arquivo.write(f"\ntempo médio = {tempo_total / solicitacoes}")


def user(usuario):
  LFU(usuario)
  LRU(usuario)
  FIFO(usuario)


def modo_simulacao():
  # Deixa o arquivo do relatório em branco
  with open("relatorio.txt", 'w', encoding='utf-8') as arquivo:
    arquivo.write("RELATÓRIO ALGORITMOS DE CACHE")

  # Simulação com 3 usuários
  for usuario in range(3):
    user(usuario)


encerrar = 0
cache = {}
while encerrar != 1:
  opcao = int(input("\n====== APP DE LEITURA ======\n0 Encerrar programa\n-1 Modo de simulação\n1 - 100 Número do texto\n\nSelecione uma opção:"))
  if opcao == 0:
    encerrar = 1
    
  elif opcao == -1:
    modo_simulacao()
    
  elif 1 <= opcao <= 100:
    # Algoritmo de cache mais eficiente com base no tempo de 
    # apresentação do arquivo de textos em tela = LFU
    if opcao in cache:
      cache[opcao][1] += 1

    else:
      if(len(cache) == cache_max):
        posicao_menor = min(cache, key=lambda x: cache[x][1])
        del cache[posicao_menor]
      cache[opcao] = [carrega_texto(opcao), 1]
    print(" ".join(cache[opcao][0]))
  
  # Na inserção de uma opção inválida
  else:
    print("\nOpção inválida. Tente novamente.")

