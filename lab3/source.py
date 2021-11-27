import numpy as np
from copy import copy
import gmpy2
from math import log


def read(path):
    with open(path, 'r') as file:
        text = file.read()
        return text

def write(path, text):
    with open(path, 'w') as file:
        file.write(text)


def norm(x, pol):
    bx = bin(x)[2:]
    bpol = bin(pol)[2:]

    while len(bx) >= len(bpol):
        shift = len(bx) - len(bpol)
        x ^= pol << shift
        bx = bin(x)[2:]
    return x


def inverse(value, module):
    v = [0, 1]
    rem = 1
    a = module
    value %= module

    while rem > 0:
        tmp = a // value
        v[0] -= (v[1] * tmp) % module
        v[0], v[1] = v[1], v[0]
        rem = a % value
        a = value
        value = rem
    return v[0] % module


# def mul(x, y, n):
#     lg = log(n, 2)
#     if lg - int(lg) > 0:
#         raise
#     x_str = bin(x)[2:]
#     y_str = bin(y)[2:]

#     len_x = len(x_str)
#     len_y = len(y_str)

#     if len_x <= 32 or len_y <= 32:
#         return x * y

#     x_str = '0' * (n - len_x) + x_str
#     y_str = '0' * (n - len_y) + y_str

#     return karatsuba(x_str, y_str, n)



    
    


# def karatsuba(x, y, n):
#     if n == 32:
#         return int(x, 2) * int(y, 2)

#     half = n // 2

#     a = x[:half]
#     b = x[half:]

#     c = y[:half]
#     d = y[half:]

#     apb = bin(int(a, 2) + int(b, 2))[2:half + 2]
#     cpd = bin(int(c, 2) + int(d, 2))[2:half + 2]

#     a1 = karatsuba(apb, cpd, half)
#     ac = karatsuba(a, c, half)
#     bd = karatsuba(a, c, half)

#     return ((a1 - ac - bd) << half) + bd

 

if __name__ == '__main__':
    pass

    # a = int('0x3364db216e85f795553ef5f435e1f4b8fecd4156b620bbd221327a9242bacaff0fd525cb7bbbd48a3357d1e11832b672a68b61db213970f02bf9c07547267897d4e1721b465c4c2d221d4322e1faebb897285ceadb17bee30c2186b8fbc8e93b1e5247154c36a4773630c0119142b108057a2574aca941acd01a503d647d27b8', 16)
    # b = int('0xD54335E37FA477FABF27638338B0E7A76602850DE614BE3B208956FF9A862FFCFDF3DCA909310FE7EBD561C21E349CA9751ADDEE3D96C75CAED8050710946F737A1EDC2E58A0352D8767A735817022DBE3966A62210C26951603654B25B9F632FF14DA0AC8BB701DFEFE30AA2758927ED03871E86EFCF2C74EA863ED7674E9DB', 16)

    # mod = int('0xD8C2C535BBC67DCB5AD87E0F89EFE9E87C621C5A19E49E0A3F67079DA1BA312714D3A422A628B9D60A461D1AF646B72C22334304694800B1D4C70E1BEA5932B3273B0EC406016FAB0830691F14C754A6158423A745C439BFDB3473513D90EE75A7D1C16A70880B9BB0D03DD1282566273490C9F2987891B764C2787B5304E8BB', 16)

    # print(mul(a, b, 1024) % mod)