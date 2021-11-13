import os
#from lab2.frequency import bigram_frequency
from source import read, write
import json
from frequency import n_gram_frequency
import numpy as np
import zipfile

path = os.path.dirname(os.path.abspath(__file__))

class Criterion:
    def __init__(self, n_grams_frequency: dict[str,int]) -> None:
        self.__n_grams = sorted(n_grams_frequency, key=n_grams_frequency.get, reverse=True)
        self.__n_grams_len = len(self.__n_grams[0])
        self.__compliance_index_language = self.__compliance_index(n_grams_frequency)
        self.__n_grams_frequency = n_grams_frequency

    def __split_into_n_grams(self, text: str, n_grams_len: int) -> list[str]:
        return [text[i:i+n_grams_len] for i in range(len(text) - 1)]

    def __compliance_index(self, frequency: dict[str,int]) -> int:
        frequency_val = frequency.values()
        text_len = sum(frequency_val)
        return  sum([x * (x-1) for x in frequency_val]) / (text_len * (text_len - 1))

    def criterian20(self, text: str, set_size: int) -> bool: #10: 1, 100: ~1, 1000: ~30, 10000: 210
        return self.criterian21(text, set_size, set_size)

    def criterian21(self, text: str, set_size: int, threshold: int) -> bool: # 10: <50, 1>, 100: <5, 2>, 1000: <50, 49>, 10000: <210, 210>
        text_n_grams = set(self.__split_into_n_grams(text, self.__n_grams_len))
        allowed_n_grams = set(self.__n_grams[:set_size])
        tmp = len(text_n_grams & allowed_n_grams)
        #print(tmp)
        if len(text_n_grams & allowed_n_grams) < threshold:
            return False
        return True

    def criterian22(self, text: str, set_size: int, threshold: int) -> bool: # 10: <1, 1>, 100: <1, 1>, 1000: <5, 4>, 10000: <30, 40>
        text_n_grams = self.__split_into_n_grams(text, self.__n_grams_len)
        allowed_n_grams = set(self.__n_grams[:set_size])

        frequencies = sorted([text_n_grams.count(i) for i in allowed_n_grams])
        #print(frequencies[0])
        if frequencies[0] >= threshold:
            return True
        return False

    def criterian23(self, text: str, set_size: int, thresholds: list[int]) -> bool: # 10: <30, 1>, 100: <7, 4>, 1000: <20, 150>, 10000: <20, 1700>
        text_n_grams = self.__split_into_n_grams(text, self.__n_grams_len)
        allowed_n_grams = set(self.__n_grams[:set_size])

        frequencies = sorted([text_n_grams.count(i) for i in allowed_n_grams])
        #print(sum(frequencies))
        if sum(frequencies) >= thresholds:
            return True
        return False

    def criterian40(self, text: str, threshold: int) -> bool: #10: .03, 100: .003, 1000: .001, 10000: .00035
        I = self.__compliance_index(n_gram_frequency(text, self.__n_grams_len))
        #print(abs(I - self.__compliance_index_language))
        if abs(I - self.__compliance_index_language) > threshold:
            return False
        return True

    def criterian50(self, text: str, set_size: int, threshold: int) -> bool: # 10: <500, 497>, 100: <100, 99>, 1000: <50, 49>, 10000: <50, 47>
        allowed_n_grams = set(self.__n_grams[-set_size:])
        frequency = n_gram_frequency(text, self.__n_grams_len)

        count = len(set(frequency.keys()) & allowed_n_grams)
        #print(set_size - count)
        if (set_size - count) <= threshold:
            return False
        return True
    
    def structuralCriterian(self, path_to_text: str, threshold: float) -> bool: # 10: --, 100: --, 1000: 48, 10000: 66.2
        archive = zipfile.ZipFile(f'{path}/tmp.zip', 'w', zipfile.ZIP_DEFLATED)
        archive.write(path_to_text)
        archive.close()
        tt = os.stat(path_to_text).st_size
        ttt = os.stat(f'{path}/tmp.zip').st_size
        statinfo = 100 * abs(os.stat(path_to_text).st_size - os.stat(f'{path}/tmp.zip').st_size) / os.stat(path_to_text).st_size
        #print(statinfo)
        if statinfo > threshold:
            return True
        return False


def testTrue(result_name, path, N, criteria, *parameters):
    res = []
    for n in range(N):
        res.append(criteria(read(f'{path}{n + 1}'), *parameters))
    print(f'{result_name}{res.count(True)}                  {res.count(True)}/10000 = {res.count(True)/10000}')

def testFalse(result_name, path, N, criteria, *parameters):
    res = []
    for n in range(N):
        res.append(criteria(read(f'{path}{n + 1}'), *parameters))
    print(f'{result_name}{res.count(False)}                  {res.count(False)}/10000 = {res.count(False)/10000}')

def testTrueStructural(result_name, path, N, criteria, *parameters):
    res = []
    for n in range(N):
        res.append(criteria(f'{path}{n + 1}', *parameters))
    print(f'{result_name}{res.count(True)}                  {res.count(True)}/10000 = {res.count(True)/10000}')

def testFalseStructural(result_name, path, N, criteria, *parameters):
    res = []
    for n in range(N):
        res.append(criteria(f'{path}{n + 1}', *parameters))
    print(f'{result_name}{res.count(False)}                  {res.count(False)}/10000 = {res.count(False)/10000}')

