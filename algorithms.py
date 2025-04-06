"""""
	21635 -- Nuno Fernandes
	21986 -- Rafael Carvalho	
"""
import random
from libic import *
from Ficha03 import *

def gerarSucessores(estado):
    """
    Gera todos os sucessores possíveis a partir de um estado,
    trocando pares de cidades.
    """
    sucessores = []
    
    # Gerar todos os sucessores possiveis
    for i in range(len(estado)):
        for j in range(i + 1, len(estado)):
            vizinho = estado[:]
            trocaIC(vizinho, i, j)
            sucessores.append((vizinho, distCircularIC(vizinho)))
            
    return sucessores


def optDistCircularIC(cidadesList, r):
    distOriginal = distCircularIC(cidadesList)
    novaLista = melhoraDistCircularIC(cidadesList, r)
    distNova = distCircularIC(novaLista)

    return distOriginal, distNova, novaLista


def Greedy(cidadesList, r):
    """
    Hill Climbing (Greedy) para o problema do TSP.
    Em cada iteração, escolhe o melhor vizinho dentre todos os possíveis.
    """
    # Definir constantes para o novo critério de paragem
    k = 5  # número de iterações para verificar a melhoria
    epsilon = 0.001  # valor pequeno para a melhoria mínima
    
    # Cria uma cópia da lista de cidades
    estado = cidadesList[:]
    
    # Calcula a distância inicial
    distanciaInicial = distCircularIC(estado)
    
    # Lista para armazenar as melhorias nas últimas k iterações
    melhoriasRecentes = []
    
    iteracoes = 0
    while iteracoes < r:
        iteracoes += 1
        
        # Distância atual
        distanciaAtual = distCircularIC(estado)
        
        # Gera todos os sucessores possíveis
        sucessores = gerarSucessores(estado)
        
        # Escolhe o melhor sucessor
        melhorVizinho, melhorDistancia = min(sucessores, key=lambda x: x[1])
        
        # Verifica se houve melhoria
        if melhorDistancia >= distCircularIC(estado):
            break
        
        # Calcula a melhoria nesta iteração
        melhoria = distanciaAtual - melhorDistancia
        
        # Atualiza o estado
        estado = melhorVizinho
        
        # Registra a melhoria
        melhoriasRecentes.append(melhoria)
        
        # Mantém apenas as últimas k melhorias
        if len(melhoriasRecentes) > k:
            melhoriasRecentes.pop(0)
        
        # Verifica critério de paragem por epsilon
        if len(melhoriasRecentes) == k:
            melhoriaTotal = sum(melhoriasRecentes)
            if melhoriaTotal < epsilon:
                break
    
    distanciaFinal = distCircularIC(estado)
    
    return distanciaInicial, distanciaFinal, estado

def sGreedy(cidadesList, r):
    """
    Stochastic Hill Climbing para o problema do TSP.
    Em cada iteração, escolhe aleatoriamente um dos b melhores vizinhos.
    """
    # Definir constantes para o novo critério de paragem
    k = 5  # número de iterações para verificar a melhoria
    epsilon = 0.001  # valor pequeno para a melhoria mínima 
    b = 10
    
    # Cria uma cópia da lista de cidades
    estadoAtual = cidadesList[:]
    
    # Calcula a distância inicial
    distanciaInicial = distCircularIC(estadoAtual)
    
    # Lista para armazenar as melhorias nas últimas k iterações
    melhoriasRecentes = []
    
    iteracoes = 0
    while iteracoes < r:
        iteracoes += 1
        
        # Distância atual
        distanciaAtual = distCircularIC(estadoAtual)
        
        # Gera todos os sucessores possíveis
        sucessores = gerarSucessores(estadoAtual)
        
        # Ordena os sucessores pelo custo (menor para maior)
        sucessores.sort(key=lambda x: x[1])
        
        # Seleciona os b melhores sucessores
        melhoresSucessores = sucessores[:b]
        
        # Escolhe aleatoriamente um dos b melhores
        vizinhoEscolhido, distanciaEscolhida = random.choice(melhoresSucessores)
        
        # Verifica se houve melhoria
        if distanciaEscolhida >= distCircularIC(estadoAtual):
            break
        
        # Calcula a melhoria nesta iteração
        melhoria = distanciaAtual - distanciaEscolhida
        
        # Atualiza o estado
        estadoAtual = vizinhoEscolhido
        
        # Registra a melhoria
        melhoriasRecentes.append(melhoria)
        
        # Mantém apenas as últimas k melhorias
        if len(melhoriasRecentes) > k:
            melhoriasRecentes.pop(0)
        
        # Verifica critério de paragem por epsilon
        if len(melhoriasRecentes) == k:
            melhoriaTotal = sum(melhoriasRecentes)
            if melhoriaTotal < epsilon:
                break
    
    distanciaFinal = distCircularIC(estadoAtual)
    
    return distanciaInicial, distanciaFinal, estadoAtual


