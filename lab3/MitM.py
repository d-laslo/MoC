from source import read, write
from lab3_operations import *
import os
import gc
import re
import json
import time
from gmpy2 import mpz, powmod, invert, mul, t_mod
path = os.path.dirname(os.path.abspath(__file__))


class MitM:
    @staticmethod
    def result(num_sections, pre_calc_path):
        

        # if not pre_calc_is_exist:
        #     MitM.__pre_calc(C, N, e, quota_size, num_sections)
        T = 0
        S = 0
        try:
            for section in range(num_sections):
                Ss = json.loads(read(f'{pre_calc_path}/{section}'))
                for j in range(section, num_sections):
                    Ts = json.loads(read(f'{pre_calc_path}/{j}'))
                    for Ti in Ts:
                        Si = Ts[Ti][1]
                        try:
                            S = Ss[Si][0]
                            T = Ts[Ti][0]
                        except:
                            continue
                        raise
                    Ts = {}
                    gc.collect()
                Ss = {}
                gc.collect()
        except Exception as exc:
            print(exc)
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

    @staticmethod
    def pre_calc(C, N, e, l, num_sections, path):
        l = l // 2

        C = mpz(C)
        N = mpz(N)
        T = 0
        S = 0

        quota_size = 2**l // num_sections
        for j in range(0, num_sections):
            shift = quota_size*j
            quota = {}
            for i in range(1, quota_size + 1):
                T = powmod(mpz(i + shift), e, N)
                S = t_mod(mul(C, invert(mpz(T), N)), N)
                quota[T.digits()] = [i + shift, S.digits()]
            
            write(f'{path}/{j}', json.dumps(quota))



if __name__ == '__main__':
    path_var = f'{path}/vars/MitM_vars/MitM_RSA_2048_56_hard/11.txt'
    l = int(re.findall(r'RSA\_\d*\_(\d*)\_', path_var)[0])
    C, N = get_data(path_var)
    e = 65537
    num_sections = 16


    st = time.time()
    MitM.pre_calc(C[0], N[0], e, l, num_sections, path)
    precalc_time = time.time() - st 
    print(f'{precalc_time}')
    print()

    st = time.time()
    T, S = MitM.result(num_sections, path)
    search_time = time.time() - st 
    print(f'{search_time}')
    print()

    print(f'{T=}')
    print(f'{S=}')
    M = T * S
    print(f'{M=}')
    print(hex(M**e % N[0]) == hex(C[0]))
    print()