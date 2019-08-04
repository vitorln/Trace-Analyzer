#coding: utf-8
from collections import defaultdict
import time

def hex2bin(hexdata):
    scale = 16
    num_of_bits = 8
    b = bin(int(hexdata, scale))[2:].zfill(num_of_bits)
    return b

def trace_name(path_file):
    idx = path_file.rfind('/')
    return path_file[idx+1:]


def read_file(page_size, path_file):
    d = {}
    count = 0
    with open(path_file) as f:
        for line in f:
            (key, val) = line.split()
            d[count] = (hex2bin(key)[:page_size])
            count += 1
    return d


def predict(frames, process_list, idx):
    res = -1
    farthest = idx
    for i, fr in enumerate(frames):
        j = 0
        for j in range(idx, len(process_list)):
            if frames[i] == process_list[j]:
                if j > farthest:
                    farthest = j
                    res = i
                break
        if j == len(process_list) - 1:
            return i

    return res if res != -1 else 0


def optimal(process_list, frames_size):
    frames = []
    hits = 0
    misses = 0
    for idx, page in process_list.items():
        if page in frames:
            hits += 1
            continue

        if len(frames) < frames_size:
            frames.append(page)
            misses += 1

        else:
            replace = predict(frames, process_list, idx + 1)
            frames[replace] = page
            misses += 1

    print('n hits = %s' % hits)
    print('n misses = %s' % misses)


def aprox_lru(process_list, frames_size):
    frames = []
    reference_bytes = [0] * frames_size
    hits = 0
    misses = 0
    for idx, page in process_list.items():

        if page in frames:
            hits += 1
            reference_bytes[frames.index(page)] = 1
            continue

        if len(frames) < frames_size:
            frames.append(page)
            misses += 1

        else:
            replace = reference_bytes.index(min(reference_bytes))
            frames[replace] = page
            misses += 1

    print('n hits = %s' % hits)
    print('n misses = %s' % misses)



# print("-------------------- Algoritmo Otimo -----------------------")
# start_time_opt = time.time()
# optimal(process_list, frames_size)
# optimal_time = (time.time() - start_time_opt)
# print("--- Execução: %s segundos ---" % optimal_time)

# print("-------------------- LRU Aproximado ------------------------")
# start_time_lru = time.time()
# aprox_lru(process_list, frames_size)
# lru_time = (time.time() - start_time_lru)
# print("--- Execução: %s segundos ---" % lru_time)



def main():
    path_file = "traces/gcc.trace.txt"
    frames_size = 4
    page_size = 16
    tam_conj_trabalho = 1000

    process_list = read_file(page_size, path_file)
    print("Processo", process_list)
    print("Arquivo: %s" % trace_name(path_file))
    print("Quantidade de páginas: %s" % len(process_list))


if __name__ == "__main__":
    main()