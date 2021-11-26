from source import inverse, read
import math 
import re
import gmpy

def CRT(remains, modules):
    M = 1
    for i in modules:
        M *= i

    Mi = [M // i for i in modules]
    invMi = [inverse(mi, pol) for mi, pol in zip(Mi, modules)]
    ri = [(r * mi * invmi) % M  for r, mi, invmi in zip(remains, Mi, invMi)]

    return sum(ri) % M


def root(num, root_n, e = 10):
    def pow(base, exp):
        itr = bin(exp)[2:][::-1]
        tmp = base
        result = 1
        for i in itr:
            if i == '1':
                result *= tmp
            tmp *= tmp
        return result

    x = [1, 0]

    n = root_n - 1

    while x[0] != x[1]:
        x[1] = (n * x[0] + num // x[0]**n) // root_n
        x[0], x[1] = x[1], x[0]

    return  x[0]
    

def get_data(path):
    data = read(path)
    return [int(i, 16) for i in re.findall(r'C\d*\s*=*\s*(0x[\d\w]*)', data)],\
            [int(i, 16) for i in re.findall(r'N\d*\s*=*\s*(0x[\d\w]*)', data)]