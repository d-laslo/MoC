from source import read, inverse
from lab3_operations import *
import os
import gc
import re
from gmpy2 import mpz, powmod, invert, mul, t_mod
path = os.path.dirname(os.path.abspath(__file__))


class MitM:
    @staticmethod
    def result(C, N, e, l, num_sections = 1):
        l = l // 2

        C = mpz(C)
        N = mpz(N)
        T = 0
        S = 0

        quota_size = 2**l // num_sections
        
        try:
            for section in range(num_sections):
                for j in range(section, num_sections):
                    shift = quota_size*j
                    Ts = {powmod(mpz(i + shift), e, N): i for i in range(1, quota_size + 1)}
                    for Ti in Ts:
                        Si = t_mod(mul(C, invert(Ti, N)), N)
                        try:
                            S = quota_size * section + Ts[Si]
                            T = quota_size * j + Ts[Ti]
                        except:
                            continue
                        raise
                    Ts = {}
                    gc.collect()
        except:
            pass


        # Ts = [powmod(mpz(i), e, N) for i in range( 1, 2**l )]

        # for i in range(0, 2**l):
        #     Si = t_mod(mul(C, invert(Ts[i], N)), N)
        #     try:
        #         S = Ts.index(Si) + 1
        #         T = i + 1
        #         break
        #     except:
        #         pass
        
        if T == 0:
            print("Вiдкритий текст не було визначено")
            return 0

        return T, S





if __name__ == '__main__':
    path = f'{path}/vars/MitM_vars/MitM_RSA_2048_56_hard/11.txt'
    l = int(re.findall(r'RSA\_\d*\_(\d*)\_', path)[0])
    C, N = get_data(path)
    e = 65537

    T, S = MitM.result(C[0], N[0], e, l, 8)

    print(f'{T=}')
    print(f'{S=}')
    M = T * S
    print(hex(M**e % N[0]) == hex(C[0]))
    print()