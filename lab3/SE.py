from source import read
from lab3_operations import *
import os
path = os.path.dirname(os.path.abspath(__file__))

class SE:
    @staticmethod
    def result(path, Ci, Ni, e):
        C = CRT(Ci, Ni)
        M = root(C, e)
        return M


if __name__ == '__main__':
    path = f'{path}/vars/SE_vars/SE_RSA_1024_5_hard/11.txt'
    Ci, Ni = get_data(path)
    e = 5

    M = SE.result(path, Ci, Ni, e)

    for i in range(len(Ci)):
        print(hex(M**e % Ni[i]))
        print()
