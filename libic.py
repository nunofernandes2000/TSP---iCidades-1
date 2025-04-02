import math
import random
from tkinter import *
from algorithms import *
from Ficha03 import *

# --------------------------
#   Funcoes parte grafica
# --------------------------
def minmaxListaIC(l):
    min,max = l[0][1], l[0][1]
    for ic in l:
        if ic[1] < min:
            min = ic[1]
        if ic[1] > max:
            max = ic[1]
        if ic[2] < min:
            min = ic[2]
        if ic[2] > max:
            max = ic[2]
    return min,max

# Considero limite de 15 pixeis à volta
def convertXY(x, y, min, max, size):
    limite = 15
    ratio =  (size - 2*limite) / (max-min)
    xNew = (limite + (x-min) * ratio)
    yNew = (limite + (y-min) * ratio)
    return xNew, yNew

def windowIC(tamanho):
    window = Tk()
    window.title("iCidade")
    window.geometry("+10+10")
    window.minsize(tamanho,tamanho)

    c = Canvas(window,bg="white", height=tamanho, width=tamanho)
    return window, c, tamanho

def drawIC(l, windefs):
    (window, c, tamanho) = windefs
    c.delete('all')

    min, max = minmaxListaIC(l)
    for i in range(-1,len(l)-1):
        xi,yi = convertXY(l[i][1], l[i][2], min, max, tamanho)
        xf,yf = convertXY(l[i+1][1], l[i+1][2], min, max, tamanho)
        c.create_line(xi,yi,xf,yf, fill="blue", width=2)
    for ic in l:
        x,y = convertXY(ic[1], ic[2], min, max, tamanho)
        c.create_oval(x-5,y-5,x+5,y+5, fill="yellow")
        #c.create_text(x,y, text=str(ic[0]), fill="black", font=('Helvetica', '8', 'bold'))

    c.pack()
    window.update()
    return windefs


# ----------------------------------
#   Funções para ler de ficheiros
# ----------------------------------
def checkStrBegin(s, txt):
    return (s == txt[0:len(s)])

# Função para ler um ficheiro tsp
def readTSP2ListIC(file):
    readIC = False
    listaIC = []
    fin = open(file,"r")
    llinhas = fin.read().splitlines()
    for linha in llinhas:
        if checkStrBegin("NODE_COORD_SECTION", linha):
            readIC = True
            continue
        if checkStrBegin("EOF", linha):
            readIC = False
            break
        if readIC:
            lista = linha.split()
            ic = int(lista[0]), float(lista[1]), float(lista[2])
            listaIC.append(ic)
    fin.close()
    return listaIC

# Função para ler um ficheiro TSP e respetivo ficheiro de tour óptima
def readTSP2ListICOpt(file, fileOpt):
    listaIC = readTSP2ListIC(file)
    readID = False
    listaOpt = []
    fin = open(fileOpt,"r")
    llinhas = fin.read().splitlines()
    for linha in llinhas:
        if checkStrBegin("TOUR_SECTION", linha):
            readID = True
            continue
        if checkStrBegin("EOF", linha):
            readID = False
            break
        if readID:
            id = int(linha)
            if(id==-1):
                readID = False
                break
            listaOpt.append(listaIC[id-1])
    fin.close()
    return listaOpt



# -------------------------
#   Para testar o código:
# -------------------------
"""
# Criar uma janela    
w = windowIC(800)

# Criar uma lista de IC
#l = [(1, 10.0, 15.0), (2, 15.0, 6.5), (3, 12.1, 19.7)]

# Ler um TSP para uma lista de IC
l = readTSP2ListIC("berlin52.tsp")
# Desenhar graficamente a lista de IC
drawIC(l,w)
input("Enter para continuar... ")

# Ler o TSP e a tour óptima para uma lista de IC
l = readTSP2ListICOpt("berlin52.tsp", "berlin52.opt.tour")
# Desenhar graficamente a lista de IC
drawIC(l,w)
input("Enter para continuar... ")
"""