def pGreedy(cidadesList, r):
    """
    Partial Hill Climbing (pGreedy) para o problema do TSP.
    Em cada iteração, considera apenas O(n) sucessores em vez de O(n²).
    """
    # Definir constantes para o novo critério de paragem
    k = 5  # número de iterações para verificar a melhoria
    epsilon = 0.001  # valor pequeno para a melhoria mínima
    
    # Cria uma cópia da lista de cidades
    estadoAtual = cidadesList[:]
    
    # Calcula a distância inicial
    distanciaInicial = distCircularIC(estadoAtual)
    
    # Lista para armazenar as melhorias nas últimas k iterações
    melhoriasRecentes = []
    
    iteracoes = 0
    while iteracoes < r:
        iteracoes += 1
        melhorou = False
        
        # Distância atual antes de qualquer mudança nesta iteração
        distanciaAtual = distCircularIC(estadoAtual)
        
        # Número de cidades
        n = len(estadoAtual)
        
        # Escolhe uma posição aleatória para trocar
        posicaoFixa = random.randint(0, n-1)
        
        # Tenta trocar com cada outra posição (O(n) sucessores)
        for j in range(n):
            if j == posicaoFixa:
                continue
                
            # Cria um novo caminho trocando as cidades nas posições posicaoFixa e j
            vizinho = estadoAtual[:]
            trocaIC(vizinho, posicaoFixa, j)
            
            # Calcula o custo do novo caminho
            novaDistancia = distCircularIC(vizinho)
            
            # Se o novo caminho for melhor, atualiza o caminho atual
            if novaDistancia < distanciaAtual:
                # Calcular a melhoria antes de atualizar
                melhoria = distanciaAtual - novaDistancia
                
                # Atualizar o estado
                estadoAtual = vizinho
                melhorou = True
                
                # Registra a melhoria
                melhoriasRecentes.append(melhoria)
                
                # Mantém apenas as últimas k melhorias
                if len(melhoriasRecentes) > k:
                    melhoriasRecentes.pop(0)
                
                break  # Estratégia de primeira melhoria
        
        # Se não houver melhoria, podemos parar
        if not melhorou:
            break
            
        # Verifica critério de paragem por epsilon
        if len(melhoriasRecentes) == k:
            melhoriaTotal = sum(melhoriasRecentes)
            if melhoriaTotal < epsilon:
                break
    
    distanciaFinal = distCircularIC(estadoAtual)
    
    return distanciaInicial, distanciaFinal, estadoAtual

def rGreedy(cidadesList, r):
    """
    Algoritmo de Reinício para o problema do TSP.
    Realiza múltiplos reinícios do algoritmo escolhido, neste caso o SGreedy.
    """
    # Definir constantes para o novo critério de paragem
    k = 5  # número de iterações para verificar a melhoria
    epsilon = 0.001  # valor pequeno para a melhoria mínima
    
    # Definir número máximo de reinícios
    numReiniciosMax = 10
    
    # Manter o estado inicial para fins de retorno
    cidadesOriginais = cidadesList[:]
    distanciaInicial = distCircularIC(cidadesOriginais)
    
    # Guardar a melhor solução entre todos os reinícios
    melhorEstado = cidadesOriginais[:]
    melhorDistancia = distanciaInicial
    
    # Lista para armazenar as melhorias dos últimos k reinícios
    melhoriasReiniciosRecentes = []
    
    # Realizar múltiplos reinícios
    for contadorReiniciosFeitos in range(numReiniciosMax):
        # Para o primeiro reinício, usar a lista original
        # Para os reinícios subsequentes, usar uma permutação aleatória
        if contadorReiniciosFeitos == 0:
            cidadesAtuais = cidadesOriginais[:]
        else:
            cidadesAtuais = cidadesOriginais[:]
            random.shuffle(cidadesAtuais)
        
        # Regista a distância do melhor estado antes deste reinício
        distanciaAnterior = melhorDistancia
        
        # Chamar o algoritmo escolhido com a lista atual
        _, distanciaAtual, estadoAtual = sGreedy(cidadesAtuais, r)
        
        # Após a execução, verificar se este reinício produziu uma solução melhor
        if distanciaAtual < melhorDistancia:
            melhorEstado = estadoAtual[:]
            melhorDistancia = distanciaAtual
            
            # Calcular a melhoria obtida com este reinício
            melhoria = distanciaAnterior - melhorDistancia
            
            # Registra a melhoria deste reinício
            melhoriasReiniciosRecentes.append(melhoria)
            
            # Mantém apenas as últimas k melhorias
            if len(melhoriasReiniciosRecentes) > k:
                melhoriasReiniciosRecentes.pop(0)
            
            # Verifica critério de paragem por epsilon
            if len(melhoriasReiniciosRecentes) == k:
                melhoriaTotal = sum(melhoriasReiniciosRecentes)
                if melhoriaTotal < epsilon:
                    break
        else:
            # Se não houver melhoria neste reinício, registra zero
            melhoriasReiniciosRecentes.append(0)
            
            # Mantém apenas as últimas k melhorias
            if len(melhoriasReiniciosRecentes) > k:
                melhoriasReiniciosRecentes.pop(0)
    
    return distanciaInicial, melhorDistancia, melhorEstado