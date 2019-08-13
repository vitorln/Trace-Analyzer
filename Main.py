#coding: utf-8
from collections import defaultdict
import time
import math

def hex2bin(hexdata):
    scale = 16
    return bin(int(hexdata, scale))[2:]

def trace_name(path_file):
    idx = path_file.rfind('/')
    return path_file[idx+1:]

def readFile(desloc, path_file):
    lista = []
    with open(path_file) as f:
        for line in f:
            (key, val) = line.split()
            lista.append(int('0b0' + hex2bin(key)[:-desloc], 2))
    return lista

def workingSet(process_list, tam_conjunto):
    conjuntos = {}
    t = 0
    for intervalo in range(0, len(process_list), tam_conjunto):
        conjuntos[t] = processaConjunto(process_list[intervalo : intervalo + tam_conjunto-1])
        t += 1
    return conjuntos

def processaConjunto(intervalo):
    paginas_conjunto = []
    for elemento in intervalo:
        if (elemento not in paginas_conjunto):
            paginas_conjunto.append(elemento)
    return (len(paginas_conjunto), paginas_conjunto)


def main():
    path_file = "traces/gcc.trace.txt"
    page_size = 4096 #20 numero pag e 12 desloc
    desloc = int(math.log2(page_size))
    tam_conjunto = 100
    
    process_list = readFile(desloc, path_file)
    conjuntos = workingSet(process_list, tam_conjunto)
    
    print("tamanho da pagina: {0}\ntamanho da janela: {1}\n".format(page_size, tam_conjunto))
    contador_conjuntos = 0
    contador_falhas = 0
    contador_falhas_total = 0
    lista_falhas = []
    teste = conjuntos[0]
    for i in conjuntos:
        contador_conjuntos += conjuntos[i][0]
        if (i != 0):
            for j in conjuntos[i][1]:
                if (j not in teste[1]):
                    contador_falhas +=1
            for j in teste[1]:
                if (j not in conjuntos[i][1]):
                    contador_falhas +=1
            lista_falhas.append(contador_falhas)
            contador_falhas_total += contador_falhas
            contador_falhas = 0
            teste = conjuntos[i]
    media_conjuntos = contador_conjuntos/len(conjuntos)

    print("media dos conjuntos: {0}\nfalhas totais: {1}\n\n".format(media_conjuntos, contador_falhas_total))
    for i in conjuntos:
        print("ws({0}): tam = {1}\nconjunto: {2}\n\n".format(i, conjuntos[i][0], conjuntos[i][1] ))
        if i < len(conjuntos)-1:
            print("diferença entre ws({0}) e ws({1}): {2}\n\n".format(i, i+1, lista_falhas[i]))    


if __name__ == "__main__":
    main()