def letter_affine_L10(criterion):
    p = 1
    testFalse(f'criterian20 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, criterion.criterian20, p)
    testTrue(f'criterian20 Y/affine/L_10: ', f'{path}/texts/Y/affine/L_10_N_', 10000, criterion.criterian20, p)

    size = 4
    p = 1
    testFalse(f'criterian21 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, criterion.criterian21, size, p)
    testTrue(f'criterian21 Y/affine/L_10: ', f'{path}/texts/Y/affine/L_10_N_', 10000, criterion.criterian21, size, p)

    size = 1
    p = 1
    testFalse(f'criterian22 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, criterion.criterian22, size, p)
    testTrue(f'criterian22 Y/affine/L_10: ', f'{path}/texts/Y/affine/L_10_N_', 10000, criterion.criterian22, size, p)

    size = 7
    p = 3
    testFalse(f'criterian23 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, criterion.criterian23, size, p)
    testTrue(f'criterian23 Y/affine/L_10: ', f'{path}/texts/Y/affine/L_10_N_', 10000, criterion.criterian23, size, p)

    p = .03
    testFalse(f'criterian40 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, criterion.criterian40, p)
    testTrue(f'criterian40 Y/affine/L_10: ', f'{path}/texts/Y/affine/L_10_N_', 10000, criterion.criterian40, p)
    
    size = 20
    p = 16
    testFalse(f'criterian50 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, criterion.criterian50, size, p)
    testTrue(f'criterian50 Y/affine/L_10: ', f'{path}/texts/Y/affine/L_10_N_', 10000, criterion.criterian50, size, p)

    p = 1015
    testFalseStructural('structural X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, criterion.structuralCriterian, p)
    testTrueStructural('structural Y/L_10: ', f'{path}/texts/Y/affine/L_10_N_', 10000, criterion.structuralCriterian, p)
   
def letter_affine_L100(criterion):
    p = 1
    testFalse(f'criterian20 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, criterion.criterian20, p)
    testTrue(f'criterian20 Y/affine/L_100: ', f'{path}/texts/Y/affine/L_100_N_', 10000, criterion.criterian20, p)

    size = 1
    p = 1
    testFalse(f'criterian21 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, criterion.criterian21, size, p)
    testTrue(f'criterian21 Y/affine/L_100: ', f'{path}/texts/Y/affine/L_100_N_', 10000, criterion.criterian21, size, p)

    size = 5
    p = 1
    testFalse(f'criterian22 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, criterion.criterian22, size, p)
    testTrue(f'criterian22 Y/affine/L_100: ', f'{path}/texts/Y/affine/L_100_N_', 10000, criterion.criterian22, size, p)

    size = 1
    p = 2
    testFalse(f'criterian23 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, criterion.criterian23, size, p)
    testTrue(f'criterian23 Y/affine/L_100: ', f'{path}/texts/Y/affine/L_100_N_', 10000, criterion.criterian23, size, p)

    p = 0.02
    testFalse(f'criterian40 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, criterion.criterian40, p)
    testTrue(f'criterian40 Y/affine/L_100: ', f'{path}/texts/Y/affine/L_100_N_', 10000, criterion.criterian40, p)
    
    size = 100
    p = 71
    testFalse(f'criterian50 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, criterion.criterian50, size, p)
    testTrue(f'criterian50 Y/affine/L_100: ', f'{path}/texts/Y/affine/L_100_N_', 10000, criterion.criterian50, size, p)

    p = 57.5
    testFalseStructural('structural X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, criterion.structuralCriterian, p)
    testTrueStructural('structural Y/affine/L_100_N_: ', f'{path}/texts/Y/affine/L_100_N_', 10000, criterion.structuralCriterian, p)
   
def letter_affine_L1000(criterion):
    p = 3
    testFalse(f'criterian20 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, criterion.criterian20, p)
    testTrue(f'criterian20 Y/affine/L_1000: ', f'{path}/texts/Y/affine/L_1000_N_', 10000, criterion.criterian20, p)

    size = 3
    p = 3
    testFalse(f'criterian21 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, criterion.criterian21, size, p)
    testTrue(f'criterian21 Y/affine/L_1000: ', f'{path}/texts/Y/affine/L_1000_N_', 10000, criterion.criterian21, size, p)

    size = 5
    p = 30
    testFalse(f'criterian22 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, criterion.criterian22, size, p)
    testTrue(f'criterian22 Y/affine/L_1000: ', f'{path}/texts/Y/affine/L_1000_N_', 10000, criterion.criterian22, size, p)

    size = 5
    p = 340
    testFalse(f'criterian23 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, criterion.criterian23, size, p)
    testTrue(f'criterian23 Y/affine/L_1000: ', f'{path}/texts/Y/affine/L_1000_N_', 10000, criterion.criterian23, size, p)

    p = 0.005
    testFalse(f'criterian40 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, criterion.criterian40, p)
    testTrue(f'criterian40 Y/affine/L_1000: ', f'{path}/texts/Y/affine/L_1000_N_', 10000, criterion.criterian40, p)
    
    size = 1000
    p = 967 #problem
    testFalse(f'criterian50 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, criterion.criterian50, size, p)
    testTrue(f'criterian50 Y/affine/L_1000: ', f'{path}/texts/Y/affine/L_1000_N_', 10000, criterion.criterian50, size, p)

    p = 49.0
    testFalseStructural('structural X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, criterion.structuralCriterian, p)
    testTrueStructural('structural Y/affine/L_1000: ', f'{path}/texts/Y/affine/L_1000_N_', 10000, criterion.structuralCriterian, p)

def letter_affine_L10000(criterion):
    p = 3
    testFalse(f'criterian20 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, criterion.criterian20, p)
    testTrue(f'criterian20 Y/affine/L_10000: ', f'{path}/texts/Y/affine/L_10000_N_', 1000, criterion.criterian20, p)

    size = 100
    p = 32
    testFalse(f'criterian21 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, criterion.criterian21, size, p)
    testTrue(f'criterian21 Y/affine/L_10000: ', f'{path}/texts/Y/affine/L_10000_N_', 1000, criterion.criterian21, size, p)

    size = 100
    p = 30
    testFalse(f'criterian22 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, criterion.criterian22, size, p)
    testTrue(f'criterian22 Y/affine/L_10000: ', f'{path}/texts/Y/affine/L_10000_N_', 1000, criterion.criterian22, size, p)

    size = 10
    p = 6000
    testFalse(f'criterian23 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, criterion.criterian23, size, p)
    testTrue(f'criterian23 Y/affine/L_10000: ', f'{path}/texts/Y/affine/L_10000_N_', 1000, criterion.criterian23, size, p)

    p = 0.0005
    testFalse(f'criterian40 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, criterion.criterian40, p)
    testTrue(f'criterian40 Y/affine/L_10000: ', f'{path}/texts/Y/affine/L_10000_N_', 1000, criterion.criterian40, p)
    
    size = 100
    p = 67 #problem
    testFalse(f'criterian50 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, criterion.criterian50, size, p)
    testTrue(f'criterian50 Y/affine/L_10000: ', f'{path}/texts/Y/affine/L_10000_N_', 1000, criterion.criterian50, size, p)

    p = 66
    testFalseStructural('structural X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, criterion.structuralCriterian, p)
    testTrueStructural('structural Y/affine/L_10000: ', f'{path}/texts/Y/affine/L_10000_N_', 1000, criterion.structuralCriterian, p)

def letter_recursive_L10(criterion):
    p = 1
    testFalse(f'criterian20 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, criterion.criterian20, p)
    testTrue(f'criterian20 Y/recursive/L_10: ', f'{path}/texts/Y/recursive/L_10_N_', 10000, criterion.criterian20, p)

    size = 5
    p = 2
    testFalse(f'criterian21 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, criterion.criterian21, size, p)
    testTrue(f'criterian21 Y/recursive/L_10: ', f'{path}/texts/Y/recursive/L_10_N_', 10000, criterion.criterian21, size, p)

    size = 1
    p = 1
    testFalse(f'criterian22 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, criterion.criterian22, size, p)
    testTrue(f'criterian22 Y/recursive/L_10: ', f'{path}/texts/Y/recursive/L_10_N_', 10000, criterion.criterian22, size, p)

    size = 7
    p = 4
    testFalse(f'criterian23 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, criterion.criterian23, size, p)
    testTrue(f'criterian23 Y/recursive/L_10: ', f'{path}/texts/Y/recursive/L_10_N_', 10000, criterion.criterian23, size, p)

    p = .03
    testFalse(f'criterian40 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, criterion.criterian40, p)
    testTrue(f'criterian40 Y/recursive/L_10: ', f'{path}/texts/Y/recursive/L_10_N_', 10000, criterion.criterian40, p)
    
    size = 20
    p = 16
    testFalse(f'criterian50 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, criterion.criterian50, size, p)
    testTrue(f'criterian50 Y/recursive/L_10: ', f'{path}/texts/Y/recursive/L_10_N_', 10000, criterion.criterian50, size, p)

    p = 1015
    testFalseStructural('structural X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, criterion.structuralCriterian, p)
    testTrueStructural('structural Y/recursive/L_10: ', f'{path}/texts/Y/recursive/L_10_N_', 10000, criterion.structuralCriterian, p)
    
   

def letter_recursive_L100(criterion):
    p = 3
    testFalse(f'criterian20 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, criterion.criterian20, p)
    testTrue(f'criterian20 Y/recursive/L_100: ', f'{path}/texts/Y/recursive/L_100_N_', 10000, criterion.criterian20, p)

    size = 10
    p = 8
    testFalse(f'criterian21 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, criterion.criterian21, size, p)
    testTrue(f'criterian21 Y/recursive/L_100: ', f'{path}/texts/Y/recursive/L_100_N_', 10000, criterion.criterian21, size, p)

    size = 5
    p = 1
    testFalse(f'criterian22 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, criterion.criterian22, size, p)
    testTrue(f'criterian22 Y/recursive/L_100: ', f'{path}/texts/Y/recursive/L_100_N_', 10000, criterion.criterian22, size, p)

    size = 3
    p = 17
    testFalse(f'criterian23 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, criterion.criterian23, size, p)
    testTrue(f'criterian23 Y/recursive/L_100: ', f'{path}/texts/Y/recursive/L_100_N_', 10000, criterion.criterian23, size, p)

    p = 0.005
    testFalse(f'criterian40 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, criterion.criterian40, p)
    testTrue(f'criterian40 Y/recursive/L_100: ', f'{path}/texts/Y/recursive/L_100_N_', 10000, criterion.criterian40, p)
    
    size = 10
    p = 4
    testFalse(f'criterian50 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, criterion.criterian50, size, p)
    testTrue(f'criterian50 Y/recursive/L_100: ', f'{path}/texts/Y/recursive/L_100_N_', 10000, criterion.criterian50, size, p)

    p = 58
    testFalseStructural('structural X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, criterion.structuralCriterian, p)
    testTrueStructural('structural Y/recursive/L_100_N_: ', f'{path}/texts/Y/recursive/L_100_N_', 10000, criterion.structuralCriterian, p)


def letter_recursive_L1000(criterion):
    p = 3
    testFalse(f'criterian20 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, criterion.criterian20, p)
    testTrue(f'criterian20 Y/recursive/L_1000: ', f'{path}/texts/Y/recursive/L_1000_N_', 10000, criterion.criterian20, p)

    size = 10
    p = 8
    testFalse(f'criterian21 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, criterion.criterian21, size, p)
    testTrue(f'criterian21 Y/recursive/L_1000: ', f'{path}/texts/Y/recursive/L_1000_N_', 10000, criterion.criterian21, size, p)

    size = 5
    p = 1
    testFalse(f'criterian22 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, criterion.criterian22, size, p)
    testTrue(f'criterian22 Y/recursive/L_1000: ', f'{path}/texts/Y/recursive/L_1000_N_', 10000, criterion.criterian22, size, p)

    size = 3
    p = 190
    testFalse(f'criterian23 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, criterion.criterian23, size, p)
    testTrue(f'criterian23 Y/recursive/L_1000: ', f'{path}/texts/Y/recursive/L_1000_N_', 10000, criterion.criterian23, size, p)

    p = 0.005
    testFalse(f'criterian40 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, criterion.criterian40, p)
    testTrue(f'criterian40 Y/recursive/L_1000: ', f'{path}/texts/Y/recursive/L_1000_N_', 10000, criterion.criterian40, p)
    
    size = 100
    p = 68 #promlem
    testFalse(f'criterian50 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, criterion.criterian50, size, p)
    testTrue(f'criterian50 Y/recursive/L_1000: ', f'{path}/texts/Y/recursive/L_1000_N_', 10000, criterion.criterian50, size, p)

    p = 49
    testFalseStructural('structural X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, criterion.structuralCriterian, p)
    testTrueStructural('structural Y/recursive/L_1000_N_: ', f'{path}/texts/Y/recursive/L_1000_N_', 10000, criterion.structuralCriterian, p)

def letter_recursive_L10000(criterion):
    p = 3
    testFalse(f'criterian20 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, criterion.criterian20, p)
    testTrue(f'criterian20 Y/recursive/L_10000: ', f'{path}/texts/Y/recursive/L_10000_N_', 1000, criterion.criterian20, p)

    size = 100
    p = 32
    testFalse(f'criterian21 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, criterion.criterian21, size, p)
    testTrue(f'criterian21 Y/recursive/L_10000: ', f'{path}/texts/Y/recursive/L_10000_N_', 1000, criterion.criterian21, size, p)

    size = 10
    p = 350
    testFalse(f'criterian22 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, criterion.criterian22, size, p)
    testTrue(f'criterian22 Y/recursive/L_10000: ', f'{path}/texts/Y/recursive/L_10000_N_', 1000, criterion.criterian22, size, p)

    size = 10
    p = 5900
    testFalse(f'criterian23 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, criterion.criterian23, size, p)
    testTrue(f'criterian23 Y/recursive/L_10000: ', f'{path}/texts/Y/recursive/L_10000_N_', 1000, criterion.criterian23, size, p)

    p = 0.001
    testFalse(f'criterian40 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, criterion.criterian40, p)
    testTrue(f'criterian40 Y/recursive/L_10000: ', f'{path}/texts/Y/recursive/L_10000_N_', 1000, criterion.criterian40, p)
    
    size = 200
    p = 167 #problem
    testFalse(f'criterian50 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, criterion.criterian50, size, p)
    testTrue(f'criterian50 Y/recursive/L_10000: ', f'{path}/texts/Y/recursive/L_10000_N_', 1000, criterion.criterian50, size, p)

    p = 66 #problem
    testFalseStructural('structural X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, criterion.structuralCriterian, p)
    testTrueStructural('structural Y/recursive/L_10000: ', f'{path}/texts/Y/recursive/L_10000_N_', 1000, criterion.structuralCriterian, p)

def letter_uniform_L10(criterion):
    p = 1
    testFalse(f'criterian20 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, criterion.criterian20, p)
    testTrue(f'criterian20 Y/uniform/L_10: ', f'{path}/texts/Y/uniform/L_10_N_', 10000, criterion.criterian20, p)

    size = 7
    p = 3
    testFalse(f'criterian21 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, criterion.criterian21, size, p)
    testTrue(f'criterian21 Y/uniform/L_10: ', f'{path}/texts/Y/uniform/L_10_N_', 10000, criterion.criterian21, size, p)

    size = 1
    p = 1
    testFalse(f'criterian22 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, criterion.criterian22, size, p)
    testTrue(f'criterian22 Y/uniform/L_10: ', f'{path}/texts/Y/uniform/L_10_N_', 10000, criterion.criterian22, size, p)

    size = 7
    p = 4
    testFalse(f'criterian23 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, criterion.criterian23, size, p)
    testTrue(f'criterian23 Y/uniform/L_10: ', f'{path}/texts/Y/uniform/L_10_N_', 10000, criterion.criterian23, size, p)

    p = .028
    testFalse(f'criterian40 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, criterion.criterian40, p)
    testTrue(f'criterian40 Y/uniform/L_10: ', f'{path}/texts/Y/uniform/L_10_N_', 10000, criterion.criterian40, p)
    
    size = 20
    p = 16
    testFalse(f'criterian50 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, criterion.criterian50, size, p)
    testTrue(f'criterian50 Y/uniform/L_10: ', f'{path}/texts/Y/uniform/L_10_N_', 10000, criterion.criterian50, size, p)

    p = 1015 #problem
    testFalseStructural('structural X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, criterion.structuralCriterian, p)
    testTrueStructural('structural Y/uniform/L_10: ', f'{path}/texts/Y/uniform/L_10_N_', 10000, criterion.structuralCriterian, p)

def letter_uniform_L100(criterion):
    p = 18
    testFalse(f'criterian20 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, criterion.criterian20, p)
    testTrue(f'criterian20 Y/uniform/L_100: ', f'{path}/texts/Y/uniform/L_100_N_', 10000, criterion.criterian20, p)

    size = 20
    p = 19
    testFalse(f'criterian21 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, criterion.criterian21, size, p)
    testTrue(f'criterian21 Y/uniform/L_100: ', f'{path}/texts/Y/uniform/L_100_N_', 10000, criterion.criterian21, size, p)

    size = 5
    p = 3
    testFalse(f'criterian22 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, criterion.criterian22, size, p)
    testTrue(f'criterian22 Y/uniform/L_100: ', f'{path}/texts/Y/uniform/L_100_N_', 10000, criterion.criterian22, size, p)

    size = 5
    p = 20
    testFalse(f'criterian23 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, criterion.criterian23, size, p)
    testTrue(f'criterian23 Y/uniform/L_100: ', f'{path}/texts/Y/uniform/L_100_N_', 10000, criterion.criterian23, size, p)

    p = .01
    testFalse(f'criterian40 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, criterion.criterian40, p)
    testTrue(f'criterian40 Y/uniform/L_100: ', f'{path}/texts/Y/uniform/L_100_N_', 10000, criterion.criterian40, p)
    
    size = 20
    p = 3
    testFalse(f'criterian50 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, criterion.criterian50, size, p)
    testTrue(f'criterian50 Y/uniform/L_100: ', f'{path}/texts/Y/uniform/L_100_N_', 10000, criterion.criterian50, size, p)

    p = 60 #problem
    testFalseStructural('structural X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, criterion.structuralCriterian, p)
    testTrueStructural('structural Y/uniform/L_100: ', f'{path}/texts/Y/uniform/L_100_N_', 10000, criterion.structuralCriterian, p)

def letter_uniform_L1000(criterion):
    p = 18
    testFalse(f'criterian20 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, criterion.criterian20, p)
    testTrue(f'criterian20 Y/uniform/L_1000: ', f'{path}/texts/Y/uniform/L_1000_N_', 10000, criterion.criterian20, p)

    size = 20
    p = 20
    testFalse(f'criterian21 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, criterion.criterian21, size, p)
    testTrue(f'criterian21 Y/uniform/L_1000: ', f'{path}/texts/Y/uniform/L_1000_N_', 10000, criterion.criterian21, size, p)

    size = 5
    p = 32
    testFalse(f'criterian22 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, criterion.criterian22, size, p)
    testTrue(f'criterian22 Y/uniform/L_1000: ', f'{path}/texts/Y/uniform/L_1000_N_', 10000, criterion.criterian22, size, p)

    size = 5
    p = 200
    testFalse(f'criterian23 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, criterion.criterian23, size, p)
    testTrue(f'criterian23 Y/uniform/L_1000: ', f'{path}/texts/Y/uniform/L_1000_N_', 10000, criterion.criterian23, size, p)

    p = .01
    testFalse(f'criterian40 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, criterion.criterian40, p)
    testTrue(f'criterian40 Y/uniform/L_1000: ', f'{path}/texts/Y/uniform/L_1000_N_', 10000, criterion.criterian40, p)
    
    size = 500
    p = 467 #problem
    testFalse(f'criterian50 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, criterion.criterian50, size, p)
    testTrue(f'criterian50 Y/uniform/L_1000: ', f'{path}/texts/Y/uniform/L_1000_N_', 10000, criterion.criterian50, size, p)

    p = 47.5
    testFalseStructural('structural X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, criterion.structuralCriterian, p)
    testTrueStructural('structural Y/uniform/L_1000: ', f'{path}/texts/Y/uniform/L_1000_N_', 10000, criterion.structuralCriterian, p)

def letter_uniform_L10000(criterion):
    p = 18
    testFalse(f'criterian20 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, criterion.criterian20, p)
    testTrue(f'criterian20 Y/uniform/L_10000: ', f'{path}/texts/Y/uniform/L_10000_N_', 1000, criterion.criterian20, p)

    size = 20
    p = 20
    testFalse(f'criterian21 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, criterion.criterian21, size, p)
    testTrue(f'criterian21 Y/uniform/L_10000: ', f'{path}/texts/Y/uniform/L_10000_N_', 1000, criterion.criterian21, size, p)

    size = 5
    p = 550
    testFalse(f'criterian22 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, criterion.criterian22, size, p)
    testTrue(f'criterian22 Y/uniform/L_10000: ', f'{path}/texts/Y/uniform/L_10000_N_', 1000, criterion.criterian22, size, p)

    size = 5
    p = 3600
    testFalse(f'criterian23 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, criterion.criterian23, size, p)
    testTrue(f'criterian23 Y/uniform/L_10000: ', f'{path}/texts/Y/uniform/L_10000_N_', 1000, criterion.criterian23, size, p)

    p = .01
    testFalse(f'criterian40 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, criterion.criterian40, p)
    testTrue(f'criterian40 Y/uniform/L_10000: ', f'{path}/texts/Y/uniform/L_10000_N_', 1000, criterion.criterian40, p)
    
    size = 500
    p = 467 #problem
    testFalse(f'criterian50 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, criterion.criterian50, size, p)
    testTrue(f'criterian50 Y/uniform/L_10000: ', f'{path}/texts/Y/uniform/L_10000_N_', 1000, criterion.criterian50, size, p)

    p = 54.7
    testFalseStructural('structural X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, criterion.structuralCriterian, p)
    testTrueStructural('structural Y/uniform/L_10000: ', f'{path}/texts/Y/uniform/L_10000_N_', 1000, criterion.structuralCriterian, p)

def letter_vigenere_L10(criterion):
    pass

def letter_vigenere_L100(criterion):
    pass

def letter_vigenere_L1000(criterion):
    pass    

def letter_vigenere_L10000(criterion):
    pass



def main_test():
    letters_frequency = json.loads(read(f'{path}/result/letter_frequency.json'))
    criterion = Criterion(letters_frequency)
    print("letters:")
    letter_affine_L10(criterion)
    letter_affine_L100(criterion)
    letter_affine_L1000(criterion)
    letter_affine_L10000(criterion)

    letter_recursive_L10(criterion)
    letter_recursive_L100(criterion)
    letter_recursive_L1000(criterion)
    letter_recursive_L10000(criterion)
    
    letter_uniform_L10(criterion)
    letter_uniform_L100(criterion)
    letter_uniform_L1000(criterion)
    letter_uniform_L10000(criterion)
    
    letter_vigenere_L1000(criterion)
    letter_vigenere_L10000(criterion)



    #criterian20
    # name = 'criterian20'
    # p_L10 = 1
    # p_L100 = 1
    # p_L1000 = 22
    # p_L10000 = 30
    # letter_raw(name,criterion.criterian20,p_L10,p_L100,p_L1000,p_L10000)
    # letter_affine(name, criterion.criterian20,p_L10,p_L100,p_L1000,p_L10000)

    # p_L10 = 1
    # p_L100 = 3
    # p_L1000 = 30
    # p_L10000 = 30
    # letter_raw(name,criterion.criterian20,p_L10,p_L100,p_L1000,p_L10000)
    # letter_recursive(name,criterion.criterian20,p_L10,p_L100,p_L1000,p_L10000)

    # p_L10 = 1
    # p_L100 = 18
    # p_L1000 = 30
    # p_L10000 = 30
    # letter_raw(name,criterion.criterian20,p_L10,p_L100,p_L1000,p_L10000)
    # letter_uniform(name,criterion.criterian20,p_L10,p_L100,p_L1000,p_L10000)

    # p_L10 = 1
    # p_L100 = 7
    # p_L1000 = 31
    # p_L10000 = 31 #problem here
    # letter_raw(name,criterion.criterian20,p_L10,p_L100,p_L1000,p_L10000)
    # letter_vigenere(name, criterion, 1, p_L10, p_L100, p_L1000, p_L10000)

    # p_L10 = 1
    # p_L100 = 8
    # p_L1000 = 31
    # p_L10000 = 32
    # letter_raw(name,criterion.criterian20,p_L10,p_L100,p_L1000,p_L10000)
    # letter_vigenere(name, criterion, 5, p_L10, p_L100, p_L1000, p_L10000)

    # p_L10 = 1
    # p_L100 = 15
    # p_L1000 = 31
    # p_L10000 = 32
    # letter_raw(name,criterion.criterian20,p_L10,p_L100,p_L1000,p_L10000)
    # letter_vigenere(name, criterion, 10, p_L10, p_L100, p_L1000, p_L10000)

    #criterian21
    # name = 'criterian21'
    # size = 9
    # p_L10 = 1
    # p_L100 = 1
    # p_L1000 = 30
    # p_L10000 = 30
    # letter_raw_extraSize(name,criterion.criterian21,p_L10,p_L100,p_L1000,p_L10000,size)
    # letter_affine_extraSize(name, criterion.criterian21,p_L10,p_L100,p_L1000,p_L10000,size)

    # p_L10 = 1
    # p_L100 = 3
    # p_L1000 = 10
    # p_L10000 = 30
    # letter_raw(name,criterion.criterian21,p_L10,p_L100,p_L1000,p_L10000)
    # letter_recursive(name,criterion.criterian21,p_L10,p_L100,p_L1000,p_L10000)

    # p_L10 = 1
    # p_L100 = 16
    # p_L1000 = 25
    # p_L10000 = 30
    # letter_raw(name,criterion.criterian20,p_L10,p_L100,p_L1000,p_L10000)
    # letter_uniform(name,criterion.criterian20,p_L10,p_L100,p_L1000,p_L10000)

    # p_L10 = 1
    # p_L100 = 7
    # p_L1000 = 29
    # p_L10000 = 31
    # letter_raw(name,criterion.criterian20,p_L10,p_L100,p_L1000,p_L10000)
    # letter_vigenere(name, criterion, 1, p_L10, p_L100, p_L1000, p_L10000)

    # p_L10 = 1
    # p_L100 = 8
    # p_L1000 = 30
    # p_L10000 = 32
    # letter_raw(name,criterion.criterian20,p_L10,p_L100,p_L1000,p_L10000)
    # letter_vigenere(name, criterion, 5, p_L10, p_L100, p_L1000, p_L10000)

    # p_L10 = 1
    # p_L100 = 15
    # p_L1000 = 31
    # p_L10000 = 32
    # letter_raw(name,criterion.criterian20,p_L10,p_L100,p_L1000,p_L10000)
    # letter_vigenere(name, criterion, 10, p_L10, p_L100, p_L1000, p_L10000)

    #criteria22
    name = 'criterian22'
    # p_L10 = 1
    # p_L100 = 1
    # p_L1000 = 30
    # p_L10000 = 30
    # letter_raw(name,criterion.criterian20,p_L10,p_L100,p_L1000,p_L10000)
    # letter_affine(name, criterion.criterian20,p_L10,p_L100,p_L1000,p_L10000)

    # p_L10 = 1
    # p_L100 = 3
    # p_L1000 = 10
    # p_L10000 = 30
    # letter_raw(name,criterion.criterian20,p_L10,p_L100,p_L1000,p_L10000)
    # letter_recursive(name,criterion.criterian20,p_L10,p_L100,p_L1000,p_L10000)

    # p_L10 = 1
    # p_L100 = 16
    # p_L1000 = 25
    # p_L10000 = 30
    # letter_raw(name,criterion.criterian20,p_L10,p_L100,p_L1000,p_L10000)
    # letter_uniform(name,criterion.criterian20,p_L10,p_L100,p_L1000,p_L10000)

    # p_L10 = 1
    # p_L100 = 7
    # p_L1000 = 29
    # p_L10000 = 31
    # letter_raw(name,criterion.criterian20,p_L10,p_L100,p_L1000,p_L10000)
    # letter_vigenere(name, criterion, 1, p_L10, p_L100, p_L1000, p_L10000)

    # p_L10 = 1
    # p_L100 = 8
    # p_L1000 = 30
    # p_L10000 = 32
    # letter_raw(name,criterion.criterian20,p_L10,p_L100,p_L1000,p_L10000)
    # letter_vigenere(name, criterion, 5, p_L10, p_L100, p_L1000, p_L10000)

    # p_L10 = 1
    # p_L100 = 15
    # p_L1000 = 31
    # p_L10000 = 32
    # letter_raw(name,criterion.criterian20,p_L10,p_L100,p_L1000,p_L10000)
    # letter_vigenere(name, criterion, 10, p_L10, p_L100, p_L1000, p_L10000)


    # test('criterian21 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, criterion.criterian21, 50, 6)
    # test('criterian21 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, criterion.criterian21, 50, 23)
    # test('criterian21 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, criterion.criterian21, 50, 30)
    # test('criterian21 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, criterion.criterian21, 50, 32)
    # test('criterian21 Y/affine/L_10: ', f'{path}/texts/Y/affine/L_10_N_', 10000, criterion.criterian21, 50, 6)
    # test('criterian21 Y/affine/L_100: ', f'{path}/texts/Y/affine/L_100_N_', 10000, criterion.criterian21, 50, 23)
    # test('criterian21 Y/affine/L_1000: ', f'{path}/texts/Y/affine/L_1000_N_', 10000, criterion.criterian21, 50, 30)
    # test('criterian21 Y/affine/L_10000: ', f'{path}/texts/Y/affine/L_10000_N_', 1000, criterion.criterian21, 50, 32)
    # test('criterian21 Y/recursive/L_10: ', f'{path}/texts/Y/recursive/L_10_N_', 10000, criterion.criterian21, 50, 6)
    # test('criterian21 Y/recursive/L_100: ', f'{path}/texts/Y/recursive/L_100_N_', 10000, criterion.criterian21, 50, 23)
    # test('criterian21 Y/recursive/L_1000: ', f'{path}/texts/Y/recursive/L_1000_N_', 10000, criterion.criterian21, 50, 30)
    # test('criterian21 Y/recursive/L_10000: ', f'{path}/texts/Y/recursive/L_10000_N_', 1000, criterion.criterian21,50, 32)
    # test('criterian21 Y/uniform/L_10: ', f'{path}/texts/Y/uniform/L_10_N_', 10000, criterion.criterian21, 50, 6)
    # test('criterian21 Y/uniform/L_100: ', f'{path}/texts/Y/uniform/L_100_N_', 10000, criterion.criterian21, 50, 23)
    # test('criterian21 Y/uniform/L_1000: ', f'{path}/texts/Y/uniform/L_1000_N_', 10000, criterion.criterian21, 50, 30)
    # test('criterian21 Y/uniform/L_10000: ', f'{path}/texts/Y/uniform/L_10000_N_', 1000, criterion.criterian21, 50, 32)
    # test('criterian21 Y/vigenere/KEY_1_L_10: ', f'{path}/texts/Y/vigenere/KEY_1_L_10_N_', 10000, criterion.criterian21, 50, 6)
    # test('criterian21 Y/vigenere/KEY_1_L_100: ', f'{path}/texts/Y/vigenere/KEY_1_L_100_N_', 10000, criterion.criterian21, 50, 23)
    # test('criterian21 Y/vigenere/KEY_1_L_1000: ', f'{path}/texts/Y/vigenere/KEY_1_L_1000_N_', 10000, criterion.criterian21, 50, 30)
    # test('criterian21 Y/vigenere/KEY_1_L_10000: ', f'{path}/texts/Y/vigenere/KEY_1_L_10000_N_', 1000, criterion.criterian21, 50, 32)
    # test('criterian21 Y/vigenere/KEY_5_L_10: ', f'{path}/texts/Y/vigenere/KEY_5_L_10_N_', 10000, criterion.criterian21, 50, 6)
    # test('criterian21 Y/vigenere/KEY_5_L_100: ', f'{path}/texts/Y/vigenere/KEY_5_L_100_N_', 10000, criterion.criterian21, 50, 23)
    # test('criterian21 Y/vigenere/KEY_5_L_1000: ', f'{path}/texts/Y/vigenere/KEY_5_L_1000_N_', 10000, criterion.criterian21, 50, 30)
    # test('criterian21 Y/vigenere/KEY_5_L_10000: ', f'{path}/texts/Y/vigenere/KEY_5_L_10000_N_', 1000, criterion.criterian21, 50, 32)
    # test('criterian21 Y/vigenere/KEY_10_L_10: ', f'{path}/texts/Y/vigenere/KEY_10_L_10_N_', 10000, criterion.criterian21, 50, 6)
    # test('criterian21 Y/vigenere/KEY_10_L_100: ', f'{path}/texts/Y/vigenere/KEY_10_L_100_N_', 10000, criterion.criterian21, 50, 23)
    # test('criterian21 Y/vigenere/KEY_10_L_1000: ', f'{path}/texts/Y/vigenere/KEY_10_L_1000_N_', 10000, criterion.criterian21, 50, 30)
    # test('criterian21 Y/vigenere/KEY_10_L_10000: ', f'{path}/texts/Y/vigenere/KEY_10_L_10000_N_', 1000, criterion.criterian21, 50, 32)

    # #criteria22

    # test('criterian22 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, criterion.criterian22, 1, 1)
    # test('criterian22 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, criterion.criterian22, 1, 5)
    # test('criterian22 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, criterion.criterian22, 1, 74)
    # test('criterian22 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, criterion.criterian22, 1, 850)
    # test('criterian22 Y/affine/L_10: ', f'{path}/texts/Y/affine/L_10_N_', 10000, criterion.criterian22, 1, 1)
    # test('criterian22 Y/affine/L_100: ', f'{path}/texts/Y/affine/L_100_N_', 10000, criterion.criterian22, 1, 5)
    # test('criterian22 Y/affine/L_1000: ', f'{path}/texts/Y/affine/L_1000_N_', 10000, criterion.criterian22, 1, 74)
    # test('criterian22 Y/affine/L_10000: ', f'{path}/texts/Y/affine/L_10000_N_', 1000, criterion.criterian22, 1, 850)
    # test('criterian22 Y/recursive/L_10: ', f'{path}/texts/Y/recursive/L_10_N_', 10000, criterion.criterian22, 1, 1)
    # test('criterian22 Y/recursive/L_100: ', f'{path}/texts/Y/recursive/L_100_N_', 10000, criterion.criterian22, 1, 5)
    # test('criterian22 Y/recursive/L_1000: ', f'{path}/texts/Y/recursive/L_1000_N_', 10000, criterion.criterian22, 1, 74)
    # test('criterian22 Y/recursive/L_10000: ', f'{path}/texts/Y/recursive/L_10000_N_', 1000, criterion.criterian22,1, 850)
    # test('criterian22 Y/uniform/L_10: ', f'{path}/texts/Y/uniform/L_10_N_', 10000, criterion.criterian22, 1, 1)
    # test('criterian22 Y/uniform/L_100: ', f'{path}/texts/Y/uniform/L_100_N_', 10000, criterion.criterian22, 1, 5)
    # test('criterian22 Y/uniform/L_1000: ', f'{path}/texts/Y/uniform/L_1000_N_', 10000, criterion.criterian22, 1, 74)
    # test('criterian22 Y/uniform/L_10000: ', f'{path}/texts/Y/uniform/L_10000_N_', 1000, criterion.criterian22, 1, 850)
    # test('criterian22 Y/vigenere/KEY_1_L_10: ', f'{path}/texts/Y/vigenere/KEY_1_L_10_N_', 10000, criterion.criterian22, 1, 1)
    # test('criterian22 Y/vigenere/KEY_1_L_100: ', f'{path}/texts/Y/vigenere/KEY_1_L_100_N_', 10000, criterion.criterian22, 1, 5)
    # test('criterian22 Y/vigenere/KEY_1_L_1000: ', f'{path}/texts/Y/vigenere/KEY_1_L_1000_N_', 10000, criterion.criterian22, 1, 74)
    # test('criterian22 Y/vigenere/KEY_1_L_10000: ', f'{path}/texts/Y/vigenere/KEY_1_L_10000_N_', 1000, criterion.criterian22, 1, 850)
    # test('criterian22 Y/vigenere/KEY_5_L_10: ', f'{path}/texts/Y/vigenere/KEY_5_L_10_N_', 10000, criterion.criterian22, 1, 1)
    # test('criterian22 Y/vigenere/KEY_5_L_100: ', f'{path}/texts/Y/vigenere/KEY_5_L_100_N_', 10000, criterion.criterian22, 1, 5)
    # test('criterian22 Y/vigenere/KEY_5_L_1000: ', f'{path}/texts/Y/vigenere/KEY_5_L_1000_N_', 10000, criterion.criterian22, 1, 74)
    # test('criterian22 Y/vigenere/KEY_5_L_10000: ', f'{path}/texts/Y/vigenere/KEY_5_L_10000_N_', 1000, criterion.criterian22, 1, 850)
    # test('criterian22 Y/vigenere/KEY_10_L_10: ', f'{path}/texts/Y/vigenere/KEY_10_L_10_N_', 10000, criterion.criterian22, 1, 1)
    # test('criterian22 Y/vigenere/KEY_10_L_100: ', f'{path}/texts/Y/vigenere/KEY_10_L_100_N_', 10000, criterion.criterian22, 1, 5)
    # test('criterian22 Y/vigenere/KEY_10_L_1000: ', f'{path}/texts/Y/vigenere/KEY_10_L_1000_N_', 10000, criterion.criterian22, 1, 74)
    # test('criterian22 Y/vigenere/KEY_10_L_10000: ', f'{path}/texts/Y/vigenere/KEY_10_L_10000_N_', 1000, criterion.criterian22, 1, 850)

    # #criterian23

    # test('criterian23 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, criterion.criterian23, 1, 1)
    # test('criterian23 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, criterion.criterian23, 1, 5)
    # test('criterian23 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, criterion.criterian23, 1, 74)
    # test('criterian23 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, criterion.criterian23, 1, 850)
    # test('criterian23 Y/affine/L_10: ', f'{path}/texts/Y/affine/L_10_N_', 10000, criterion.criterian23, 1, 1)
    # test('criterian23 Y/affine/L_100: ', f'{path}/texts/Y/affine/L_100_N_', 10000, criterion.criterian23, 1, 5)
    # test('criterian23 Y/affine/L_1000: ', f'{path}/texts/Y/affine/L_1000_N_', 10000, criterion.criterian23, 1, 74)
    # test('criterian23 Y/affine/L_10000: ', f'{path}/texts/Y/affine/L_10000_N_', 1000, criterion.criterian23, 1, 850)
    # test('criterian23 Y/recursive/L_10: ', f'{path}/texts/Y/recursive/L_10_N_', 10000, criterion.criterian23, 1, 1)
    # test('criterian23 Y/recursive/L_100: ', f'{path}/texts/Y/recursive/L_100_N_', 10000, criterion.criterian23, 1, 5)
    # test('criterian23 Y/recursive/L_1000: ', f'{path}/texts/Y/recursive/L_1000_N_', 10000, criterion.criterian23, 1, 74)
    # test('criterian23 Y/recursive/L_10000: ', f'{path}/texts/Y/recursive/L_10000_N_', 1000, criterion.criterian23,1, 850)
    # test('criterian23 Y/uniform/L_10: ', f'{path}/texts/Y/uniform/L_10_N_', 10000, criterion.criterian23, 1, 1)
    # test('criterian23 Y/uniform/L_100: ', f'{path}/texts/Y/uniform/L_100_N_', 10000, criterion.criterian23, 1, 5)
    # test('criterian23 Y/uniform/L_1000: ', f'{path}/texts/Y/uniform/L_1000_N_', 10000, criterion.criterian23, 1, 74)
    # test('criterian23 Y/uniform/L_10000: ', f'{path}/texts/Y/uniform/L_10000_N_', 1000, criterion.criterian23, 1, 850)
    # test('criterian23 Y/vigenere/KEY_1_L_10: ', f'{path}/texts/Y/vigenere/KEY_1_L_10_N_', 10000, criterion.criterian23, 1, 1)
    # test('criterian23 Y/vigenere/KEY_1_L_100: ', f'{path}/texts/Y/vigenere/KEY_1_L_100_N_', 10000, criterion.criterian23, 1, 5)
    # test('criterian23 Y/vigenere/KEY_1_L_1000: ', f'{path}/texts/Y/vigenere/KEY_1_L_1000_N_', 10000, criterion.criterian23, 1, 74)
    # test('criterian23 Y/vigenere/KEY_1_L_10000: ', f'{path}/texts/Y/vigenere/KEY_1_L_10000_N_', 1000, criterion.criterian23, 1, 850)
    # test('criterian23 Y/vigenere/KEY_5_L_10: ', f'{path}/texts/Y/vigenere/KEY_5_L_10_N_', 10000, criterion.criterian23, 1, 1)
    # test('criterian23 Y/vigenere/KEY_5_L_100: ', f'{path}/texts/Y/vigenere/KEY_5_L_100_N_', 10000, criterion.criterian23, 1, 5)
    # test('criterian23 Y/vigenere/KEY_5_L_1000: ', f'{path}/texts/Y/vigenere/KEY_5_L_1000_N_', 10000, criterion.criterian23, 1, 74)
    # test('criterian23 Y/vigenere/KEY_5_L_10000: ', f'{path}/texts/Y/vigenere/KEY_5_L_10000_N_', 1000, criterion.criterian23, 1, 850)
    # test('criterian23 Y/vigenere/KEY_10_L_10: ', f'{path}/texts/Y/vigenere/KEY_10_L_10_N_', 10000, criterion.criterian23, 1, 1)
    # test('criterian23 Y/vigenere/KEY_10_L_100: ', f'{path}/texts/Y/vigenere/KEY_10_L_100_N_', 10000, criterion.criterian23, 1, 5)
    # test('criterian23 Y/vigenere/KEY_10_L_1000: ', f'{path}/texts/Y/vigenere/KEY_10_L_1000_N_', 10000, criterion.criterian23, 1, 74)
    # test('criterian23 Y/vigenere/KEY_10_L_10000: ', f'{path}/texts/Y/vigenere/KEY_10_L_10000_N_', 1000, criterion.criterian23, 1, 850)

    # #criterian40

    # test('criterian40 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, criterion.criterian40, .05)
    # test('criterian40 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, criterion.criterian40, .015)
    # test('criterian40 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, criterion.criterian40, .004)
    # test('criterian40 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, criterion.criterian40, .001)
    # test('criterian40 Y/affine/L_10: ', f'{path}/texts/Y/affine/L_10_N_', 10000, criterion.criterian40, .05)
    # test('criterian40 Y/affine/L_100: ', f'{path}/texts/Y/affine/L_100_N_', 10000, criterion.criterian40, .015)
    # test('criterian40 Y/affine/L_1000: ', f'{path}/texts/Y/affine/L_1000_N_', 10000, criterion.criterian40, .004)
    # test('criterian40 Y/affine/L_10000: ', f'{path}/texts/Y/affine/L_10000_N_', 1000, criterion.criterian40, .001)
    # test('criterian40 Y/recursive/L_10: ', f'{path}/texts/Y/recursive/L_10_N_', 10000, criterion.criterian40, .05)
    # test('criterian40 Y/recursive/L_100: ', f'{path}/texts/Y/recursive/L_100_N_', 10000, criterion.criterian40, .015)
    # test('criterian40 Y/recursive/L_1000: ', f'{path}/texts/Y/recursive/L_1000_N_', 10000, criterion.criterian40, .004)
    # test('criterian40 Y/recursive/L_10000: ', f'{path}/texts/Y/recursive/L_10000_N_', 1000, criterion.criterian40, .001)
    # test('criterian40 Y/uniform/L_10: ', f'{path}/texts/Y/uniform/L_10_N_', 10000, criterion.criterian40, .05)
    # test('criterian40 Y/uniform/L_100: ', f'{path}/texts/Y/uniform/L_100_N_', 10000, criterion.criterian40, .015)
    # test('criterian40 Y/uniform/L_1000: ', f'{path}/texts/Y/uniform/L_1000_N_', 10000, criterion.criterian40, .004)
    # test('criterian40 Y/uniform/L_10000: ', f'{path}/texts/Y/uniform/L_10000_N_', 1000, criterion.criterian40, .001)
    # test('criterian40 Y/vigenere/KEY_1_L_10: ', f'{path}/texts/Y/vigenere/KEY_1_L_10_N_', 10000, criterion.criterian40, .05)
    # test('criterian40 Y/vigenere/KEY_1_L_100: ', f'{path}/texts/Y/vigenere/KEY_1_L_100_N_', 10000, criterion.criterian40, .015)
    # test('criterian40 Y/vigenere/KEY_1_L_1000: ', f'{path}/texts/Y/vigenere/KEY_1_L_1000_N_', 10000, criterion.criterian40, .004)
    # test('criterian40 Y/vigenere/KEY_1_L_10000: ', f'{path}/texts/Y/vigenere/KEY_1_L_10000_N_', 1000, criterion.criterian40, .001)
    # test('criterian40 Y/vigenere/KEY_5_L_10: ', f'{path}/texts/Y/vigenere/KEY_5_L_10_N_', 10000, criterion.criterian40, .05)
    # test('criterian40 Y/vigenere/KEY_5_L_100: ', f'{path}/texts/Y/vigenere/KEY_5_L_100_N_', 10000, criterion.criterian40, .015)
    # test('criterian40 Y/vigenere/KEY_5_L_1000: ', f'{path}/texts/Y/vigenere/KEY_5_L_1000_N_', 10000, criterion.criterian40, .004)
    # test('criterian40 Y/vigenere/KEY_5_L_10000: ', f'{path}/texts/Y/vigenere/KEY_5_L_10000_N_', 1000, criterion.criterian40, .001)
    # test('criterian40 Y/vigenere/KEY_10_L_10: ', f'{path}/texts/Y/vigenere/KEY_10_L_10_N_', 10000, criterion.criterian40, .05)
    # test('criterian40 Y/vigenere/KEY_10_L_100: ', f'{path}/texts/Y/vigenere/KEY_10_L_100_N_', 10000, criterion.criterian40, .015)
    # test('criterian40 Y/vigenere/KEY_10_L_1000: ', f'{path}/texts/Y/vigenere/KEY_10_L_1000_N_', 10000, criterion.criterian40, .004)
    # test('criterian40 Y/vigenere/KEY_10_L_10000: ', f'{path}/texts/Y/vigenere/KEY_10_L_10000_N_', 1000, criterion.criterian40, .001)

    # #criterian50

    # test('criterian50 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, criterion.criterian50, 50, 41)
    # test('criterian50 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, criterion.criterian50, 50, 21)
    # test('criterian50 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, criterion.criterian50, 50, 17)
    # test('criterian50 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, criterion.criterian50, 50, 17)
    # test('criterian50 Y/affine/L_10: ', f'{path}/texts/Y/affine/L_10_N_', 10000, criterion.criterian50, 50, 41)
    # test('criterian50 Y/affine/L_100: ', f'{path}/texts/Y/affine/L_100_N_', 10000, criterion.criterian50, 50, 21)
    # test('criterian50 Y/affine/L_1000: ', f'{path}/texts/Y/affine/L_1000_N_', 10000, criterion.criterian50, 50, 17)
    # test('criterian50 Y/affine/L_10000: ', f'{path}/texts/Y/affine/L_10000_N_', 1000, criterion.criterian50, 50, 17)
    # test('criterian50 Y/recursive/L_10: ', f'{path}/texts/Y/recursive/L_10_N_', 10000, criterion.criterian50, 50, 41)
    # test('criterian50 Y/recursive/L_100: ', f'{path}/texts/Y/recursive/L_100_N_', 10000, criterion.criterian50, 50, 21)
    # test('criterian50 Y/recursive/L_1000: ', f'{path}/texts/Y/recursive/L_1000_N_', 10000, criterion.criterian50, 50, 17)
    # test('criterian50 Y/recursive/L_10000: ', f'{path}/texts/Y/recursive/L_10000_N_', 1000, criterion.criterian50, 50, 17)
    # test('criterian50 Y/uniform/L_10: ', f'{path}/texts/Y/uniform/L_10_N_', 10000, criterion.criterian50, 50, 41)
    # test('criterian50 Y/uniform/L_100: ', f'{path}/texts/Y/uniform/L_100_N_', 10000, criterion.criterian50, 50, 21)
    # test('criterian50 Y/uniform/L_1000: ', f'{path}/texts/Y/uniform/L_1000_N_', 10000, criterion.criterian50, 50, 17)
    # test('criterian50 Y/uniform/L_10000: ', f'{path}/texts/Y/uniform/L_10000_N_', 1000, criterion.criterian50, 50, 17)
    # test('criterian50 Y/vigenere/KEY_1_L_10: ', f'{path}/texts/Y/vigenere/KEY_1_L_10_N_', 10000, criterion.criterian50, 50, 41)
    # test('criterian50 Y/vigenere/KEY_1_L_100: ', f'{path}/texts/Y/vigenere/KEY_1_L_100_N_', 10000, criterion.criterian50, 50, 21)
    # test('criterian50 Y/vigenere/KEY_1_L_1000: ', f'{path}/texts/Y/vigenere/KEY_1_L_1000_N_', 10000, criterion.criterian50, 50, 17)
    # test('criterian50 Y/vigenere/KEY_1_L_10000: ', f'{path}/texts/Y/vigenere/KEY_1_L_10000_N_', 1000, criterion.criterian50, 50, 17)
    # test('criterian50 Y/vigenere/KEY_5_L_10: ', f'{path}/texts/Y/vigenere/KEY_5_L_10_N_', 10000, criterion.criterian50, 50, 41)
    # test('criterian50 Y/vigenere/KEY_5_L_100: ', f'{path}/texts/Y/vigenere/KEY_5_L_100_N_', 10000, criterion.criterian50, 50, 21)
    # test('criterian50 Y/vigenere/KEY_5_L_1000: ', f'{path}/texts/Y/vigenere/KEY_5_L_1000_N_', 10000, criterion.criterian50, 50, 17)
    # test('criterian50 Y/vigenere/KEY_5_L_10000: ', f'{path}/texts/Y/vigenere/KEY_5_L_10000_N_', 1000, criterion.criterian50, 50, 17)
    # test('criterian50 Y/vigenere/KEY_10_L_10: ', f'{path}/texts/Y/vigenere/KEY_10_L_10_N_', 10000, criterion.criterian50, 50, 41)
    # test('criterian50 Y/vigenere/KEY_10_L_100: ', f'{path}/texts/Y/vigenere/KEY_10_L_100_N_', 10000, criterion.criterian50, 50, 21)
    # test('criterian50 Y/vigenere/KEY_10_L_1000: ', f'{path}/texts/Y/vigenere/KEY_10_L_1000_N_', 10000, criterion.criterian50, 50, 17)
    # test('criterian50 Y/vigenere/KEY_10_L_10000: ', f'{path}/texts/Y/vigenere/KEY_10_L_10000_N_', 1000, criterion.criterian50, 50, 17)


    # #structural

    # testStructural('structural X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, criterion.structuralCriterian, 48)
    # testStructural('structural X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, criterion.structuralCriterian, 66.2)

    # testStructural('structuralCriterian Y/affine/L_1000: ', f'{path}/texts/Y/affine/L_1000_N_', 10000, criterion.structuralCriterian, 48)
    # testStructural('structuralCriterian Y/affine/L_10000: ', f'{path}/texts/Y/affine/L_10000_N_', 1000, criterion.structuralCriterian, 66.2)
    
    # testStructural('structuralCriterian Y/recursive/L_1000: ', f'{path}/texts/Y/recursive/L_1000_N_', 10000, criterion.structuralCriterian, 48)
    # testStructural('structuralCriterian Y/recursive/L_10000: ', f'{path}/texts/Y/recursive/L_10000_N_', 1000, criterion.structuralCriterian, 66.2)

    # testStructural('structuralCriterian Y/uniform/L_1000: ', f'{path}/texts/Y/uniform/L_1000_N_', 10000, criterion.structuralCriterian, 48)
    # testStructural('structuralCriterian Y/uniform/L_10000: ', f'{path}/texts/Y/uniform/L_10000_N_', 1000, criterion.structuralCriterian, 66.2)
    
    # testStructural('structuralCriterian Y/vigenere/KEY_1_L_1000: ', f'{path}/texts/Y/vigenere/KEY_1_L_1000_N_', 10000, criterion.structuralCriterian, 48)
    # testStructural('structuralCriterian Y/vigenere/KEY_1_L_10000: ', f'{path}/texts/Y/vigenere/KEY_1_L_10000_N_', 1000, criterion.structuralCriterian, 66.2)
    
    # testStructural('structuralCriterian Y/vigenere/KEY_5_L_1000: ', f'{path}/texts/Y/vigenere/KEY_5_L_1000_N_', 10000, criterion.structuralCriterian, 48)
    # testStructural('structuralCriterian Y/vigenere/KEY_5_L_10000: ', f'{path}/texts/Y/vigenere/KEY_5_L_10000_N_', 1000, criterion.structuralCriterian, 66.2)
    
    # testStructural('structuralCriterian Y/vigenere/KEY_10_L_1000: ', f'{path}/texts/Y/vigenere/KEY_10_L_1000_N_', 10000, criterion.structuralCriterian, 48)
    # testStructural('structuralCriterian Y/vigenere/KEY_10_L_10000: ', f'{path}/texts/Y/vigenere/KEY_10_L_10000_N_', 1000, criterion.structuralCriterian, 66.2)

    # ################################################

    # bigrams_frequency =  json.loads(read(f'{path}/result/bigrams_frequency.json'))
    # criterion_bigram = Criterion(bigrams_frequency)

    # print("bigram: ")
    # #criteria20

    # test('criterian20 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, criterion_bigram.criterian20, 1)
    # test('criterian20 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, criterion_bigram.criterian20, 1)
    # test('criterian20 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, criterion_bigram.criterian20, 30)
    # test('criterian20 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, criterion_bigram.criterian20, 210)
    # test('criterian20 Y/affine/L_10: ', f'{path}/texts/Y/affine/L_10_N_', 10000, criterion_bigram.criterian20, 1)
    # test('criterian20 Y/affine/L_100: ', f'{path}/texts/Y/affine/L_100_N_', 10000, criterion_bigram.criterian20, 1)
    # test('criterian20 Y/affine/L_1000: ', f'{path}/texts/Y/affine/L_1000_N_', 10000, criterion_bigram.criterian20, 30)
    # test('criterian20 Y/affine/L_10000: ', f'{path}/texts/Y/affine/L_10000_N_', 1000, criterion_bigram.criterian20, 210)
    # test('criterian20 Y/recursive/L_10: ', f'{path}/texts/Y/recursive/L_10_N_', 10000, criterion_bigram.criterian20, 1)
    # test('criterian20 Y/recursive/L_100: ', f'{path}/texts/Y/recursive/L_100_N_', 10000, criterion_bigram.criterian20, 1)
    # test('criterian20 Y/recursive/L_1000: ', f'{path}/texts/Y/recursive/L_1000_N_', 10000, criterion_bigram.criterian20, 30)
    # test('criterian20 Y/recursive/L_10000: ', f'{path}/texts/Y/recursive/L_10000_N_', 1000, criterion_bigram.criterian20, 210)
    # test('criterian20 Y/uniform/L_10: ', f'{path}/texts/Y/uniform/L_10_N_', 10000, criterion_bigram.criterian20, 1)
    # test('criterian20 Y/uniform/L_100: ', f'{path}/texts/Y/uniform/L_100_N_', 10000, criterion_bigram.criterian20, 1)
    # test('criterian20 Y/uniform/L_1000: ', f'{path}/texts/Y/uniform/L_1000_N_', 10000, criterion_bigram.criterian20, 30)
    # test('criterian20 Y/uniform/L_10000: ', f'{path}/texts/Y/uniform/L_10000_N_', 1000, criterion_bigram.criterian20, 210)
    # test('criterian20 Y/vigenere/KEY_1_L_10: ', f'{path}/texts/Y/vigenere/KEY_1_L_10_N_', 10000, criterion_bigram.criterian20, 1)
    # test('criterian20 Y/vigenere/KEY_1_L_100: ', f'{path}/texts/Y/vigenere/KEY_1_L_100_N_', 10000, criterion_bigram.criterian20, 1)
    # test('criterian20 Y/vigenere/KEY_1_L_1000: ', f'{path}/texts/Y/vigenere/KEY_1_L_1000_N_', 10000, criterion_bigram.criterian20, 30)
    # test('criterian20 Y/vigenere/KEY_1_L_10000: ', f'{path}/texts/Y/vigenere/KEY_1_L_10000_N_', 1000, criterion_bigram.criterian20, 210)
    # test('criterian20 Y/vigenere/KEY_5_L_10: ', f'{path}/texts/Y/vigenere/KEY_5_L_10_N_', 10000, criterion_bigram.criterian20, 1)
    # test('criterian20 Y/vigenere/KEY_5_L_100: ', f'{path}/texts/Y/vigenere/KEY_5_L_100_N_', 10000, criterion_bigram.criterian20, 1)
    # test('criterian20 Y/vigenere/KEY_5_L_1000: ', f'{path}/texts/Y/vigenere/KEY_5_L_1000_N_', 10000, criterion_bigram.criterian20, 30)
    # test('criterian20 Y/vigenere/KEY_5_L_10000: ', f'{path}/texts/Y/vigenere/KEY_5_L_10000_N_', 1000, criterion_bigram.criterian20, 210)
    # test('criterian20 Y/vigenere/KEY_10_L_10: ', f'{path}/texts/Y/vigenere/KEY_10_L_10_N_', 10000, criterion_bigram.criterian20, 1)
    # test('criterian20 Y/vigenere/KEY_10_L_100: ', f'{path}/texts/Y/vigenere/KEY_10_L_100_N_', 10000, criterion_bigram.criterian20, 1)
    # test('criterian20 Y/vigenere/KEY_10_L_1000: ', f'{path}/texts/Y/vigenere/KEY_10_L_1000_N_', 10000, criterion_bigram.criterian20, 30)
    # test('criterian20 Y/vigenere/KEY_10_L_10000: ', f'{path}/texts/Y/vigenere/KEY_10_L_10000_N_', 1000, criterion_bigram.criterian20, 210)

    # #criteria21

    # test('criterian21 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, criterion_bigram.criterian21, 50, 1)
    # test('criterian21 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, criterion_bigram.criterian21, 5, 2)
    # test('criterian21 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, criterion_bigram.criterian21, 50, 49)
    # test('criterian21 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, criterion_bigram.criterian21, 210, 210)
    # test('criterian21 Y/affine/L_10: ', f'{path}/texts/Y/affine/L_10_N_', 10000, criterion_bigram.criterian21, 50, 1)
    # test('criterian21 Y/affine/L_100: ', f'{path}/texts/Y/affine/L_100_N_', 10000, criterion_bigram.criterian21, 5, 2)
    # test('criterian21 Y/affine/L_1000: ', f'{path}/texts/Y/affine/L_1000_N_', 10000, criterion_bigram.criterian21, 50, 49)
    # test('criterian21 Y/affine/L_10000: ', f'{path}/texts/Y/affine/L_10000_N_', 1000, criterion_bigram.criterian21, 210, 210)
    # test('criterian21 Y/recursive/L_10: ', f'{path}/texts/Y/recursive/L_10_N_', 10000, criterion_bigram.criterian21, 50, 1)
    # test('criterian21 Y/recursive/L_100: ', f'{path}/texts/Y/recursive/L_100_N_', 10000, criterion_bigram.criterian21, 5, 2)
    # test('criterian21 Y/recursive/L_1000: ', f'{path}/texts/Y/recursive/L_1000_N_', 10000, criterion_bigram.criterian21, 50, 49)
    # test('criterian21 Y/recursive/L_10000: ', f'{path}/texts/Y/recursive/L_10000_N_', 1000, criterion_bigram.criterian21,210, 210)
    # test('criterian21 Y/uniform/L_10: ', f'{path}/texts/Y/uniform/L_10_N_', 10000, criterion_bigram.criterian21, 50, 1)
    # test('criterian21 Y/uniform/L_100: ', f'{path}/texts/Y/uniform/L_100_N_', 10000, criterion_bigram.criterian21, 5, 2)
    # test('criterian21 Y/uniform/L_1000: ', f'{path}/texts/Y/uniform/L_1000_N_', 10000, criterion_bigram.criterian21, 50, 49)
    # test('criterian21 Y/uniform/L_10000: ', f'{path}/texts/Y/uniform/L_10000_N_', 1000, criterion_bigram.criterian21, 210, 210)
    # test('criterian21 Y/vigenere/KEY_1_L_10: ', f'{path}/texts/Y/vigenere/KEY_1_L_10_N_', 10000, criterion_bigram.criterian21, 50, 1)
    # test('criterian21 Y/vigenere/KEY_1_L_100: ', f'{path}/texts/Y/vigenere/KEY_1_L_100_N_', 10000, criterion_bigram.criterian21, 5, 2)
    # test('criterian21 Y/vigenere/KEY_1_L_1000: ', f'{path}/texts/Y/vigenere/KEY_1_L_1000_N_', 10000, criterion_bigram.criterian21, 50, 49)
    # test('criterian21 Y/vigenere/KEY_1_L_10000: ', f'{path}/texts/Y/vigenere/KEY_1_L_10000_N_', 1000, criterion_bigram.criterian21, 210, 210)
    # test('criterian21 Y/vigenere/KEY_5_L_10: ', f'{path}/texts/Y/vigenere/KEY_5_L_10_N_', 10000, criterion_bigram.criterian21, 50, 1)
    # test('criterian21 Y/vigenere/KEY_5_L_100: ', f'{path}/texts/Y/vigenere/KEY_5_L_100_N_', 10000, criterion_bigram.criterian21, 5, 2)
    # test('criterian21 Y/vigenere/KEY_5_L_1000: ', f'{path}/texts/Y/vigenere/KEY_5_L_1000_N_', 10000, criterion_bigram.criterian21, 50, 49)
    # test('criterian21 Y/vigenere/KEY_5_L_10000: ', f'{path}/texts/Y/vigenere/KEY_5_L_10000_N_', 1000, criterion_bigram.criterian21, 210, 210)
    # test('criterian21 Y/vigenere/KEY_10_L_10: ', f'{path}/texts/Y/vigenere/KEY_10_L_10_N_', 10000, criterion_bigram.criterian21, 50, 1)
    # test('criterian21 Y/vigenere/KEY_10_L_100: ', f'{path}/texts/Y/vigenere/KEY_10_L_100_N_', 10000, criterion_bigram.criterian21, 5, 2)
    # test('criterian21 Y/vigenere/KEY_10_L_1000: ', f'{path}/texts/Y/vigenere/KEY_10_L_1000_N_', 10000, criterion_bigram.criterian21, 50, 49)
    # test('criterian21 Y/vigenere/KEY_10_L_10000: ', f'{path}/texts/Y/vigenere/KEY_10_L_10000_N_', 1000, criterion_bigram.criterian21, 210, 210)

    # #criteria22

    # test('criterian22 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, criterion_bigram.criterian22, 1, 1)
    # test('criterian22 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, criterion_bigram.criterian22, 1, 1)
    # test('criterian22 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, criterion_bigram.criterian22, 5, 4)
    # test('criterian22 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, criterion_bigram.criterian22, 30, 40)
    # test('criterian22 Y/affine/L_10: ', f'{path}/texts/Y/affine/L_10_N_', 10000, criterion_bigram.criterian22, 1, 1)
    # test('criterian22 Y/affine/L_100: ', f'{path}/texts/Y/affine/L_100_N_', 10000, criterion_bigram.criterian22, 1, 1)
    # test('criterian22 Y/affine/L_1000: ', f'{path}/texts/Y/affine/L_1000_N_', 10000, criterion_bigram.criterian22, 5, 4)
    # test('criterian22 Y/affine/L_10000: ', f'{path}/texts/Y/affine/L_10000_N_', 1000, criterion_bigram.criterian22, 30, 40)
    # test('criterian22 Y/recursive/L_10: ', f'{path}/texts/Y/recursive/L_10_N_', 10000, criterion_bigram.criterian22, 1, 1)
    # test('criterian22 Y/recursive/L_100: ', f'{path}/texts/Y/recursive/L_100_N_', 10000, criterion_bigram.criterian22, 1, 1)
    # test('criterian22 Y/recursive/L_1000: ', f'{path}/texts/Y/recursive/L_1000_N_', 10000, criterion_bigram.criterian22, 5, 4)
    # test('criterian22 Y/recursive/L_10000: ', f'{path}/texts/Y/recursive/L_10000_N_', 1000, criterion_bigram.criterian22,30, 40)
    # test('criterian22 Y/uniform/L_10: ', f'{path}/texts/Y/uniform/L_10_N_', 10000, criterion_bigram.criterian22, 1, 1)
    # test('criterian22 Y/uniform/L_100: ', f'{path}/texts/Y/uniform/L_100_N_', 10000, criterion_bigram.criterian22, 1, 1)
    # test('criterian22 Y/uniform/L_1000: ', f'{path}/texts/Y/uniform/L_1000_N_', 10000, criterion_bigram.criterian22, 5, 4)
    # test('criterian22 Y/uniform/L_10000: ', f'{path}/texts/Y/uniform/L_10000_N_', 1000, criterion_bigram.criterian22, 30, 40)
    # test('criterian22 Y/vigenere/KEY_1_L_10: ', f'{path}/texts/Y/vigenere/KEY_1_L_10_N_', 10000, criterion_bigram.criterian22, 1, 1)
    # test('criterian22 Y/vigenere/KEY_1_L_100: ', f'{path}/texts/Y/vigenere/KEY_1_L_100_N_', 10000, criterion_bigram.criterian22, 1, 1)
    # test('criterian22 Y/vigenere/KEY_1_L_1000: ', f'{path}/texts/Y/vigenere/KEY_1_L_1000_N_', 10000, criterion_bigram.criterian22, 5, 4)
    # test('criterian22 Y/vigenere/KEY_1_L_10000: ', f'{path}/texts/Y/vigenere/KEY_1_L_10000_N_', 1000, criterion_bigram.criterian22, 30, 40)
    # test('criterian22 Y/vigenere/KEY_5_L_10: ', f'{path}/texts/Y/vigenere/KEY_5_L_10_N_', 10000, criterion_bigram.criterian22, 1, 1)
    # test('criterian22 Y/vigenere/KEY_5_L_100: ', f'{path}/texts/Y/vigenere/KEY_5_L_100_N_', 10000, criterion_bigram.criterian22, 1, 1)
    # test('criterian22 Y/vigenere/KEY_5_L_1000: ', f'{path}/texts/Y/vigenere/KEY_5_L_1000_N_', 10000, criterion_bigram.criterian22, 5, 4)
    # test('criterian22 Y/vigenere/KEY_5_L_10000: ', f'{path}/texts/Y/vigenere/KEY_5_L_10000_N_', 1000, criterion_bigram.criterian22, 30, 40)
    # test('criterian22 Y/vigenere/KEY_10_L_10: ', f'{path}/texts/Y/vigenere/KEY_10_L_10_N_', 10000, criterion_bigram.criterian22, 1, 1)
    # test('criterian22 Y/vigenere/KEY_10_L_100: ', f'{path}/texts/Y/vigenere/KEY_10_L_100_N_', 10000, criterion_bigram.criterian22, 1, 1)
    # test('criterian22 Y/vigenere/KEY_10_L_1000: ', f'{path}/texts/Y/vigenere/KEY_10_L_1000_N_', 10000, criterion_bigram.criterian22, 5, 4)
    # test('criterian22 Y/vigenere/KEY_10_L_10000: ', f'{path}/texts/Y/vigenere/KEY_10_L_10000_N_', 1000, criterion_bigram.criterian22, 30, 40)

    # #criterian23

    # test('criterian23 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, criterion_bigram.criterian23, 30, 1)
    # test('criterian23 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, criterion_bigram.criterian23, 7, 4)
    # test('criterian23 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, criterion_bigram.criterian23, 20, 150)
    # test('criterian23 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, criterion_bigram.criterian23, 20, 1700)
    # test('criterian23 Y/affine/L_10: ', f'{path}/texts/Y/affine/L_10_N_', 10000, criterion_bigram.criterian23, 30, 1)
    # test('criterian23 Y/affine/L_100: ', f'{path}/texts/Y/affine/L_100_N_', 10000, criterion_bigram.criterian23, 7, 4)
    # test('criterian23 Y/affine/L_1000: ', f'{path}/texts/Y/affine/L_1000_N_', 10000, criterion_bigram.criterian23, 20, 150)
    # test('criterian23 Y/affine/L_10000: ', f'{path}/texts/Y/affine/L_10000_N_', 1000, criterion_bigram.criterian23, 20, 1700)
    # test('criterian23 Y/recursive/L_10: ', f'{path}/texts/Y/recursive/L_10_N_', 10000, criterion_bigram.criterian23, 30, 1)
    # test('criterian23 Y/recursive/L_100: ', f'{path}/texts/Y/recursive/L_100_N_', 10000, criterion_bigram.criterian23, 7, 4)
    # test('criterian23 Y/recursive/L_1000: ', f'{path}/texts/Y/recursive/L_1000_N_', 10000, criterion_bigram.criterian23, 20, 150)
    # test('criterian23 Y/recursive/L_10000: ', f'{path}/texts/Y/recursive/L_10000_N_', 1000, criterion_bigram.criterian23,20, 1700)
    # test('criterian23 Y/uniform/L_10: ', f'{path}/texts/Y/uniform/L_10_N_', 10000, criterion_bigram.criterian23, 30, 1)
    # test('criterian23 Y/uniform/L_100: ', f'{path}/texts/Y/uniform/L_100_N_', 10000, criterion_bigram.criterian23, 7, 4)
    # test('criterian23 Y/uniform/L_1000: ', f'{path}/texts/Y/uniform/L_1000_N_', 10000, criterion_bigram.criterian23, 20, 150)
    # test('criterian23 Y/uniform/L_10000: ', f'{path}/texts/Y/uniform/L_10000_N_', 1000, criterion_bigram.criterian23, 20, 1700)
    # test('criterian23 Y/vigenere/KEY_1_L_10: ', f'{path}/texts/Y/vigenere/KEY_1_L_10_N_', 10000, criterion_bigram.criterian23, 30, 1)
    # test('criterian23 Y/vigenere/KEY_1_L_100: ', f'{path}/texts/Y/vigenere/KEY_1_L_100_N_', 10000, criterion_bigram.criterian23, 7, 4)
    # test('criterian23 Y/vigenere/KEY_1_L_1000: ', f'{path}/texts/Y/vigenere/KEY_1_L_1000_N_', 10000, criterion_bigram.criterian23, 20, 150)
    # test('criterian23 Y/vigenere/KEY_1_L_10000: ', f'{path}/texts/Y/vigenere/KEY_1_L_10000_N_', 1000, criterion_bigram.criterian23, 20, 1700)
    # test('criterian23 Y/vigenere/KEY_5_L_10: ', f'{path}/texts/Y/vigenere/KEY_5_L_10_N_', 10000, criterion_bigram.criterian23, 30, 1)
    # test('criterian23 Y/vigenere/KEY_5_L_100: ', f'{path}/texts/Y/vigenere/KEY_5_L_100_N_', 10000, criterion_bigram.criterian23, 7, 4)
    # test('criterian23 Y/vigenere/KEY_5_L_1000: ', f'{path}/texts/Y/vigenere/KEY_5_L_1000_N_', 10000, criterion_bigram.criterian23, 20, 150)
    # test('criterian23 Y/vigenere/KEY_5_L_10000: ', f'{path}/texts/Y/vigenere/KEY_5_L_10000_N_', 1000, criterion_bigram.criterian23, 20, 1700)
    # test('criterian23 Y/vigenere/KEY_10_L_10: ', f'{path}/texts/Y/vigenere/KEY_10_L_10_N_', 10000, criterion_bigram.criterian23, 30, 1)
    # test('criterian23 Y/vigenere/KEY_10_L_100: ', f'{path}/texts/Y/vigenere/KEY_10_L_100_N_', 10000, criterion_bigram.criterian23, 7, 4)
    # test('criterian23 Y/vigenere/KEY_10_L_1000: ', f'{path}/texts/Y/vigenere/KEY_10_L_1000_N_', 10000, criterion_bigram.criterian23, 20, 150)
    # test('criterian23 Y/vigenere/KEY_10_L_10000: ', f'{path}/texts/Y/vigenere/KEY_10_L_10000_N_', 1000, criterion_bigram.criterian23, 20, 1700)

    # #criterian40

    # test('criterian40 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, criterion_bigram.criterian40, .03)
    # test('criterian40 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, criterion_bigram.criterian40, .003)
    # test('criterian40 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, criterion_bigram.criterian40, .001)
    # test('criterian40 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, criterion_bigram.criterian40, .00035)
    # test('criterian40 Y/affine/L_10: ', f'{path}/texts/Y/affine/L_10_N_', 10000, criterion_bigram.criterian40, .03)
    # test('criterian40 Y/affine/L_100: ', f'{path}/texts/Y/affine/L_100_N_', 10000, criterion_bigram.criterian40, .003)
    # test('criterian40 Y/affine/L_1000: ', f'{path}/texts/Y/affine/L_1000_N_', 10000, criterion_bigram.criterian40, .001)
    # test('criterian40 Y/affine/L_10000: ', f'{path}/texts/Y/affine/L_10000_N_', 1000, criterion_bigram.criterian40, .00035)
    # test('criterian40 Y/recursive/L_10: ', f'{path}/texts/Y/recursive/L_10_N_', 10000, criterion_bigram.criterian40, .03)
    # test('criterian40 Y/recursive/L_100: ', f'{path}/texts/Y/recursive/L_100_N_', 10000, criterion_bigram.criterian40, .003)
    # test('criterian40 Y/recursive/L_1000: ', f'{path}/texts/Y/recursive/L_1000_N_', 10000, criterion_bigram.criterian40, .001)
    # test('criterian40 Y/recursive/L_10000: ', f'{path}/texts/Y/recursive/L_10000_N_', 1000, criterion_bigram.criterian40, .00035)
    # test('criterian40 Y/uniform/L_10: ', f'{path}/texts/Y/uniform/L_10_N_', 10000, criterion_bigram.criterian40, .03)
    # test('criterian40 Y/uniform/L_100: ', f'{path}/texts/Y/uniform/L_100_N_', 10000, criterion_bigram.criterian40, .003)
    # test('criterian40 Y/uniform/L_1000: ', f'{path}/texts/Y/uniform/L_1000_N_', 10000, criterion_bigram.criterian40, .001)
    # test('criterian40 Y/uniform/L_10000: ', f'{path}/texts/Y/uniform/L_10000_N_', 1000, criterion_bigram.criterian40, .00035)
    # test('criterian40 Y/vigenere/KEY_1_L_10: ', f'{path}/texts/Y/vigenere/KEY_1_L_10_N_', 10000, criterion_bigram.criterian40, .03)
    # test('criterian40 Y/vigenere/KEY_1_L_100: ', f'{path}/texts/Y/vigenere/KEY_1_L_100_N_', 10000, criterion_bigram.criterian40, .003)
    # test('criterian40 Y/vigenere/KEY_1_L_1000: ', f'{path}/texts/Y/vigenere/KEY_1_L_1000_N_', 10000, criterion_bigram.criterian40, .001)
    # test('criterian40 Y/vigenere/KEY_1_L_10000: ', f'{path}/texts/Y/vigenere/KEY_1_L_10000_N_', 1000, criterion_bigram.criterian40, .00035)
    # test('criterian40 Y/vigenere/KEY_5_L_10: ', f'{path}/texts/Y/vigenere/KEY_5_L_10_N_', 10000, criterion_bigram.criterian40, .03)
    # test('criterian40 Y/vigenere/KEY_5_L_100: ', f'{path}/texts/Y/vigenere/KEY_5_L_100_N_', 10000, criterion_bigram.criterian40, .003)
    # test('criterian40 Y/vigenere/KEY_5_L_1000: ', f'{path}/texts/Y/vigenere/KEY_5_L_1000_N_', 10000, criterion_bigram.criterian40, .001)
    # test('criterian40 Y/vigenere/KEY_5_L_10000: ', f'{path}/texts/Y/vigenere/KEY_5_L_10000_N_', 1000, criterion_bigram.criterian40, .00035)
    # test('criterian40 Y/vigenere/KEY_10_L_10: ', f'{path}/texts/Y/vigenere/KEY_10_L_10_N_', 10000, criterion_bigram.criterian40, .03)
    # test('criterian40 Y/vigenere/KEY_10_L_100: ', f'{path}/texts/Y/vigenere/KEY_10_L_100_N_', 10000, criterion_bigram.criterian40, .003)
    # test('criterian40 Y/vigenere/KEY_10_L_1000: ', f'{path}/texts/Y/vigenere/KEY_10_L_1000_N_', 10000, criterion_bigram.criterian40, .001)
    # test('criterian40 Y/vigenere/KEY_10_L_10000: ', f'{path}/texts/Y/vigenere/KEY_10_L_10000_N_', 1000, criterion_bigram.criterian40, .00035)

    # #criterian50

    # test('criterian50 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, criterion_bigram.criterian50, 500, 497)
    # test('criterian50 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, criterion_bigram.criterian50, 100, 99)
    # test('criterian50 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, criterion_bigram.criterian50, 50, 49)
    # test('criterian50 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, criterion_bigram.criterian50, 50, 47)
    # test('criterian50 Y/affine/L_10: ', f'{path}/texts/Y/affine/L_10_N_', 10000, criterion_bigram.criterian50, 500, 497)
    # test('criterian50 Y/affine/L_100: ', f'{path}/texts/Y/affine/L_100_N_', 10000, criterion_bigram.criterian50, 100, 99)
    # test('criterian50 Y/affine/L_1000: ', f'{path}/texts/Y/affine/L_1000_N_', 10000, criterion_bigram.criterian50, 50, 49)
    # test('criterian50 Y/affine/L_10000: ', f'{path}/texts/Y/affine/L_10000_N_', 1000, criterion_bigram.criterian50, 50, 47)
    # test('criterian50 Y/recursive/L_10: ', f'{path}/texts/Y/recursive/L_10_N_', 10000, criterion_bigram.criterian50, 500, 497)
    # test('criterian50 Y/recursive/L_100: ', f'{path}/texts/Y/recursive/L_100_N_', 10000, criterion_bigram.criterian50, 100, 99)
    # test('criterian50 Y/recursive/L_1000: ', f'{path}/texts/Y/recursive/L_1000_N_', 10000, criterion_bigram.criterian50, 50, 49)
    # test('criterian50 Y/recursive/L_10000: ', f'{path}/texts/Y/recursive/L_10000_N_', 1000, criterion_bigram.criterian50, 50, 47)
    # test('criterian50 Y/uniform/L_10: ', f'{path}/texts/Y/uniform/L_10_N_', 10000, criterion_bigram.criterian50, 500, 497)
    # test('criterian50 Y/uniform/L_100: ', f'{path}/texts/Y/uniform/L_100_N_', 10000, criterion_bigram.criterian50, 100, 99)
    # test('criterian50 Y/uniform/L_1000: ', f'{path}/texts/Y/uniform/L_1000_N_', 10000, criterion_bigram.criterian50, 50, 49)
    # test('criterian50 Y/uniform/L_10000: ', f'{path}/texts/Y/uniform/L_10000_N_', 1000, criterion_bigram.criterian50, 50, 47)
    # test('criterian50 Y/vigenere/KEY_1_L_10: ', f'{path}/texts/Y/vigenere/KEY_1_L_10_N_', 10000, criterion_bigram.criterian50, 500, 497)
    # test('criterian50 Y/vigenere/KEY_1_L_100: ', f'{path}/texts/Y/vigenere/KEY_1_L_100_N_', 10000, criterion_bigram.criterian50, 100, 99)
    # test('criterian50 Y/vigenere/KEY_1_L_1000: ', f'{path}/texts/Y/vigenere/KEY_1_L_1000_N_', 10000, criterion_bigram.criterian50, 50, 49)
    # test('criterian50 Y/vigenere/KEY_1_L_10000: ', f'{path}/texts/Y/vigenere/KEY_1_L_10000_N_', 1000, criterion_bigram.criterian50, 50, 47)
    # test('criterian50 Y/vigenere/KEY_5_L_10: ', f'{path}/texts/Y/vigenere/KEY_5_L_10_N_', 10000, criterion_bigram.criterian50, 500, 497)
    # test('criterian50 Y/vigenere/KEY_5_L_100: ', f'{path}/texts/Y/vigenere/KEY_5_L_100_N_', 10000, criterion_bigram.criterian50, 100, 99)
    # test('criterian50 Y/vigenere/KEY_5_L_1000: ', f'{path}/texts/Y/vigenere/KEY_5_L_1000_N_', 10000, criterion_bigram.criterian50, 50, 49)
    # test('criterian50 Y/vigenere/KEY_5_L_10000: ', f'{path}/texts/Y/vigenere/KEY_5_L_10000_N_', 1000, criterion_bigram.criterian50, 50, 47)
    # test('criterian50 Y/vigenere/KEY_10_L_10: ', f'{path}/texts/Y/vigenere/KEY_10_L_10_N_', 10000, criterion_bigram.criterian50, 500, 497)
    # test('criterian50 Y/vigenere/KEY_10_L_100: ', f'{path}/texts/Y/vigenere/KEY_10_L_100_N_', 10000, criterion_bigram.criterian50, 100, 99)
    # test('criterian50 Y/vigenere/KEY_10_L_1000: ', f'{path}/texts/Y/vigenere/KEY_10_L_1000_N_', 10000, criterion_bigram.criterian50, 50, 49)
    # test('criterian50 Y/vigenere/KEY_10_L_10000: ', f'{path}/texts/Y/vigenere/KEY_10_L_10000_N_', 1000, criterion_bigram.criterian50, 50, 47)


    # #structural

    # testStructural('structural X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, criterion_bigram.structuralCriterian, 48)
    # testStructural('structural X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, criterion_bigram.structuralCriterian, 66.2)

    # testStructural('structuralCriterian Y/affine/L_1000: ', f'{path}/texts/Y/affine/L_1000_N_', 10000, criterion_bigram.structuralCriterian, 48)
    # testStructural('structuralCriterian Y/affine/L_10000: ', f'{path}/texts/Y/affine/L_10000_N_', 1000, criterion_bigram.structuralCriterian, 66.2)
    
    # testStructural('structuralCriterian Y/recursive/L_1000: ', f'{path}/texts/Y/recursive/L_1000_N_', 10000, criterion_bigram.structuralCriterian, 48)
    # testStructural('structuralCriterian Y/recursive/L_10000: ', f'{path}/texts/Y/recursive/L_10000_N_', 1000, criterion_bigram.structuralCriterian, 66.2)

    # testStructural('structuralCriterian Y/uniform/L_1000: ', f'{path}/texts/Y/uniform/L_1000_N_', 10000, criterion_bigram.structuralCriterian, 48)
    # testStructural('structuralCriterian Y/uniform/L_10000: ', f'{path}/texts/Y/uniform/L_10000_N_', 1000, criterion_bigram.structuralCriterian, 66.2)
    
    # testStructural('structuralCriterian Y/vigenere/KEY_1_L_1000: ', f'{path}/texts/Y/vigenere/KEY_1_L_1000_N_', 10000, criterion_bigram.structuralCriterian, 48)
    # testStructural('structuralCriterian Y/vigenere/KEY_1_L_10000: ', f'{path}/texts/Y/vigenere/KEY_1_L_10000_N_', 1000, criterion_bigram.structuralCriterian, 66.2)
    
    # testStructural('structuralCriterian Y/vigenere/KEY_5_L_1000: ', f'{path}/texts/Y/vigenere/KEY_5_L_1000_N_', 10000, criterion_bigram.structuralCriterian, 48)
    # testStructural('structuralCriterian Y/vigenere/KEY_5_L_10000: ', f'{path}/texts/Y/vigenere/KEY_5_L_10000_N_', 1000, criterion_bigram.structuralCriterian, 66.2)
    
    # testStructural('structuralCriterian Y/vigenere/KEY_10_L_1000: ', f'{path}/texts/Y/vigenere/KEY_10_L_1000_N_', 10000, criterion_bigram.structuralCriterian, 48)
    # testStructural('structuralCriterian Y/vigenere/KEY_10_L_10000: ', f'{path}/texts/Y/vigenere/KEY_10_L_10000_N_', 1000, criterion_bigram.structuralCriterian, 66.2)


if __name__ == '__main__':
    main_test()