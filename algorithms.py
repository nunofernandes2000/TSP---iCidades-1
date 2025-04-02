import math #importar funções da matematica
import random #importar funções random
from libic import *
from Ficha03 import *

def gerarSucessores(state):
    successors = []
    
    # Gerar todos os sucessores possiveis
    for i in range(len(state)):
        for j in range(i + 1, len(state)):
            neighbor = state[:]
            trocaIC(neighbor, i, j)
            successors.append((neighbor, distCircularIC(neighbor)))
            
    return successors

def Greedy(cidadesList, r):
    #distCircularIC -> custo

    state = cidadesList[:]

    initial_distance = distCircularIC(state)

    iterations = 0
    while iterations < r:
        iterations += 1
        successors = []

        successors = gerarSucessores(state)

        #Escolher o melhor sucessor
        best_neighbor, best_distance = min(successors, key=lambda x: x[1])

        #Verificar se há melhoria
        if best_distance >= distCircularIC(state):
            break

        state = best_neighbor

    final_distance = distCircularIC(state)

    return initial_distance, final_distance, state

def sGreedy(cidadesList, r):
    state = cidadesList[:]
    
    initial_distance = distCircularIC(state)

    b = 5
    
    iterations = 0
    while iterations < r:
        iterations += 1
        successors = []
        
        successors = gerarSucessores(state)
        
        # Ordenar os sucessores pela distância (menor para maior)
        successors.sort(key=lambda x: x[1])
        
        # Verificar se há sucessores melhores que o atual
        current_distance = distCircularIC(state)
        better_successors = [s for s in successors if s[1] < current_distance]
        
        if not better_successors:
            # Se não houver sucessores melhores, paramos
            break
        
        # Escolher aleatoriamente entre os melhores b sucessores
        # (ou todos os melhores, se houver menos que b)
        num_to_consider = min(b, len(better_successors))
        best_b_successors = better_successors[:num_to_consider]
        
        # Escolher aleatoriamente um dos melhores b sucessores
        chosen_neighbor, chosen_distance = random.choice(best_b_successors)
        state = chosen_neighbor
    
    final_distance = distCircularIC(state)

    return initial_distance, final_distance, state 

def pGreedyIC(cidadesList, r):
    current = cidadesList[:]
    
    # calcula a distância inicial
    initial_distance = distCircularIC(current)
    
    iterations = 0
    while iterations < r:
        iterations += 1
        improved = False
        
        # numero de cidades
        n = len(current)
        
        # esclhe uma posição random para trocar
        fixed_position = random.randint(0, n-1)
        
        # Try swapping with each other position (O(n) successors)
        for j in range(n):
            if j == fixed_position:
                continue
                
            # Create a new path by swapping cities at positions fixed_position and j
            neighbor = current[:]
            trocaIC(neighbor, fixed_position, j)
            
            # Calculate the cost of the new path
            new_distance = distCircularIC(neighbor)
            
            # If the new path is better, update current path
            if new_distance < distCircularIC(current):
                current = neighbor
                improved = True
                break  # First improvement strategy
        
        # If no improvement was found, we can stop
        if not improved:
            break
    
    final_distance = distCircularIC(current)
    
    return initial_distance, final_distance, current

def rGreedyIC(cidadesList, r):
    # Numero de restarts
    num_restarts = 10
    
    # Keep track of the initial state for return purposes
    original_cities = cidadesList[:]
    initial_distance = distCircularIC(original_cities)
    
    # Save the best solution across all restarts
    best_state = original_cities[:]
    best_distance = initial_distance
    
    # Perform multiple restarts
    for restart in range(num_restarts):
        # For the first restart, use the original list
        # For subsequent restarts, use a random permutation
        if restart == 0:
            current_state = original_cities[:]
        else:
            current_state = original_cities[:]
            random.shuffle(current_state)
        
        # Run standard hill climbing
        iterations = 0
        while iterations < r:
            iterations += 1
            successors = []
            
            successors = gerarSucessores(current_state)
            
            # escolhe o melhor sucessor
            best_neighbor, best_neighbor_distance = min(successors, key=lambda x: x[1])
            
            # veerifica se houve melhoria
            if best_neighbor_distance >= distCircularIC(current_state):
                break
            
            current_state = best_neighbor
        
        current_distance = distCircularIC(current_state)
        if current_distance < best_distance:
            best_state = current_state[:]
            best_distance = current_distance
    
    return initial_distance, best_distance, best_state