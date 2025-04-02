import math #importar funções da matematica
import random #importar funções random
from libic import *

def iCidade(id,x,y):
    return (id, x, y)

def getId(iCidade):
    return iCidade[0]

def getX(iCidade):
    return iCidade[1]

def getY(iCidade):
    return iCidade[2]

def distIC(cidade1, cidade2):
    return math.sqrt((getX(cidade2) - getX(cidade1))**2 + (getY(cidade2) - getY(cidade1))**2)

def nCidades(n):
    list = []
    for i in range(1,n+1):
        list.append(iCidade(i, random.randint(0,1000), random.randint(0,1000)))
        
    return list

def distCircularIC(cidadesList):
    return sum([distIC(cidadesList[i], cidadesList[i+1]) 
                for i in range(len(cidadesList)-1)]) + distIC(cidadesList[-1], cidadesList[0])
    
def trocaIC(cidadesList, pos1, pos2):
    cidadesList[pos1], cidadesList[pos2] = cidadesList[pos2], cidadesList[pos1]
    return cidadesList


cidadesList = nCidades(4)

for cidade in cidadesList:   
    pos1 = random.randint(0, len(cidadesList)-1)
    pos2 = random.randint(0, len(cidadesList)-1)
    cidadesList = trocaIC(cidadesList, pos1, pos2)

def trocaseMelhorIC(cidadesList):

    listaOriginal = cidadesList.copy() 

    pos1 = random.randint(0, len(cidadesList)-1) 
    pos2 = random.randint(0, len(cidadesList)-1) 

    novaLista = listaOriginal.copy() 
    trocaIC(novaLista, pos1, pos2)

    if distCircularIC(novaLista) <= distCircularIC(listaOriginal):
        return novaLista
    return cidadesList

r = 3

def melhoraDistCircularIC(cidadesList, r):
    for i in range(r):
        cidadesList = trocaseMelhorIC(cidadesList)
    return cidadesList

r = 3

def optDistCircularIC(cidadesList, r):
    distOriginal = distCircularIC(cidadesList)
    novaLista = melhoraDistCircularIC(cidadesList, r)
    distNova = distCircularIC(novaLista)

    return distOriginal, distNova, novaLista


        
