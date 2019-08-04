#coding: utf-8
from collections import defaultdict
import time
import math

def hex2bin(hexdata):
    scale = 16
    num_of_bits = 8

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
    
    for intervalo in range(tam_conjunto-1, len(process_list)):
        processaConjunto(process_list[intervalo - (tam_conjunto - 1) : intervalo])
        
def processaConjunto(intervalo):
    paginas_conjunto = []
    for elemento in intervalo:
        if (elemento not in paginas_conjunto):
            paginas_conjunto.append(elemento)
    print(len(paginas_conjunto))


def main():
    path_file = "traces/gcc.trace.txt"
    page_size = 16777216 #20 numero pag e 12 desloc
    desloc = int(math.log2(page_size))
    tam_conjunto = 10
    
    process_list = readFile(desloc, path_file)
    print("Processo", type(process_list[0]))
    print("Processo", process_list[:10])
    print("Arquivo: %s" % trace_name(path_file))
    print("Quantidade de páginas: %s" % len(process_list))

    workingSet(process_list[:100], tam_conjunto)

if __name__ == "__main__":
    main()