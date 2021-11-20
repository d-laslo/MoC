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
    return res.count(True) / N
    # print(f'{result_name}{res.count(True)}                         {res.count(True)}/10000 = {res.count(True)/10000}')

def testFalse(result_name, path, N, criteria, *parameters):
    res = []
    for n in range(N):
        res.append(criteria(read(f'{path}{n + 1}'), *parameters))
    return res.count(False)/ N
    # print(f'{result_name}{res.count(False)}                        {res.count(False)}/10000 = {res.count(False)/10000}')

def testTrueStructural(result_name, path, N, criteria, *parameters):
    res = []
    for n in range(N):
        res.append(criteria(f'{path}{n + 1}', *parameters))
    return res.count(True) / N
    #print(f'{result_name}{res.count(True)}                         {res.count(True)}/10000 = {res.count(True)/10000}')

def testFalseStructural(result_name, path, N, criteria, *parameters):
    res = []
    for n in range(N):
        res.append(criteria(f'{path}{n + 1}', *parameters))
    return res.count(False)/ N
    #print(f'{result_name}{res.count(False)}                        {res.count(False)}/10000 = {res.count(False)/10000}')


def output(criteria, size_l1, p_l1, size_l2, p_l2, fp_l1, fn_l1, fp_l2, fn_l2):
    #&2.1 () &0.0245 & 0.5208 & 0.1167 & 0.0096
    if size_l1 == '' or size_l2 == '':
        print(f'{criteria} ({p_l1}; {p_l2}) & {fp_l1} & {fn_l1} & {fp_l2} & {fn_l2}')
    else:
        print(f'{criteria} ({size_l1},{p_l1}; {size_l2}, {p_l2}) & {fp_l1} & {fn_l1} & {fp_l2} & {fn_l2}')

def affine_L10(letter_criterion,bigram_criterion):
    print("affine_L10:")

    p_l1 = 1
    fp_l1 = testFalse(f'criterian20 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, letter_criterion.criterian20, p_l1)
    fn_l1 = testTrue(f'criterian20 Y/affine/L_10: ', f'{path}/texts/Y/affine/L_10_N_', 10000, letter_criterion.criterian20, p_l1)

    p = 1
    fp_l2 = testFalse(f'criterian20 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, bigram_criterion.criterian20, p)
    fn_l2 = testTrue(f'criterian20 Y/affine/L_10: ', f'{path}/texts/Y/affine/L_10_N_', 10000, bigram_criterion.criterian20, p)

    output('2.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 4
    p_l1 = 1
    fp_l1 = testFalse(f'criterian21 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, letter_criterion.criterian21, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian21 Y/affine/L_10: ', f'{path}/texts/Y/affine/L_10_N_', 10000, letter_criterion.criterian21, size_l1, p_l1)

    size = 50
    p = 2
    fp_l2 = testFalse(f'criterian21 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, bigram_criterion.criterian21, size, p)
    fn_l2 = testTrue(f'criterian21 Y/affine/L_10: ', f'{path}/texts/Y/affine/L_10_N_', 10000, bigram_criterion.criterian21, size, p)

    output('2.1',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 1
    p_l1 = 1
    fp_l1 = testFalse(f'criterian22 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, letter_criterion.criterian22, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian22 Y/affine/L_10: ', f'{path}/texts/Y/affine/L_10_N_', 10000, letter_criterion.criterian22, size_l1, p_l1)

    size = 1
    p = 1
    fp_l2 = testFalse(f'criterian22 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, bigram_criterion.criterian22, size, p)
    fn_l2 = testTrue(f'criterian22 Y/affine/L_10: ', f'{path}/texts/Y/affine/L_10_N_', 10000, bigram_criterion.criterian22, size, p)

    output('2.2',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 7
    p_l1 = 3
    fp_l1 = testFalse(f'criterian23 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, letter_criterion.criterian23, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian23 Y/affine/L_10: ', f'{path}/texts/Y/affine/L_10_N_', 10000, letter_criterion.criterian23, size_l1, p_l1)

    size = 10
    p = 1
    fp_l2 = testFalse(f'criterian23 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, bigram_criterion.criterian23, size, p)
    fn_l2 = testTrue(f'criterian23 Y/affine/L_10: ', f'{path}/texts/Y/affine/L_10_N_', 10000, bigram_criterion.criterian23, size, p)

    output('2.3',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = .03
    fp_l1 = testFalse(f'criterian40 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, letter_criterion.criterian40, p_l1)
    fn_l1 = testTrue(f'criterian40 Y/affine/L_10: ', f'{path}/texts/Y/affine/L_10_N_', 10000, letter_criterion.criterian40, p_l1)

    p = .02
    fp_l2 = testFalse(f'criterian40 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, bigram_criterion.criterian40, p)
    fn_l2 = testTrue(f'criterian40 Y/affine/L_10: ', f'{path}/texts/Y/affine/L_10_N_', 10000, bigram_criterion.criterian40, p)

    output('4.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 20
    p_l1 = 16
    fp_l1 = testFalse(f'criterian50 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, letter_criterion.criterian50, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian50 Y/affine/L_10: ', f'{path}/texts/Y/affine/L_10_N_', 10000, letter_criterion.criterian50, size_l1, p_l1)

    size = 200
    p = 199
    fp_l2 = testFalse(f'criterian50 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, bigram_criterion.criterian50, size, p)
    fn_l2 = testTrue(f'criterian50 Y/affine/L_10: ', f'{path}/texts/Y/affine/L_10_N_', 10000, bigram_criterion.criterian50, size, p)

    output('5.0',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = 1015
    fp_l1 = testFalseStructural('structural X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, letter_criterion.structuralCriterian, p_l1)
    fn_l1 = testTrueStructural('structural Y/L_10: ', f'{path}/texts/Y/affine/L_10_N_', 10000, letter_criterion.structuralCriterian, p_l1)

    p = 1009
    fp_l2 = testFalseStructural('structural X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, bigram_criterion.structuralCriterian, p)
    fn_l2 = testTrueStructural('structural Y/L_10: ', f'{path}/texts/Y/affine/L_10_N_', 10000, bigram_criterion.structuralCriterian, p)

    output('struct','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

def affine_L100(letter_criterion,bigram_criterion):
    print("affine L100:")

    p_l1 = 1
    fp_l1 = testFalse(f'criterian20 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, letter_criterion.criterian20, p_l1)
    fn_l1 = testTrue(f'criterian20 Y/affine/L_100: ', f'{path}/texts/Y/affine/L_100_N_', 10000, letter_criterion.criterian20, p_l1)

    p = 1
    fp_l2 = testFalse(f'criterian20 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, bigram_criterion.criterian20, p)
    fn_l2 = testTrue(f'criterian20 Y/affine/L_100: ', f'{path}/texts/Y/affine/L_100_N_', 10000, bigram_criterion.criterian20, p)

    output('2.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 1
    p_l1 = 1
    fp_l1 = testFalse(f'criterian21 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, letter_criterion.criterian21, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian21 Y/affine/L_100: ', f'{path}/texts/Y/affine/L_100_N_', 10000, letter_criterion.criterian21, size_l1, p_l1)
    
    size = 1
    p = 1
    fp_l2 = testFalse(f'criterian21 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, bigram_criterion.criterian21, size, p)
    fn_l2 = testTrue(f'criterian21 Y/affine/L_100: ', f'{path}/texts/Y/affine/L_100_N_', 10000, bigram_criterion.criterian21, size, p)

    output('2.1',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 5
    p_l1 = 1
    fp_l1 = testFalse(f'criterian22 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, letter_criterion.criterian22, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian22 Y/affine/L_100: ', f'{path}/texts/Y/affine/L_100_N_', 10000, letter_criterion.criterian22, size_l1, p_l1)
    
    size = 1
    p = 1
    fp_l2 = testFalse(f'criterian22 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, bigram_criterion.criterian22, size, p)
    fn_l2 = testTrue(f'criterian22 Y/affine/L_100: ', f'{path}/texts/Y/affine/L_100_N_', 10000, bigram_criterion.criterian22, size, p)

    output('2.2',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 1
    p_l1 = 2
    fp_l1 = testFalse(f'criterian23 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, letter_criterion.criterian23, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian23 Y/affine/L_100: ', f'{path}/texts/Y/affine/L_100_N_', 10000, letter_criterion.criterian23, size_l1, p_l1)

    size = 1
    p = 1
    fp_l2 = testFalse(f'criterian23 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, bigram_criterion.criterian23, size, p)
    fn_l2 = testTrue(f'criterian23 Y/affine/L_100: ', f'{path}/texts/Y/affine/L_100_N_', 10000, bigram_criterion.criterian23, size, p)
    
    output('2.3',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = 0.02
    fp_l1 = testFalse(f'criterian40 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, letter_criterion.criterian40, p_l1)
    fn_l1 = testTrue(f'criterian40 Y/affine/L_100: ', f'{path}/texts/Y/affine/L_100_N_', 10000, letter_criterion.criterian40, p_l1)
    
    p = 0.001
    fp_l2 = testFalse(f'criterian40 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, bigram_criterion.criterian40, p)
    fn_l2 = testTrue(f'criterian40 Y/affine/L_100: ', f'{path}/texts/Y/affine/L_100_N_', 10000, bigram_criterion.criterian40, p)
    
    output('4.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 100
    p_l1 = 71
    fp_l1 = testFalse(f'criterian50 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, letter_criterion.criterian50, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian50 Y/affine/L_100: ', f'{path}/texts/Y/affine/L_100_N_', 10000, letter_criterion.criterian50, size_l1, p_l1)
    
    size = 100
    p = 99
    fp_l2 = testFalse(f'criterian50 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, bigram_criterion.criterian50, size, p)
    fn_l2 = testTrue(f'criterian50 Y/affine/L_100: ', f'{path}/texts/Y/affine/L_100_N_', 10000, bigram_criterion.criterian50, size, p)

    output('5.0',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = 57.5
    fp_l1 = testFalseStructural('structural X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, letter_criterion.structuralCriterian, p_l1)
    fn_l1 = testTrueStructural('structural Y/affine/L_100_N_: ', f'{path}/texts/Y/affine/L_100_N_', 10000, letter_criterion.structuralCriterian, p_l1)

    p = 59
    fp_l2 = testFalseStructural('structural X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, bigram_criterion.structuralCriterian, p)
    fn_l2 = testTrueStructural('structural Y/affine/L_100_N_: ', f'{path}/texts/Y/affine/L_100_N_', 10000, bigram_criterion.structuralCriterian, p)
   
    output('struct','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

def affine_L1000(letter_criterion,bigram_criterion):
    print("affine L1000:")

    p_l1 = 3
    fp_l1 = testFalse(f'criterian20 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, letter_criterion.criterian20, p_l1)
    fn_l1 = testTrue(f'criterian20 Y/affine/L_1000: ', f'{path}/texts/Y/affine/L_1000_N_', 10000, letter_criterion.criterian20, p_l1)

    p = 3
    fp_l2 = testFalse(f'criterian20 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, bigram_criterion.criterian20, p)
    fn_l2 = testTrue(f'criterian20 Y/affine/L_1000: ', f'{path}/texts/Y/affine/L_1000_N_', 10000, bigram_criterion.criterian20, p)

    output('2.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 3
    p_l1 = 3
    fp_l1 = testFalse(f'criterian21 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, letter_criterion.criterian21, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian21 Y/affine/L_1000: ', f'{path}/texts/Y/affine/L_1000_N_', 10000, letter_criterion.criterian21, size_l1, p_l1)

    size = 3
    p = 3
    fp_l2 = testFalse(f'criterian21 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, bigram_criterion.criterian21, size, p)
    fn_l2 = testTrue(f'criterian21 Y/affine/L_1000: ', f'{path}/texts/Y/affine/L_1000_N_', 10000, bigram_criterion.criterian21, size, p)

    output('2.1',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 5
    p_l1 = 30
    fp_l1 = testFalse(f'criterian22 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, letter_criterion.criterian22, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian22 Y/affine/L_1000: ', f'{path}/texts/Y/affine/L_1000_N_', 10000, letter_criterion.criterian22, size_l1, p_l1)

    size = 5
    p = 3
    fp_l2 = testFalse(f'criterian22 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, bigram_criterion.criterian22, size, p)
    fn_l2 = testTrue(f'criterian22 Y/affine/L_1000: ', f'{path}/texts/Y/affine/L_1000_N_', 10000, bigram_criterion.criterian22, size, p)

    output('2.2',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 5
    p_l1 = 340
    fp_l1 = testFalse(f'criterian23 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, letter_criterion.criterian23, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian23 Y/affine/L_1000: ', f'{path}/texts/Y/affine/L_1000_N_', 10000, letter_criterion.criterian23, size_l1, p_l1)

    size = 5
    p = 5
    fp_l2 = testFalse(f'criterian23 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, bigram_criterion.criterian23, size, p)
    fn_l2 = testTrue(f'criterian23 Y/affine/L_1000: ', f'{path}/texts/Y/affine/L_1000_N_', 10000, bigram_criterion.criterian23, size, p)

    output('2.3',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = 0.005
    fp_l1 = testFalse(f'criterian40 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, letter_criterion.criterian40, p_l1)
    fn_l1 = testTrue(f'criterian40 Y/affine/L_1000: ', f'{path}/texts/Y/affine/L_1000_N_', 10000, letter_criterion.criterian40, p_l1)

    p = 0.005
    fp_l2 = testFalse(f'criterian40 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, bigram_criterion.criterian40, p)
    fn_l2 = testTrue(f'criterian40 Y/affine/L_1000: ', f'{path}/texts/Y/affine/L_1000_N_', 10000, bigram_criterion.criterian40, p)

    output('4.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 1000
    p_l1 = 967 #problem
    fp_l1 = testFalse(f'criterian50 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, letter_criterion.criterian50, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian50 Y/affine/L_1000: ', f'{path}/texts/Y/affine/L_1000_N_', 10000, letter_criterion.criterian50, size_l1, p_l1)

    size = 500
    p = 450 #problem:to slow 
    fp_l2 = testFalse(f'criterian50 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, bigram_criterion.criterian50, size, p)
    fn_l2 = testTrue(f'criterian50 Y/affine/L_1000: ', f'{path}/texts/Y/affine/L_1000_N_', 10000, bigram_criterion.criterian50, size, p)

    output('5.0',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = 49.0
    fp_l1 = testFalseStructural('structural X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, letter_criterion.structuralCriterian, p_l1)
    fn_l1 = testTrueStructural('structural Y/affine/L_1000: ', f'{path}/texts/Y/affine/L_1000_N_', 10000, letter_criterion.structuralCriterian, p_l1)

    p = 48
    fp_l2 = testFalseStructural('structural X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, bigram_criterion.structuralCriterian, p)
    fn_l2 = testTrueStructural('structural Y/affine/L_1000: ', f'{path}/texts/Y/affine/L_1000_N_', 10000, bigram_criterion.structuralCriterian, p)

    output('struct','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    
def affine_L10000(letter_criterion,bigram_criterion):
    print("affine L1000:")

    p_l1 = 3
    fp_l1 = testFalse(f'criterian20 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, letter_criterion.criterian20, p_l1)
    fn_l1 = testTrue(f'criterian20 Y/affine/L_10000: ', f'{path}/texts/Y/affine/L_10000_N_', 1000, letter_criterion.criterian20, p_l1)

    p = 3
    fp_l2 = testFalse(f'criterian20 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, bigram_criterion.criterian20, p)
    fn_l2 = testTrue(f'criterian20 Y/affine/L_10000: ', f'{path}/texts/Y/affine/L_10000_N_', 1000, bigram_criterion.criterian20, p)

    output('2.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 100
    p_l1 = 32
    fp_l1 = testFalse(f'criterian21 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, letter_criterion.criterian21, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian21 Y/affine/L_10000: ', f'{path}/texts/Y/affine/L_10000_N_', 1000, letter_criterion.criterian21, size_l1, p_l1)

    size = 100
    p = 32
    fp_l2 = testFalse(f'criterian21 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, bigram_criterion.criterian21, size, p)
    fn_l2 = testTrue(f'criterian21 Y/affine/L_10000: ', f'{path}/texts/Y/affine/L_10000_N_', 1000, bigram_criterion.criterian21, size, p)

    output('2.1',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 100
    p_l1 = 30
    fp_l1 = testFalse(f'criterian22 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, letter_criterion.criterian22, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian22 Y/affine/L_10000: ', f'{path}/texts/Y/affine/L_10000_N_', 1000, letter_criterion.criterian22, size_l1, p_l1)

    size = 100
    p = 15
    fp_l2 = testFalse(f'criterian22 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, bigram_criterion.criterian22, size, p)
    fn_l2 = testTrue(f'criterian22 Y/affine/L_10000: ', f'{path}/texts/Y/affine/L_10000_N_', 1000, bigram_criterion.criterian22, size, p)

    output('2.2',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 10
    p_l1 = 6000
    fp_l1 = testFalse(f'criterian23 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, letter_criterion.criterian23, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian23 Y/affine/L_10000: ', f'{path}/texts/Y/affine/L_10000_N_', 1000, letter_criterion.criterian23, size_l1, p_l1)

    size = 10
    p = 290
    fp_l2 = testFalse(f'criterian23 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, bigram_criterion.criterian23, size, p)
    fn_l2 = testTrue(f'criterian23 Y/affine/L_10000: ', f'{path}/texts/Y/affine/L_10000_N_', 1000, bigram_criterion.criterian23, size, p)

    output('2.3',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = 0.0005
    fp_l1 = testFalse(f'criterian40 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, letter_criterion.criterian40, p_l1)
    fn_l1 = testTrue(f'criterian40 Y/affine/L_10000: ', f'{path}/texts/Y/affine/L_10000_N_', 1000, letter_criterion.criterian40, p_l1)
    
    p = 0.0005
    fp_l2 = testFalse(f'criterian40 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, bigram_criterion.criterian40, p)
    fn_l2 = testTrue(f'criterian40 Y/affine/L_10000: ', f'{path}/texts/Y/affine/L_10000_N_', 1000, bigram_criterion.criterian40, p)
    
    output('4.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 100
    p_l1 = 67 #problem
    fp_l1 = testFalse(f'criterian50 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, letter_criterion.criterian50, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian50 Y/affine/L_10000: ', f'{path}/texts/Y/affine/L_10000_N_', 1000, letter_criterion.criterian50, size_l1, p_l1)

    size = 100
    p = 96 
    fp_l2 = testFalse(f'criterian50 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, bigram_criterion.criterian50, size, p)
    fn_l2 = testTrue(f'criterian50 Y/affine/L_10000: ', f'{path}/texts/Y/affine/L_10000_N_', 1000, bigram_criterion.criterian50, size, p)

    output('5.0',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = 66
    fp_l1 = testFalseStructural('structural X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, letter_criterion.structuralCriterian, p_l1)
    fn_l1 = testTrueStructural('structural Y/affine/L_10000: ', f'{path}/texts/Y/affine/L_10000_N_', 1000, letter_criterion.structuralCriterian, p_l1)

    p = 66
    fp_l2 = testFalseStructural('structural X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, bigram_criterion.structuralCriterian, p)
    fn_l2 = testTrueStructural('structural Y/affine/L_10000: ', f'{path}/texts/Y/affine/L_10000_N_', 1000, bigram_criterion.structuralCriterian, p)

    output('struct','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

def recursive_L10(letter_criterion,bigram_criterion):
    print("recursive L10:")

    p_l1 = 1
    fp_l1 = testFalse(f'criterian20 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, letter_criterion.criterian20, p_l1)
    fn_l1 = testTrue(f'criterian20 Y/recursive/L_10: ', f'{path}/texts/Y/recursive/L_10_N_', 10000, letter_criterion.criterian20, p_l1)

    p = 1
    fp_l2 = testFalse(f'criterian20 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, bigram_criterion.criterian20, p)
    fn_l2 = testTrue(f'criterian20 Y/recursive/L_10: ', f'{path}/texts/Y/recursive/L_10_N_', 10000, bigram_criterion.criterian20, p)

    output('2.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 5
    p_l1 = 2
    fp_l1 = testFalse(f'criterian21 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, letter_criterion.criterian21, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian21 Y/recursive/L_10: ', f'{path}/texts/Y/recursive/L_10_N_', 10000, letter_criterion.criterian21, size_l1, p_l1)

    size = 50
    p = 2
    fp_l2 = testFalse(f'criterian21 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, bigram_criterion.criterian21, size, p)
    fn_l2 = testTrue(f'criterian21 Y/recursive/L_10: ', f'{path}/texts/Y/recursive/L_10_N_', 10000, bigram_criterion.criterian21, size, p)

    output('2.1',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 1
    p_l1 = 1
    fp_l1 = testFalse(f'criterian22 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, letter_criterion.criterian22, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian22 Y/recursive/L_10: ', f'{path}/texts/Y/recursive/L_10_N_', 10000, letter_criterion.criterian22, size_l1, p_l1)

    size = 1
    p = 0   
    fp_l2 = testFalse(f'criterian22 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, bigram_criterion.criterian22, size, p)
    fn_l2 = testTrue(f'criterian22 Y/recursive/L_10: ', f'{path}/texts/Y/recursive/L_10_N_', 10000, bigram_criterion.criterian22, size, p)

    output('2.2',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 7
    p_l1 = 4
    fp_l1 = testFalse(f'criterian23 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, letter_criterion.criterian23, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian23 Y/recursive/L_10: ', f'{path}/texts/Y/recursive/L_10_N_', 10000, letter_criterion.criterian23, size_l1, p_l1)

    size = 15
    p = 1
    fp_l2 = testFalse(f'criterian23 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, bigram_criterion.criterian23, size, p)
    fn_l2 = testTrue(f'criterian23 Y/recursive/L_10: ', f'{path}/texts/Y/recursive/L_10_N_', 10000, bigram_criterion.criterian23, size, p)

    output('2.3',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = .03
    fp_l1 = testFalse(f'criterian40 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, letter_criterion.criterian40, p_l1)
    fn_l1 = testTrue(f'criterian40 Y/recursive/L_10: ', f'{path}/texts/Y/recursive/L_10_N_', 10000, letter_criterion.criterian40, p_l1)

    p = .005
    fp_l2 = testFalse(f'criterian40 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, bigram_criterion.criterian40, p)
    fn_l2 = testTrue(f'criterian40 Y/recursive/L_10: ', f'{path}/texts/Y/recursive/L_10_N_', 10000, bigram_criterion.criterian40, p)

    output('4.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 20
    p_l1 = 16
    fp_l1 = testFalse(f'criterian50 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, letter_criterion.criterian50, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian50 Y/recursive/L_10: ', f'{path}/texts/Y/recursive/L_10_N_', 10000, letter_criterion.criterian50, size_l1, p_l1)

    size = 200
    p = 199
    fp_l2 = testFalse(f'criterian50 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, bigram_criterion.criterian50, size, p)
    fn_l2 = testTrue(f'criterian50 Y/recursive/L_10: ', f'{path}/texts/Y/recursive/L_10_N_', 10000, bigram_criterion.criterian50, size, p)

    output('5.0',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = 1015
    fp_l1 = testFalseStructural('structural X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, letter_criterion.structuralCriterian, p_l1)
    fn_l1 = testTrueStructural('structural Y/recursive/L_10: ', f'{path}/texts/Y/recursive/L_10_N_', 10000, letter_criterion.structuralCriterian, p_l1)

    p = 1000
    fp_l2 = testFalseStructural('structural X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, bigram_criterion.structuralCriterian, p)
    fn_l2 = fp_l1 = testTrueStructural('structural Y/recursive/L_10: ', f'{path}/texts/Y/recursive/L_10_N_', 10000, bigram_criterion.structuralCriterian, p)

    output('struct','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

def recursive_L100(letter_criterion,bigram_criterion):
    print("recursive L100:")

    p_l1 = 3
    fp_l1 = testFalse(f'criterian20 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, letter_criterion.criterian20, p_l1)
    fn_l1 = testTrue(f'criterian20 Y/recursive/L_100: ', f'{path}/texts/Y/recursive/L_100_N_', 10000, letter_criterion.criterian20, p_l1)

    p = 1
    fp_l2 = testFalse(f'criterian20 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, bigram_criterion.criterian20, p)
    fn_l2 = testTrue(f'criterian20 Y/recursive/L_100: ', f'{path}/texts/Y/recursive/L_100_N_', 10000, bigram_criterion.criterian20, p)

    output('2.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 10
    p_l1 = 8
    fp_l1 = testFalse(f'criterian21 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, letter_criterion.criterian21, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian21 Y/recursive/L_100: ', f'{path}/texts/Y/recursive/L_100_N_', 10000, letter_criterion.criterian21, size_l1, p_l1)

    size = 10
    p = 1
    fp_l2 = testFalse(f'criterian21 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, bigram_criterion.criterian21, size, p)
    fn_l2 = testTrue(f'criterian21 Y/recursive/L_100: ', f'{path}/texts/Y/recursive/L_100_N_', 10000, bigram_criterion.criterian21, size, p)

    output('2.1',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 5
    p_l1 = 1
    fp_l1 = testFalse(f'criterian22 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, letter_criterion.criterian22, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian22 Y/recursive/L_100: ', f'{path}/texts/Y/recursive/L_100_N_', 10000, letter_criterion.criterian22, size_l1, p_l1)

    size = 1
    p = 1
    fp_l2 = testFalse(f'criterian22 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, bigram_criterion.criterian22, size, p)
    fn_l2 = testTrue(f'criterian22 Y/recursive/L_100: ', f'{path}/texts/Y/recursive/L_100_N_', 10000, bigram_criterion.criterian22, size, p)

    output('2.2',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 3
    p_l1 = 17
    fp_l1 = testFalse(f'criterian23 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, letter_criterion.criterian23, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian23 Y/recursive/L_100: ', f'{path}/texts/Y/recursive/L_100_N_', 10000, letter_criterion.criterian23, size_l1, p_l1)

    size = 3
    p = 1
    fp_l2 = testFalse(f'criterian23 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, bigram_criterion.criterian23, size, p)
    fn_l2 = testTrue(f'criterian23 Y/recursive/L_100: ', f'{path}/texts/Y/recursive/L_100_N_', 10000, bigram_criterion.criterian23, size, p)

    output('2.3',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = 0.005
    fp_l1 = testFalse(f'criterian40 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, letter_criterion.criterian40, p_l1)
    fn_l1 = testTrue(f'criterian40 Y/recursive/L_100: ', f'{path}/texts/Y/recursive/L_100_N_', 10000, letter_criterion.criterian40, p_l1)

    p = 0.005
    fp_l2 = testFalse(f'criterian40 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, bigram_criterion.criterian40, p)
    fn_l2 = testTrue(f'criterian40 Y/recursive/L_100: ', f'{path}/texts/Y/recursive/L_100_N_', 10000, bigram_criterion.criterian40, p)

    output('4.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 10
    p_l1 = 4
    fp_l1 = testFalse(f'criterian50 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, letter_criterion.criterian50, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian50 Y/recursive/L_100: ', f'{path}/texts/Y/recursive/L_100_N_', 10000, letter_criterion.criterian50, size_l1, p_l1)

    size = 50
    p = 49
    fp_l2 = testFalse(f'criterian50 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, bigram_criterion.criterian50, size, p)
    fn_l2 = testTrue(f'criterian50 Y/recursive/L_100: ', f'{path}/texts/Y/recursive/L_100_N_', 10000, bigram_criterion.criterian50, size, p)

    output('5.0',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = 58
    fp_l1 = testFalseStructural('structural X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, letter_criterion.structuralCriterian, p_l1)
    fn_l1 = testTrueStructural('structural Y/recursive/L_100_N_: ', f'{path}/texts/Y/recursive/L_100_N_', 10000, letter_criterion.structuralCriterian, p_l1)
    
    p = 58
    fp_l2 = testFalseStructural('structural X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, bigram_criterion.structuralCriterian, p)
    fn_l2 = testTrueStructural('structural Y/recursive/L_100_N_: ', f'{path}/texts/Y/recursive/L_100_N_', 10000, bigram_criterion.structuralCriterian, p)

    output('struct','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

def recursive_L1000(letter_criterion,bigram_criterion):
    print("recirsive L1000")

    p_l1 = 3
    fp_l1 = testFalse(f'criterian20 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, letter_criterion.criterian20, p_l1)
    fn_l1 = testTrue(f'criterian20 Y/recursive/L_1000: ', f'{path}/texts/Y/recursive/L_1000_N_', 10000, letter_criterion.criterian20, p_l1)

    p = 3
    fp_l2 = testFalse(f'criterian20 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, bigram_criterion.criterian20, p)
    fn_l2 = testTrue(f'criterian20 Y/recursive/L_1000: ', f'{path}/texts/Y/recursive/L_1000_N_', 10000, bigram_criterion.criterian20, p)

    output('2.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 10
    p_l1 = 8
    fp_l1 = testFalse(f'criterian21 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, letter_criterion.criterian21, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian21 Y/recursive/L_1000: ', f'{path}/texts/Y/recursive/L_1000_N_', 10000, letter_criterion.criterian21, size_l1, p_l1)

    size = 10
    p = 8
    fp_l2 = testFalse(f'criterian21 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, bigram_criterion.criterian21, size, p)
    fn_l2 = testTrue(f'criterian21 Y/recursive/L_1000: ', f'{path}/texts/Y/recursive/L_1000_N_', 10000, bigram_criterion.criterian21, size, p)

    output('2.1',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 5
    p_l1 = 1
    fp_l1 = testFalse(f'criterian22 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, letter_criterion.criterian22, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian22 Y/recursive/L_1000: ', f'{path}/texts/Y/recursive/L_1000_N_', 10000, letter_criterion.criterian22, size_l1, p_l1)

    size = 5
    p = 1
    fp_l2 = testFalse(f'criterian22 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, bigram_criterion.criterian22, size, p)
    fn_l2 = testTrue(f'criterian22 Y/recursive/L_1000: ', f'{path}/texts/Y/recursive/L_1000_N_', 10000, bigram_criterion.criterian22, size, p)

    output('2.2',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 3
    p_l1 = 190
    fp_l1 = testFalse(f'criterian23 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, letter_criterion.criterian23, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian23 Y/recursive/L_1000: ', f'{path}/texts/Y/recursive/L_1000_N_', 10000, letter_criterion.criterian23, size_l1, p_l1)

    size = 50
    p = 210
    fp_l2 = testFalse(f'criterian23 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, bigram_criterion.criterian23, size, p)
    fn_l2 = testTrue(f'criterian23 Y/recursive/L_1000: ', f'{path}/texts/Y/recursive/L_1000_N_', 10000, bigram_criterion.criterian23, size, p)

    output('2.3',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = 0.005
    fp_l1 = testFalse(f'criterian40 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, letter_criterion.criterian40, p_l1)
    fn_l1 = testTrue(f'criterian40 Y/recursive/L_1000: ', f'{path}/texts/Y/recursive/L_1000_N_', 10000, letter_criterion.criterian40, p_l1)

    p = 0.005
    fp_l2 = testFalse(f'criterian40 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, bigram_criterion.criterian40, p)
    fn_l2 = testTrue(f'criterian40 Y/recursive/L_1000: ', f'{path}/texts/Y/recursive/L_1000_N_', 10000, bigram_criterion.criterian40, p)

    output('4.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 100
    p_l1 = 68 #promlem
    fp_l1 = testFalse(f'criterian50 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, letter_criterion.criterian50, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian50 Y/recursive/L_1000: ', f'{path}/texts/Y/recursive/L_1000_N_', 10000, letter_criterion.criterian50, size_l1, p_l1)

    size = 100
    p = 98 #promlem
    fp_l2 = testFalse(f'criterian50 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, bigram_criterion.criterian50, size, p)
    fn_l2 = testTrue(f'criterian50 Y/recursive/L_1000: ', f'{path}/texts/Y/recursive/L_1000_N_', 10000, bigram_criterion.criterian50, size, p)

    output('5.0',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = 49
    fp_l1 = testFalseStructural('structural X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, letter_criterion.structuralCriterian, p_l1)
    fn_l1 = testTrueStructural('structural Y/recursive/L_1000_N_: ', f'{path}/texts/Y/recursive/L_1000_N_', 10000, letter_criterion.structuralCriterian, p_l1)

    p = 47 #problem
    fp_l2 = testFalseStructural('structural X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, bigram_criterion.structuralCriterian, p)
    fn_l2 = testTrueStructural('structural Y/recursive/L_1000_N_: ', f'{path}/texts/Y/recursive/L_1000_N_', 10000, bigram_criterion.structuralCriterian, p)

    output('struct','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

def recursive_L10000(letter_criterion,bigram_criterion):
    print("recirsive L10000:")

    p_l1 = 3
    fp_l1 = testFalse(f'criterian20 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, letter_criterion.criterian20, p_l1)
    fn_l1 = testTrue(f'criterian20 Y/recursive/L_10000: ', f'{path}/texts/Y/recursive/L_10000_N_', 1000, letter_criterion.criterian20, p_l1)

    p = 3
    fp_l2 = testFalse(f'criterian20 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, bigram_criterion.criterian20, p)
    fn_l2 = testTrue(f'criterian20 Y/recursive/L_10000: ', f'{path}/texts/Y/recursive/L_10000_N_', 1000, bigram_criterion.criterian20, p)

    output('2.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 100
    p_l1 = 32
    fp_l1 = testFalse(f'criterian21 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, letter_criterion.criterian21, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian21 Y/recursive/L_10000: ', f'{path}/texts/Y/recursive/L_10000_N_', 1000, letter_criterion.criterian21, size_l1, p_l1)

    size = 100
    p = 32
    fp_l2 = testFalse(f'criterian21 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, bigram_criterion.criterian21, size, p)
    fn_l2 = testTrue(f'criterian21 Y/recursive/L_10000: ', f'{path}/texts/Y/recursive/L_10000_N_', 1000, bigram_criterion.criterian21, size, p)

    output('2.1',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 10
    p_l1 = 350
    fp_l1 = testFalse(f'criterian22 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, letter_criterion.criterian22, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian22 Y/recursive/L_10000: ', f'{path}/texts/Y/recursive/L_10000_N_', 1000, letter_criterion.criterian22, size_l1, p_l1)

    size = 1
    p = 100
    fp_l2 = testFalse(f'criterian22 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, bigram_criterion.criterian22, size, p)
    fn_l2 = testTrue(f'criterian22 Y/recursive/L_10000: ', f'{path}/texts/Y/recursive/L_10000_N_', 1000, bigram_criterion.criterian22, size, p)

    output('2.2',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 10
    p_l1 = 5900
    fp_l1 = testFalse(f'criterian23 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, letter_criterion.criterian23, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian23 Y/recursive/L_10000: ', f'{path}/texts/Y/recursive/L_10000_N_', 1000, letter_criterion.criterian23, size_l1, p_l1)

    size = 10
    p = 1000
    fp_l2 = testFalse(f'criterian23 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, bigram_criterion.criterian23, size, p)
    fn_l2 = testTrue(f'criterian23 Y/recursive/L_10000: ', f'{path}/texts/Y/recursive/L_10000_N_', 1000, bigram_criterion.criterian23, size, p)

    output('2.3',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = 0.001
    fp_l1 = testFalse(f'criterian40 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, letter_criterion.criterian40, p_l1)
    fn_l1 = testTrue(f'criterian40 Y/recursive/L_10000: ', f'{path}/texts/Y/recursive/L_10000_N_', 1000, letter_criterion.criterian40, p_l1)

    p = 0.001
    fp_l2 = testFalse(f'criterian40 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, bigram_criterion.criterian40, p)
    fn_l2 = testTrue(f'criterian40 Y/recursive/L_10000: ', f'{path}/texts/Y/recursive/L_10000_N_', 1000, bigram_criterion.criterian40, p)

    output('4.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 200
    p_l1 = 167 #problem
    fp_l1 = testFalse(f'criterian50 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, letter_criterion.criterian50, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian50 Y/recursive/L_10000: ', f'{path}/texts/Y/recursive/L_10000_N_', 1000, letter_criterion.criterian50, size_l1, p_l1)

    size = 200
    p = 180 #problem 180,
    fp_l2 = testFalse(f'criterian50 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, bigram_criterion.criterian50, size, p)
    fn_l2 = testTrue(f'criterian50 Y/recursive/L_10000: ', f'{path}/texts/Y/recursive/L_10000_N_', 1000, bigram_criterion.criterian50, size, p)

    output('5.0',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = 66 #problem
    fp_l1 = testFalseStructural('structural X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, letter_criterion.structuralCriterian, p_l1)
    fn_l1 = testTrueStructural('structural Y/recursive/L_10000: ', f'{path}/texts/Y/recursive/L_10000_N_', 1000, letter_criterion.structuralCriterian, p_l1)

    p = 66 #problem
    fp_l2 = testFalseStructural('structural X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, bigram_criterion.structuralCriterian, p)
    fn_l2 = testTrueStructural('structural Y/recursive/L_10000: ', f'{path}/texts/Y/recursive/L_10000_N_', 1000, bigram_criterion.structuralCriterian, p)

    output('struct','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

def uniform_L10(letter_criterion,bigram_criterion):
    print("uniform L10:")

    p_l1 = 1
    fp_l1 = testFalse(f'criterian20 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, letter_criterion.criterian20, p_l1)
    fn_l1 = testTrue(f'criterian20 Y/uniform/L_10: ', f'{path}/texts/Y/uniform/L_10_N_', 10000, letter_criterion.criterian20, p_l1)

    p = 0
    fp_l2 = testFalse(f'criterian20 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, bigram_criterion.criterian20, p)
    fn_l2 = testTrue(f'criterian20 Y/uniform/L_10: ', f'{path}/texts/Y/uniform/L_10_N_', 10000, bigram_criterion.criterian20, p)

    output('2.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 7
    p_l1 = 3
    fp_l1 = testFalse(f'criterian21 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, letter_criterion.criterian21, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian21 Y/uniform/L_10: ', f'{path}/texts/Y/uniform/L_10_N_', 10000, letter_criterion.criterian21, size_l1, p_l1)

    size = 10
    p = 1
    fp_l2 = testFalse(f'criterian21 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, bigram_criterion.criterian21, size, p)
    fn_l2 = testTrue(f'criterian21 Y/uniform/L_10: ', f'{path}/texts/Y/uniform/L_10_N_', 10000, bigram_criterion.criterian21, size, p)

    output('2.1',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 1
    p_l1 = 1
    fp_l1 = testFalse(f'criterian22 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, letter_criterion.criterian22, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian22 Y/uniform/L_10: ', f'{path}/texts/Y/uniform/L_10_N_', 10000, letter_criterion.criterian22, size_l1, p_l1)

    size = 1
    p = 0
    fp_l2 = testFalse(f'criterian22 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, bigram_criterion.criterian22, size, p)
    fn_l2 = testTrue(f'criterian22 Y/uniform/L_10: ', f'{path}/texts/Y/uniform/L_10_N_', 10000, bigram_criterion.criterian22, size, p)

    output('2.2',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 7
    p_l1 = 4
    fp_l1 = testFalse(f'criterian23 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, letter_criterion.criterian23, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian23 Y/uniform/L_10: ', f'{path}/texts/Y/uniform/L_10_N_', 10000, letter_criterion.criterian23, size_l1, p_l1)

    size = 7
    p = 1
    fp_l2 = testFalse(f'criterian23 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, bigram_criterion.criterian23, size, p)
    fn_l2 = testTrue(f'criterian23 Y/uniform/L_10: ', f'{path}/texts/Y/uniform/L_10_N_', 10000, bigram_criterion.criterian23, size, p)

    output('2.3',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = .028
    fp_l1 = testFalse(f'criterian40 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, letter_criterion.criterian40, p_l1)
    fn_l1 = testTrue(f'criterian40 Y/uniform/L_10: ', f'{path}/texts/Y/uniform/L_10_N_', 10000, letter_criterion.criterian40, p_l1)

    p = .0044
    fp_l2 = testFalse(f'criterian40 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, bigram_criterion.criterian40, p)
    fn_l2 = testTrue(f'criterian40 Y/uniform/L_10: ', f'{path}/texts/Y/uniform/L_10_N_', 10000, bigram_criterion.criterian40, p)
    
    output('4.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 20
    p_l1 = 16
    fp_l1 = testFalse(f'criterian50 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, letter_criterion.criterian50, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian50 Y/uniform/L_10: ', f'{path}/texts/Y/uniform/L_10_N_', 10000, letter_criterion.criterian50, size_l1, p_l1)

    size = 20
    p = 19
    fp_l2 = testFalse(f'criterian50 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, bigram_criterion.criterian50, size, p)
    fn_l2 = testTrue(f'criterian50 Y/uniform/L_10: ', f'{path}/texts/Y/uniform/L_10_N_', 10000, bigram_criterion.criterian50, size, p)

    output('5.0',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = 1015 #problem
    fp_l1 = testFalseStructural('structural X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, letter_criterion.structuralCriterian, p_l1)
    fn_l1 = testTrueStructural('structural Y/uniform/L_10: ', f'{path}/texts/Y/uniform/L_10_N_', 10000, letter_criterion.structuralCriterian, p_l1)

    p = 1015 #problem
    fp_l2 = testFalseStructural('structural X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, bigram_criterion.structuralCriterian, p)
    fn_l2 = testTrueStructural('structural Y/uniform/L_10: ', f'{path}/texts/Y/uniform/L_10_N_', 10000, bigram_criterion.structuralCriterian, p)

    output('struct','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

def uniform_L100(letter_criterion,bigram_criterion):
    print("uniform_L100:")

    p_l1 = 18
    fp_l1 = testFalse(f'criterian20 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, letter_criterion.criterian20, p_l1)
    fn_l1 = testTrue(f'criterian20 Y/uniform/L_100: ', f'{path}/texts/Y/uniform/L_100_N_', 10000, letter_criterion.criterian20, p_l1)

    p = 1
    fp_l2 = testFalse(f'criterian20 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, bigram_criterion.criterian20, p)
    fn_l2 = testTrue(f'criterian20 Y/uniform/L_100: ', f'{path}/texts/Y/uniform/L_100_N_', 10000, bigram_criterion.criterian20, p)

    output('2.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 20
    p_l1 = 19
    fp_l1 = testFalse(f'criterian21 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, letter_criterion.criterian21, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian21 Y/uniform/L_100: ', f'{path}/texts/Y/uniform/L_100_N_', 10000, letter_criterion.criterian21, size_l1, p_l1)

    size = 20
    p = 6
    fp_l2 = testFalse(f'criterian21 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, bigram_criterion.criterian21, size, p)
    fn_l2 = testTrue(f'criterian21 Y/uniform/L_100: ', f'{path}/texts/Y/uniform/L_100_N_', 10000, bigram_criterion.criterian21, size, p)

    output('2.1',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 5
    p_l1 = 3
    fp_l1 = testFalse(f'criterian22 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, letter_criterion.criterian22, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian22 Y/uniform/L_100: ', f'{path}/texts/Y/uniform/L_100_N_', 10000, letter_criterion.criterian22, size_l1, p_l1)

    size = 1
    p = 1
    fp_l2 = testFalse(f'criterian22 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, bigram_criterion.criterian22, size, p)
    fn_l2 = testTrue(f'criterian22 Y/uniform/L_100: ', f'{path}/texts/Y/uniform/L_100_N_', 10000, bigram_criterion.criterian22, size, p)

    output('2.2',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 5
    p_l1 = 20
    fp_l1 = testFalse(f'criterian23 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, letter_criterion.criterian23, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian23 Y/uniform/L_100: ', f'{path}/texts/Y/uniform/L_100_N_', 10000, letter_criterion.criterian23, size_l1, p_l1)

    size = 5
    p = 2
    fp_l2 = testFalse(f'criterian23 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, bigram_criterion.criterian23, size, p)
    fn_l2 = testTrue(f'criterian23 Y/uniform/L_100: ', f'{path}/texts/Y/uniform/L_100_N_', 10000, bigram_criterion.criterian23, size, p)

    output('2.3',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = .01
    fp_l1 = testFalse(f'criterian40 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, letter_criterion.criterian40, p_l1)
    fn_l1 = testTrue(f'criterian40 Y/uniform/L_100: ', f'{path}/texts/Y/uniform/L_100_N_', 10000, letter_criterion.criterian40, p_l1)

    p = .0025
    fp_l2 = testFalse(f'criterian40 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, bigram_criterion.criterian40, p)
    fn_l2 = testTrue(f'criterian40 Y/uniform/L_100: ', f'{path}/texts/Y/uniform/L_100_N_', 10000, bigram_criterion.criterian40, p)
    
    output('4.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 20
    p_l1 = 3
    fp_l1 = testFalse(f'criterian50 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, letter_criterion.criterian50, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian50 Y/uniform/L_100: ', f'{path}/texts/Y/uniform/L_100_N_', 10000, letter_criterion.criterian50, size_l1, p_l1)

    size = 20
    p = 19
    fp_l2 = testFalse(f'criterian50 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, bigram_criterion.criterian50, size, p)
    fn_l2 = testTrue(f'criterian50 Y/uniform/L_100: ', f'{path}/texts/Y/uniform/L_100_N_', 10000, bigram_criterion.criterian50, size, p)

    output('5.0',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = 60 #problem
    fp_l1 = testFalseStructural('structural X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, letter_criterion.structuralCriterian, p_l1)
    fn_l1 = testTrueStructural('structural Y/uniform/L_100: ', f'{path}/texts/Y/uniform/L_100_N_', 10000, letter_criterion.structuralCriterian, p_l1)

    p = 59 #problem
    fp_l2 = testFalseStructural('structural X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, bigram_criterion.structuralCriterian, p)
    fn_l2 = testTrueStructural('structural Y/uniform/L_100: ', f'{path}/texts/Y/uniform/L_100_N_', 10000, bigram_criterion.structuralCriterian, p)

    output('struct','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

def uniform_L1000(letter_criterion,bigram_criterion):
    print("uniform_L1000:")

    p_l1 = 18
    fp_l1 = testFalse(f'criterian20 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, letter_criterion.criterian20, p_l1)
    fn_l1 = testTrue(f'criterian20 Y/uniform/L_1000: ', f'{path}/texts/Y/uniform/L_1000_N_', 10000, letter_criterion.criterian20, p_l1)

    p = 18
    fp_l2 = testFalse(f'criterian20 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, bigram_criterion.criterian20, p)
    fn_l2 = testTrue(f'criterian20 Y/uniform/L_1000: ', f'{path}/texts/Y/uniform/L_1000_N_', 10000, bigram_criterion.criterian20, p)

    output('2.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 20
    p_l1 = 20
    fp_l1 = testFalse(f'criterian21 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, letter_criterion.criterian21, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian21 Y/uniform/L_1000: ', f'{path}/texts/Y/uniform/L_1000_N_', 10000, letter_criterion.criterian21, size_l1, p_l1)

    size = 20
    p = 20
    fp_l2 = testFalse(f'criterian21 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, bigram_criterion.criterian21, size, p)
    fn_l2 = testTrue(f'criterian21 Y/uniform/L_1000: ', f'{path}/texts/Y/uniform/L_1000_N_', 10000, bigram_criterion.criterian21, size, p)

    output('2.1',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 5
    p_l1 = 32
    fp_l1 = testFalse(f'criterian22 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, letter_criterion.criterian22, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian22 Y/uniform/L_1000: ', f'{path}/texts/Y/uniform/L_1000_N_', 10000, letter_criterion.criterian22, size_l1, p_l1)

    size = 5
    p = 3
    fp_l2 = testFalse(f'criterian22 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, bigram_criterion.criterian22, size, p)
    fn_l2 = testTrue(f'criterian22 Y/uniform/L_1000: ', f'{path}/texts/Y/uniform/L_1000_N_', 10000, bigram_criterion.criterian22, size, p)

    output('2.2',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 5
    p_l1 = 200
    fp_l1 = testFalse(f'criterian23 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, letter_criterion.criterian23, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian23 Y/uniform/L_1000: ', f'{path}/texts/Y/uniform/L_1000_N_', 10000, letter_criterion.criterian23, size_l1, p_l1)

    size = 5
    p = 15
    fp_l2 = testFalse(f'criterian23 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, bigram_criterion.criterian23, size, p)
    fn_l2 = testTrue(f'criterian23 Y/uniform/L_1000: ', f'{path}/texts/Y/uniform/L_1000_N_', 10000, bigram_criterion.criterian23, size, p)

    output('2.3',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = .01
    fp_l1 = testFalse(f'criterian40 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, letter_criterion.criterian40, p_l1)
    fn_l1 = testTrue(f'criterian40 Y/uniform/L_1000: ', f'{path}/texts/Y/uniform/L_1000_N_', 10000, letter_criterion.criterian40, p_l1)
    
    p = .003
    fp_l2 = testFalse(f'criterian40 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, bigram_criterion.criterian40, p)
    fn_l2 = testTrue(f'criterian40 Y/uniform/L_1000: ', f'{path}/texts/Y/uniform/L_1000_N_', 10000, bigram_criterion.criterian40, p)
    
    output('4.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 500
    p_l1 = 467 #problem
    fp_l1 = testFalse(f'criterian50 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, letter_criterion.criterian50, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian50 Y/uniform/L_1000: ', f'{path}/texts/Y/uniform/L_1000_N_', 10000, letter_criterion.criterian50, size_l1, p_l1)

    size = 500
    p = 210 #problem 470
    fp_l2 = testFalse(f'criterian50 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, bigram_criterion.criterian50, size, p)
    fn_l2 = testTrue(f'criterian50 Y/uniform/L_1000: ', f'{path}/texts/Y/uniform/L_1000_N_', 10000, bigram_criterion.criterian50, size, p)

    output('5.0',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = 47.5
    fp_l1 = testFalseStructural('structural X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, letter_criterion.structuralCriterian, p_l1)
    fn_l1 = testTrueStructural('structural Y/uniform/L_1000: ', f'{path}/texts/Y/uniform/L_1000_N_', 10000, letter_criterion.structuralCriterian, p_l1)

    p = 47.5
    fp_l2 = testFalseStructural('structural X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, bigram_criterion.structuralCriterian, p)
    fn_l2 = testTrueStructural('structural Y/uniform/L_1000: ', f'{path}/texts/Y/uniform/L_1000_N_', 10000, bigram_criterion.structuralCriterian, p)

    output('struct','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)


def uniform_L10000(letter_criterion,bigram_criterion):
    print("uniform_L10000:")

    p_l1 = 18
    fp_l1 = testFalse(f'criterian20 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, letter_criterion.criterian20, p_l1)
    fn_l1 = testTrue(f'criterian20 Y/uniform/L_10000: ', f'{path}/texts/Y/uniform/L_10000_N_', 1000, letter_criterion.criterian20, p_l1)

    p = 16
    fp_l2 = testFalse(f'criterian20 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, bigram_criterion.criterian20, p)
    fn_l2 = testTrue(f'criterian20 Y/uniform/L_10000: ', f'{path}/texts/Y/uniform/L_10000_N_', 1000, bigram_criterion.criterian20, p)

    output('2.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 20
    p_l1 = 20
    fp_l1 = testFalse(f'criterian21 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, letter_criterion.criterian21, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian21 Y/uniform/L_10000: ', f'{path}/texts/Y/uniform/L_10000_N_', 1000, letter_criterion.criterian21, size_l1, p_l1)

    size = 200
    p = 192
    fp_l2 = testFalse(f'criterian21 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, bigram_criterion.criterian21, size, p)
    fn_l2 = testTrue(f'criterian21 Y/uniform/L_10000: ', f'{path}/texts/Y/uniform/L_10000_N_', 1000, bigram_criterion.criterian21, size, p)

    output('2.1',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 5
    p_l1 = 550
    fp_l1 = testFalse(f'criterian22 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, letter_criterion.criterian22, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian22 Y/uniform/L_10000: ', f'{path}/texts/Y/uniform/L_10000_N_', 1000, letter_criterion.criterian22, size_l1, p_l1)

    size = 5
    p = 12
    fp_l2 = testFalse(f'criterian22 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, bigram_criterion.criterian22, size, p)
    fn_l2 = testTrue(f'criterian22 Y/uniform/L_10000: ', f'{path}/texts/Y/uniform/L_10000_N_', 1000, bigram_criterion.criterian22, size, p)

    output('2.2',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 5
    p_l1 = 3600
    fp_l1 = testFalse(f'criterian23 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, letter_criterion.criterian23, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian23 Y/uniform/L_10000: ', f'{path}/texts/Y/uniform/L_10000_N_', 1000, letter_criterion.criterian23, size_l1, p_l1)

    size = 5
    p = 70
    fp_l2 = testFalse(f'criterian23 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, bigram_criterion.criterian23, size, p)
    fn_l2 = testTrue(f'criterian23 Y/uniform/L_10000: ', f'{path}/texts/Y/uniform/L_10000_N_', 1000, bigram_criterion.criterian23, size, p)

    output('2.3',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = .01
    fp_l1 = testFalse(f'criterian40 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, letter_criterion.criterian40, p_l1)
    fn_l1 = testTrue(f'criterian40 Y/uniform/L_10000: ', f'{path}/texts/Y/uniform/L_10000_N_', 1000, letter_criterion.criterian40, p_l1)
    
    p = .003
    fp_l2 = testFalse(f'criterian40 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, bigram_criterion.criterian40, p)
    fn_l2 = testTrue(f'criterian40 Y/uniform/L_10000: ', f'{path}/texts/Y/uniform/L_10000_N_', 1000, bigram_criterion.criterian40, p)
    
    output('4.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 500
    p_l1 = 467 #problem
    fp_l1 = testFalse(f'criterian50 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, letter_criterion.criterian50, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian50 Y/uniform/L_10000: ', f'{path}/texts/Y/uniform/L_10000_N_', 1000, letter_criterion.criterian50, size_l1, p_l1)

    size = 500
    p = 29 #problem 280
    fp_l2 = testFalse(f'criterian50 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, bigram_criterion.criterian50, size, p)
    fn_l2 = testTrue(f'criterian50 Y/uniform/L_10000: ', f'{path}/texts/Y/uniform/L_10000_N_', 1000, bigram_criterion.criterian50, size, p)

    output('5.0',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = 54.7
    fp_l1 = testFalseStructural('structural X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, letter_criterion.structuralCriterian, p_l1)
    fn_l1 = testTrueStructural('structural Y/uniform/L_10000: ', f'{path}/texts/Y/uniform/L_10000_N_', 1000, letter_criterion.structuralCriterian, p_l1)

    p = 54.7
    fp_l2 = testFalseStructural('structural X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, bigram_criterion.structuralCriterian, p)
    fn_l2 = testTrueStructural('structural Y/uniform/L_10000: ', f'{path}/texts/Y/uniform/L_10000_N_', 1000, bigram_criterion.structuralCriterian, p)

    output('struct','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

def vigenere_L10_K1(letter_criterion,bigram_criterion):
    print("vigenere_L10_K1:")

    p_l1 = 1
    fp_l1 = testFalse(f'criterian20 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, letter_criterion.criterian20, p_l1)
    fn_l1 = testTrue(f'criterian20 Y/vigenere/KEY_1_L_10: ', f'{path}/texts/Y/vigenere/KEY_1_L_10_N_', 10000, letter_criterion.criterian20, p_l1)

    p = 0
    fp_l2 = testFalse(f'criterian20 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, bigram_criterion.criterian20, p)
    fn_l2 = testTrue(f'criterian20 Y/vigenere/KEY_1_L_10: ', f'{path}/texts/Y/vigenere/KEY_1_L_10_N_', 10000, bigram_criterion.criterian20, p)

    output('2.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 7
    p_l1 = 3
    fp_l1 = testFalse(f'criterian21 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, letter_criterion.criterian21, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian21 Y/vigenere/KEY_1_L_10: ', f'{path}/texts/Y/vigenere/KEY_1_L_10_N_', 10000, letter_criterion.criterian21, size_l1, p_l1)

    size = 10
    p = 1
    fp_l2 = testFalse(f'criterian21 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, bigram_criterion.criterian21, size, p)
    fn_l2 = testTrue(f'criterian21 Y/vigenere/KEY_1_L_10: ', f'{path}/texts/Y/vigenere/KEY_1_L_10_N_', 10000, bigram_criterion.criterian21, size, p)

    output('2.1',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 1
    p_l1 = 1
    fp_l1 = testFalse(f'criterian22 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, letter_criterion.criterian22, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian22 Y/vigenere/KEY_1_L_10: ', f'{path}/texts/Y/vigenere/KEY_1_L_10_N_', 10000, letter_criterion.criterian22, size_l1, p_l1)

    size = 1
    p = 0
    fp_l2 = testFalse(f'criterian22 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, bigram_criterion.criterian22, size, p)
    fn_l2 = testTrue(f'criterian22 Y/vigenere/KEY_1_L_10: ', f'{path}/texts/Y/vigenere/KEY_1_L_10_N_', 10000, bigram_criterion.criterian22, size, p)

    output('2.2',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 7
    p_l1 = 4
    fp_l1 = testFalse(f'criterian23 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, letter_criterion.criterian23, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian23 Y/vigenere/KEY_1_L_10: ', f'{path}/texts/Y/vigenere/KEY_1_L_10_N_', 10000, letter_criterion.criterian23, size_l1, p_l1)

    size = 100
    p = 3
    fp_l2 = testFalse(f'criterian23 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, bigram_criterion.criterian23, size, p)
    fn_l2 = testTrue(f'criterian23 Y/vigenere/KEY_1_L_10: ', f'{path}/texts/Y/vigenere/KEY_1_L_10_N_', 10000, bigram_criterion.criterian23, size, p)

    output('2.3',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = .03
    fp_l1 = testFalse(f'criterian40 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, letter_criterion.criterian40, p_l1)
    fn_l1 = testTrue(f'criterian40 Y/vigenere/KEY_1_L_10: ', f'{path}/texts/Y/vigenere/KEY_1_L_10_N_', 10000, letter_criterion.criterian40, p_l1)
    
    p = .005
    fp_l2 = testFalse(f'criterian40 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, bigram_criterion.criterian40, p)
    fn_l2 = testTrue(f'criterian40 Y/vigenere/KEY_1_L_10: ', f'{path}/texts/Y/vigenere/KEY_1_L_10_N_', 10000, bigram_criterion.criterian40, p)
    
    output('4.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 20
    p_l1 = 16
    fp_l1 = testFalse(f'criterian50 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, letter_criterion.criterian50, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian50 Y/vigenere/KEY_1_L_10: ', f'{path}/texts/Y/vigenere/KEY_1_L_10_N_', 10000, letter_criterion.criterian50, size_l1, p_l1)

    size = 100
    p = 99
    fp_l2 = testFalse(f'criterian50 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, bigram_criterion.criterian50, size, p)
    fn_l2 = testTrue(f'criterian50 Y/vigenere/KEY_1_L_10: ', f'{path}/texts/Y/vigenere/KEY_1_L_10_N_', 10000, bigram_criterion.criterian50, size, p)

    output('5.0',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = 1015 #problem
    fp_l1 = testFalseStructural('structural X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, letter_criterion.structuralCriterian, p_l1)
    fn_l1 = testTrueStructural('structural Y/vigenere/KEY_1_L_10: ', f'{path}/texts/Y/vigenere/KEY_1_L_10_N_', 10000, letter_criterion.structuralCriterian, p_l1)

    p = 1015 
    fp_l2 = testFalseStructural('structural X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, bigram_criterion.structuralCriterian, p)
    fn_l2 = testTrueStructural('structural Y/vigenere/KEY_1_L_10: ', f'{path}/texts/Y/vigenere/KEY_1_L_10_N_', 10000, bigram_criterion.structuralCriterian, p)

    output('struct','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

def vigenere_L100_K_1(letter_criterion,bigram_criterion):
    print("vigenere_L100_K_1:")

    p_l1 = 10
    fp_l1 = testFalse(f'criterian20 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, letter_criterion.criterian20, p_l1)
    fn_l1 = testTrue(f'criterian20 Y/vigenere/KEY_1_L_100: ', f'{path}/texts/Y/vigenere/KEY_1_L_100_N_', 10000, letter_criterion.criterian20, p_l1)

    p = 1
    fp_l2 = testFalse(f'criterian20 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, bigram_criterion.criterian20, p)
    fn_l2 = testTrue(f'criterian20 Y/vigenere/KEY_1_L_100: ', f'{path}/texts/Y/vigenere/KEY_1_L_100_N_', 10000, bigram_criterion.criterian20, p)

    output('2.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 7
    p_l1 = 7
    fp_l1 = testFalse(f'criterian21 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, letter_criterion.criterian21, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian21 Y/vigenere/KEY_1_L_100: ', f'{path}/texts/Y/vigenere/KEY_1_L_100_N_', 10000, letter_criterion.criterian21, size_l1, p_l1)

    size = 7
    p = 3
    fp_l2 = testFalse(f'criterian21 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, bigram_criterion.criterian21, size, p)
    fn_l2 = testTrue(f'criterian21 Y/vigenere/KEY_1_L_100: ', f'{path}/texts/Y/vigenere/KEY_1_L_100_N_', 10000, bigram_criterion.criterian21, size, p)

    output('2.1',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 1
    p_l1 = 6
    fp_l1 = testFalse(f'criterian22 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, letter_criterion.criterian22, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian22 Y/vigenere/KEY_1_L_100: ', f'{path}/texts/Y/vigenere/KEY_1_L_100_N_', 10000, letter_criterion.criterian22, size_l1, p_l1)

    size = 1
    p = 1
    fp_l2 = testFalse(f'criterian22 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, bigram_criterion.criterian22, size, p)
    fn_l2 = testTrue(f'criterian22 Y/vigenere/KEY_1_L_100: ', f'{path}/texts/Y/vigenere/KEY_1_L_100_N_', 10000, bigram_criterion.criterian22, size, p)

    output('2.2',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 7
    p_l1 = 36
    fp_l1 = testFalse(f'criterian23 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, letter_criterion.criterian23, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian23 Y/vigenere/KEY_1_L_100: ', f'{path}/texts/Y/vigenere/KEY_1_L_100_N_', 10000, letter_criterion.criterian23, size_l1, p_l1)

    size = 7
    p = 4
    fp_l2 = testFalse(f'criterian23 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, bigram_criterion.criterian23, size, p)
    fn_l2 = testTrue(f'criterian23 Y/vigenere/KEY_1_L_100: ', f'{path}/texts/Y/vigenere/KEY_1_L_100_N_', 10000, bigram_criterion.criterian23, size, p)

    output('2.3',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = .004
    fp_l1 = testFalse(f'criterian40 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, letter_criterion.criterian40, p_l1)
    fn_l1 = testTrue(f'criterian40 Y/vigenere/KEY_1_L_100: ', f'{path}/texts/Y/vigenere/KEY_1_L_100_N_', 10000, letter_criterion.criterian40, p_l1)
    
    p = .002
    fp_l2 = testFalse(f'criterian40 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, bigram_criterion.criterian40, p)
    fn_l2 = testTrue(f'criterian40 Y/vigenere/KEY_1_L_100: ', f'{path}/texts/Y/vigenere/KEY_1_L_100_N_', 10000, bigram_criterion.criterian40, p)
    
    output('4.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 20
    p_l1 = 4
    fp_l1 = testFalse(f'criterian50 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, letter_criterion.criterian50, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian50 Y/vigenere/KEY_1_L_100: ', f'{path}/texts/Y/vigenere/KEY_1_L_100_N_', 10000, letter_criterion.criterian50, size_l1, p_l1)

    size = 20
    p = 19
    fp_l2 = testFalse(f'criterian50 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, bigram_criterion.criterian50, size, p)
    fn_l2 = testTrue(f'criterian50 Y/vigenere/KEY_1_L_100: ', f'{path}/texts/Y/vigenere/KEY_1_L_100_N_', 10000, bigram_criterion.criterian50, size, p)

    output('5.0',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = 60 
    fp_l1 = testFalseStructural('structural X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, letter_criterion.structuralCriterian, p_l1)
    fn_l1 = testTrueStructural('structural Y/vigenere/KEY_1_L_100: ', f'{path}/texts/Y/vigenere/KEY_1_L_100_N_', 10000, letter_criterion.structuralCriterian, p_l1)

    p = 59 
    fp_l2 = testFalseStructural('structural X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, bigram_criterion.structuralCriterian, p)
    fn_l2 = testTrueStructural('structural Y/vigenere/KEY_1_L_100: ', f'{path}/texts/Y/vigenere/KEY_1_L_100_N_', 10000, bigram_criterion.structuralCriterian, p)

    output('struct','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

def vigenere_L1000_K_1(letter_criterion,bigram_criterion):
    print("vigenere_L1000_K_1:")

    p_l1 = 4
    fp_l1 = testFalse(f'criterian20 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, letter_criterion.criterian20, p_l1)
    fn_l1 = testTrue(f'criterian20 Y/vigenere/KEY_1_L_1000: ', f'{path}/texts/Y/vigenere/KEY_1_L_1000_N_', 10000, letter_criterion.criterian20, p_l1)

    p = 4
    fp_l2 = testFalse(f'criterian20 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, bigram_criterion.criterian20, p)
    fn_l2 = testTrue(f'criterian20 Y/vigenere/KEY_1_L_1000: ', f'{path}/texts/Y/vigenere/KEY_1_L_1000_N_', 10000, bigram_criterion.criterian20, p)

    output('2.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 7
    p_l1 = 7
    fp_l1 = testFalse(f'criterian21 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, letter_criterion.criterian21, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian21 Y/vigenere/KEY_1_L_1000: ', f'{path}/texts/Y/vigenere/KEY_1_L_1000_N_', 10000, letter_criterion.criterian21, size_l1, p_l1)

    size = 7
    p = 7
    fp_l2 = testFalse(f'criterian21 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, bigram_criterion.criterian21, size, p)
    fn_l2 = testTrue(f'criterian21 Y/vigenere/KEY_1_L_1000: ', f'{path}/texts/Y/vigenere/KEY_1_L_1000_N_', 10000, bigram_criterion.criterian21, size, p)

    output('2.1',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 1
    p_l1 = 6
    fp_l1 = testFalse(f'criterian22 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, letter_criterion.criterian22, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian22 Y/vigenere/KEY_1_L_1000: ', f'{path}/texts/Y/vigenere/KEY_1_L_1000_N_', 10000, letter_criterion.criterian22, size_l1, p_l1)

    size = 1
    p = 6
    fp_l2 = testFalse(f'criterian22 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, bigram_criterion.criterian22, size, p)
    fn_l2 = testTrue(f'criterian22 Y/vigenere/KEY_1_L_1000: ', f'{path}/texts/Y/vigenere/KEY_1_L_1000_N_', 10000, bigram_criterion.criterian22, size, p)

    output('2.2',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 7
    p_l1 = 36
    fp_l1 = testFalse(f'criterian23 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, letter_criterion.criterian23, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian23 Y/vigenere/KEY_1_L_1000: ', f'{path}/texts/Y/vigenere/KEY_1_L_1000_N_', 10000, letter_criterion.criterian23, size_l1, p_l1)

    size = 7
    p = 36
    fp_l2 = testFalse(f'criterian23 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, bigram_criterion.criterian23, size, p)
    fn_l2 = testTrue(f'criterian23 Y/vigenere/KEY_1_L_1000: ', f'{path}/texts/Y/vigenere/KEY_1_L_1000_N_', 10000, bigram_criterion.criterian23, size, p)

    output('2.3',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = .006
    fp_l1 = testFalse(f'criterian40 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, letter_criterion.criterian40, p_l1)
    fn_l1 = testTrue(f'criterian40 Y/vigenere/KEY_1_L_1000: ', f'{path}/texts/Y/vigenere/KEY_1_L_1000_N_', 10000, letter_criterion.criterian40, p_l1)
    
    p = .002
    fp_l2 = testFalse(f'criterian40 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, bigram_criterion.criterian40, p)
    fn_l2 = testTrue(f'criterian40 Y/vigenere/KEY_1_L_1000: ', f'{path}/texts/Y/vigenere/KEY_1_L_1000_N_', 10000, bigram_criterion.criterian40, p)
    
    output('4.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 100
    p_l1 = 66
    fp_l1 = testFalse(f'criterian50 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, letter_criterion.criterian50, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian50 Y/vigenere/KEY_1_L_1000: ', f'{path}/texts/Y/vigenere/KEY_1_L_1000_N_', 10000, letter_criterion.criterian50, size_l1, p_l1)

    size = 100
    p = 99
    fp_l2 = testFalse(f'criterian50 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, bigram_criterion.criterian50, size, p)
    fn_l2 = testTrue(f'criterian50 Y/vigenere/KEY_1_L_1000: ', f'{path}/texts/Y/vigenere/KEY_1_L_1000_N_', 10000, bigram_criterion.criterian50, size, p)

    output('5.0',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = 47 #problem
    fp_l1 = testFalseStructural('structural X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, letter_criterion.structuralCriterian, p_l1)
    fn_l1 = testTrueStructural('structural Y/vigenere/KEY_1_L_1000: ', f'{path}/texts/Y/vigenere/KEY_1_L_1000_N_', 10000, letter_criterion.structuralCriterian, p_l1)

    p = 47 #problem
    fp_l2 = testFalseStructural('structural X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, bigram_criterion.structuralCriterian, p)
    fn_l2 = testTrueStructural('structural Y/vigenere/KEY_1_L_1000: ', f'{path}/texts/Y/vigenere/KEY_1_L_1000_N_', 10000, bigram_criterion.structuralCriterian, p)

    output('struct','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

def vigenere_L10000_K_1(letter_criterion,bigram_criterion):
    print("vigenere_L10000_K_1:")

    p_l1 = 4
    fp_l1 = testFalse(f'criterian20 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, letter_criterion.criterian20, p_l1)
    fn_l1 = testTrue(f'criterian20 Y/vigenere/KEY_1_L_10000: ', f'{path}/texts/Y/vigenere/KEY_1_L_10000_N_', 1000, letter_criterion.criterian20, p_l1)

    p = 4
    fp_l2 = testFalse(f'criterian20 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, bigram_criterion.criterian20, p)
    fn_l2 = testTrue(f'criterian20 Y/vigenere/KEY_1_L_10000: ', f'{path}/texts/Y/vigenere/KEY_1_L_10000_N_', 1000, bigram_criterion.criterian20, p)

    output('2.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 7
    p_l1 = 7
    fp_l1 = testFalse(f'criterian21 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, letter_criterion.criterian21, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian21 Y/vigenere/KEY_1_L_10000: ', f'{path}/texts/Y/vigenere/KEY_1_L_10000_N_', 1000, letter_criterion.criterian21, size_l1, p_l1)

    size = 7
    p = 6
    fp_l2 = testFalse(f'criterian21 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, bigram_criterion.criterian21, size, p)
    fn_l2 = testTrue(f'criterian21 Y/vigenere/KEY_1_L_10000: ', f'{path}/texts/Y/vigenere/KEY_1_L_10000_N_', 1000, bigram_criterion.criterian21, size, p)

    output('2.1',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 1
    p_l1 = 6
    fp_l1 = testFalse(f'criterian22 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, letter_criterion.criterian22, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian22 Y/vigenere/KEY_1_L_10000: ', f'{path}/texts/Y/vigenere/KEY_1_L_10000_N_', 1000, letter_criterion.criterian22, size_l1, p_l1)

    size = 1
    p = 20
    fp_l2 = testFalse(f'criterian22 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, bigram_criterion.criterian22, size, p)
    fn_l2 = testTrue(f'criterian22 Y/vigenere/KEY_1_L_10000: ', f'{path}/texts/Y/vigenere/KEY_1_L_10000_N_', 1000, bigram_criterion.criterian22, size, p)

    output('2.2',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 7
    p_l1 = 36
    fp_l1 = testFalse(f'criterian23 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, letter_criterion.criterian23, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian23 Y/vigenere/KEY_1_L_10000: ', f'{path}/texts/Y/vigenere/KEY_1_L_10000_N_', 1000, letter_criterion.criterian23, size_l1, p_l1)

    size = 7
    p = 150
    fp_l2 = testFalse(f'criterian23 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, bigram_criterion.criterian23, size, p)
    fn_l2 = testTrue(f'criterian23 Y/vigenere/KEY_1_L_10000: ', f'{path}/texts/Y/vigenere/KEY_1_L_10000_N_', 1000, bigram_criterion.criterian23, size, p)

    output('2.3',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = .006
    fp_l1 = testFalse(f'criterian40 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, letter_criterion.criterian40, p_l1)
    fn_l1 = testTrue(f'criterian40 Y/vigenere/KEY_1_L_10000: ', f'{path}/texts/Y/vigenere/KEY_1_L_10000_N_', 1000, letter_criterion.criterian40, p_l1)
    
    p = .006
    fp_l2 = testFalse(f'criterian40 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, bigram_criterion.criterian40, p)
    fn_l2 = testTrue(f'criterian40 Y/vigenere/KEY_1_L_10000: ', f'{path}/texts/Y/vigenere/KEY_1_L_10000_N_', 1000, bigram_criterion.criterian40, p)
    
    output('4.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 100
    p_l1 = 66
    fp_l1 = testFalse(f'criterian50 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, letter_criterion.criterian50, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian50 Y/vigenere/KEY_1_L_10000: ', f'{path}/texts/Y/vigenere/KEY_1_L_10000_N_', 1000, letter_criterion.criterian50, size_l1, p_l1)

    size = 100
    p = 66
    fp_l2 = testFalse(f'criterian50 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, bigram_criterion.criterian50, size, p)
    fn_l2 = testTrue(f'criterian50 Y/vigenere/KEY_1_L_10000: ', f'{path}/texts/Y/vigenere/KEY_1_L_10000_N_', 1000, bigram_criterion.criterian50, size, p)

    output('5.0',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = 47 #problem
    fp_l1 = testFalseStructural('structural X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, letter_criterion.structuralCriterian, p_l1)
    fn_l1 = testTrueStructural('structural Y/vigenere/KEY_1_L_10000: ', f'{path}/texts/Y/vigenere/KEY_1_L_10000_N_', 1000, letter_criterion.structuralCriterian, p_l1)
    
    p = 66 #problem
    fp_l2 = testFalseStructural('structural X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, bigram_criterion.structuralCriterian, p)
    fn_l2 = testTrueStructural('structural Y/vigenere/KEY_1_L_10000: ', f'{path}/texts/Y/vigenere/KEY_1_L_10000_N_', 1000, bigram_criterion.structuralCriterian, p)

    output('struct','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

def vigenere_L10_K_5(letter_criterion,bigram_criterion):
    print("vigenere_L10_K_5")

    p_l1 = 1
    fp_l1 = testFalse(f'criterian20 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, letter_criterion.criterian20, p_l1)
    fn_l1 = testTrue(f'criterian20 Y/vigenere/KEY_5_L_10: ', f'{path}/texts/Y/vigenere/KEY_5_L_10_N_', 10000, letter_criterion.criterian20, p_l1)

    p = 0
    fp_l2 = testFalse(f'criterian20 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, bigram_criterion.criterian20, p)
    fn_l2 = testTrue(f'criterian20 Y/vigenere/KEY_5_L_10: ', f'{path}/texts/Y/vigenere/KEY_5_L_10_N_', 10000, bigram_criterion.criterian20, p)

    output('2.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 7
    p_l1 = 3
    fp_l1 = testFalse(f'criterian21 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, letter_criterion.criterian21, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian21 Y/vigenere/KEY_5_L_10: ', f'{path}/texts/Y/vigenere/KEY_5_L_10_N_', 10000, letter_criterion.criterian21, size_l1, p_l1)

    size = 100
    p = 1
    fp_l2 = testFalse(f'criterian21 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, bigram_criterion.criterian21, size, p)
    fn_l2 = testTrue(f'criterian21 Y/vigenere/KEY_5_L_10: ', f'{path}/texts/Y/vigenere/KEY_5_L_10_N_', 10000, bigram_criterion.criterian21, size, p)

    output('2.1',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 1
    p_l1 = 1
    fp_l1 = testFalse(f'criterian22 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, letter_criterion.criterian22, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian22 Y/vigenere/KEY_5_L_10: ', f'{path}/texts/Y/vigenere/KEY_5_L_10_N_', 10000, letter_criterion.criterian22, size_l1, p_l1)

    size = 1
    p = 0
    fp_l2 = testFalse(f'criterian22 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, bigram_criterion.criterian22, size, p)
    fn_l2 = testTrue(f'criterian22 Y/vigenere/KEY_5_L_10: ', f'{path}/texts/Y/vigenere/KEY_5_L_10_N_', 10000, bigram_criterion.criterian22, size, p)

    output('2.2',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 7
    p_l1 = 4
    fp_l1 = testFalse(f'criterian23 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, letter_criterion.criterian23, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian23 Y/vigenere/KEY_5_L_10: ', f'{path}/texts/Y/vigenere/KEY_5_L_10_N_', 10000, letter_criterion.criterian23, size_l1, p_l1)

    size = 20
    p = 1
    fp_l2 = testFalse(f'criterian23 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, bigram_criterion.criterian23, size, p)
    fn_l2 = testTrue(f'criterian23 Y/vigenere/KEY_5_L_10: ', f'{path}/texts/Y/vigenere/KEY_5_L_10_N_', 10000, bigram_criterion.criterian23, size, p)

    output('2.3',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = .03
    fp_l1 = testFalse(f'criterian40 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, letter_criterion.criterian40, p_l1)
    fn_l1 = testTrue(f'criterian40 Y/vigenere/KEY_5_L_10: ', f'{path}/texts/Y/vigenere/KEY_5_L_10_N_', 10000, letter_criterion.criterian40, p_l1)

    p = .03
    fp_l2 = testFalse(f'criterian40 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, bigram_criterion.criterian40, p)
    fn_l2 = testTrue(f'criterian40 Y/vigenere/KEY_5_L_10: ', f'{path}/texts/Y/vigenere/KEY_5_L_10_N_', 10000, bigram_criterion.criterian40, p)
    
    output('4.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 20
    p_l1 = 16
    fp_l1 = testFalse(f'criterian50 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, letter_criterion.criterian50, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian50 Y/vigenere/KEY_5_L_10: ', f'{path}/texts/Y/vigenere/KEY_5_L_10_N_', 10000, letter_criterion.criterian50, size_l1, p_l1)

    size = 20
    p = 16
    fp_l2 = testFalse(f'criterian50 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, bigram_criterion.criterian50, size, p)
    fn_l2 = testTrue(f'criterian50 Y/vigenere/KEY_5_L_10: ', f'{path}/texts/Y/vigenere/KEY_5_L_10_N_', 10000, bigram_criterion.criterian50, size, p)

    output('5.0',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = 1015 #problem
    fp_l1 = testFalseStructural('structural X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, letter_criterion.structuralCriterian, p_l1)
    fn_l1 = testTrueStructural('structural Y/vigenere/KEY_5_L_10: ', f'{path}/texts/Y/vigenere/KEY_5_L_10_N_', 10000, letter_criterion.structuralCriterian, p_l1)

    p = 1015 #problem
    fp_l2 = testFalseStructural('structural X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, bigram_criterion.structuralCriterian, p)
    fn_l2 = testTrueStructural('structural Y/vigenere/KEY_5_L_10: ', f'{path}/texts/Y/vigenere/KEY_5_L_10_N_', 10000, bigram_criterion.structuralCriterian, p)

    output('struct','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

def vigenere_L100_K_5(letter_criterion,bigram_criterion):
    print("vigenere_L100_K_5")

    p_l1 = 12
    fp_l1 = testFalse(f'criterian20 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, letter_criterion.criterian20, p_l1)
    fn_l1 = testTrue(f'criterian20 Y/vigenere/KEY_5_L_100: ', f'{path}/texts/Y/vigenere/KEY_5_L_100_N_', 10000, letter_criterion.criterian20, p_l1)

    p = 1
    fp_l2 = testFalse(f'criterian20 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, bigram_criterion.criterian20, p)
    fn_l2 = testTrue(f'criterian20 Y/vigenere/KEY_5_L_100: ', f'{path}/texts/Y/vigenere/KEY_5_L_100_N_', 10000, bigram_criterion.criterian20, p)

    output('2.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 5
    p_l1 = 5
    fp_l1 = testFalse(f'criterian21 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, letter_criterion.criterian21, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian21 Y/vigenere/KEY_5_L_100: ', f'{path}/texts/Y/vigenere/KEY_5_L_100_N_', 10000, letter_criterion.criterian21, size_l1, p_l1)

    size = 15
    p = 5
    fp_l2 = testFalse(f'criterian21 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, bigram_criterion.criterian21, size, p)
    fn_l2 = testTrue(f'criterian21 Y/vigenere/KEY_5_L_100: ', f'{path}/texts/Y/vigenere/KEY_5_L_100_N_', 10000, bigram_criterion.criterian21, size, p)

    output('2.1',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 5
    p_l1 = 2
    fp_l1 = testFalse(f'criterian22 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, letter_criterion.criterian22, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian22 Y/vigenere/KEY_5_L_100: ', f'{path}/texts/Y/vigenere/KEY_5_L_100_N_', 10000, letter_criterion.criterian22, size_l1, p_l1)

    size = 5
    p = 0
    fp_l2 = testFalse(f'criterian22 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, bigram_criterion.criterian22, size, p)
    fn_l2 = testTrue(f'criterian22 Y/vigenere/KEY_5_L_100: ', f'{path}/texts/Y/vigenere/KEY_5_L_100_N_', 10000, bigram_criterion.criterian22, size, p)

    output('2.2',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 7
    p_l1 = 36
    fp_l1 = testFalse(f'criterian23 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, letter_criterion.criterian23, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian23 Y/vigenere/KEY_5_L_100: ', f'{path}/texts/Y/vigenere/KEY_5_L_100_N_', 10000, letter_criterion.criterian23, size_l1, p_l1)

    size = 7
    p = 1
    fp_l2 = testFalse(f'criterian23 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, bigram_criterion.criterian23, size, p)
    fn_l2 = testTrue(f'criterian23 Y/vigenere/KEY_5_L_100: ', f'{path}/texts/Y/vigenere/KEY_5_L_100_N_', 10000, bigram_criterion.criterian23, size, p)

    output('2.3',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = .01
    fp_l1 = testFalse(f'criterian40 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, letter_criterion.criterian40, p_l1)
    fn_l1 = testTrue(f'criterian40 Y/vigenere/KEY_5_L_100: ', f'{path}/texts/Y/vigenere/KEY_5_L_100_N_', 10000, letter_criterion.criterian40, p_l1)
    
    p = .005
    fp_l2 = testFalse(f'criterian40 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, bigram_criterion.criterian40, p)
    fn_l2 = testTrue(f'criterian40 Y/vigenere/KEY_5_L_100: ', f'{path}/texts/Y/vigenere/KEY_5_L_100_N_', 10000, bigram_criterion.criterian40, p)
    
    output('4.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 20
    p_l1 = 3
    fp_l1 = testFalse(f'criterian50 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, letter_criterion.criterian50, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian50 Y/vigenere/KEY_5_L_100: ', f'{path}/texts/Y/vigenere/KEY_5_L_100_N_', 10000, letter_criterion.criterian50, size_l1, p_l1)

    size = 20
    p = 19
    fp_l2 = testFalse(f'criterian50 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, bigram_criterion.criterian50, size, p)
    fn_l2 = testTrue(f'criterian50 Y/vigenere/KEY_5_L_100: ', f'{path}/texts/Y/vigenere/KEY_5_L_100_N_', 10000, bigram_criterion.criterian50, size, p)

    output('5.0',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = 60 #problem
    fp_l1 = testFalseStructural('structural X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, letter_criterion.structuralCriterian, p_l1)
    fn_l1 = testTrueStructural('structural Y/vigenere/KEY_5_L_100: ', f'{path}/texts/Y/vigenere/KEY_5_L_100_N_', 10000, letter_criterion.structuralCriterian, p_l1)

    p = 60 #problem
    fp_l2 = testFalseStructural('structural X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, bigram_criterion.structuralCriterian, p)
    fn_l2 = testTrueStructural('structural Y/vigenere/KEY_5_L_100: ', f'{path}/texts/Y/vigenere/KEY_5_L_100_N_', 10000, bigram_criterion.structuralCriterian, p)

    output('struct','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

def vigenere_L1000_K_5(letter_criterion,bigram_criterion):
    print("vigenere_L1000_K_5:")

    p_l1 = 4
    fp_l1 = testFalse(f'criterian20 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, letter_criterion.criterian20, p_l1)
    fn_l1 = testTrue(f'criterian20 Y/vigenere/KEY_5_L_1000: ', f'{path}/texts/Y/vigenere/KEY_5_L_1000_N_', 10000, letter_criterion.criterian20, p_l1)

    p = 4
    fp_l2 = testFalse(f'criterian20 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, bigram_criterion.criterian20, p)
    fn_l2 = testTrue(f'criterian20 Y/vigenere/KEY_5_L_1000: ', f'{path}/texts/Y/vigenere/KEY_5_L_1000_N_', 10000, bigram_criterion.criterian20, p)

    output('2.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 7
    p_l1 = 7
    fp_l1 = testFalse(f'criterian21 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, letter_criterion.criterian21, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian21 Y/vigenere/KEY_5_L_1000: ', f'{path}/texts/Y/vigenere/KEY_5_L_1000_N_', 10000, letter_criterion.criterian21, size_l1, p_l1)

    size = 7
    p = 7
    fp_l2 = testFalse(f'criterian21 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, bigram_criterion.criterian21, size, p)
    fn_l2 = testTrue(f'criterian21 Y/vigenere/KEY_5_L_1000: ', f'{path}/texts/Y/vigenere/KEY_5_L_1000_N_', 10000, bigram_criterion.criterian21, size, p)

    output('2.1',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 1
    p_l1 = 6
    fp_l1 = testFalse(f'criterian22 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, letter_criterion.criterian22, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian22 Y/vigenere/KEY_5_L_1000: ', f'{path}/texts/Y/vigenere/KEY_5_L_1000_N_', 10000, letter_criterion.criterian22, size_l1, p_l1)

    size = 1
    p = 6
    fp_l2 = testFalse(f'criterian22 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, bigram_criterion.criterian22, size, p)
    fn_l2 = testTrue(f'criterian22 Y/vigenere/KEY_5_L_1000: ', f'{path}/texts/Y/vigenere/KEY_5_L_1000_N_', 10000, bigram_criterion.criterian22, size, p)

    output('2.2',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 7
    p_l1 = 36
    fp_l1 = testFalse(f'criterian23 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, letter_criterion.criterian23, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian23 Y/vigenere/KEY_5_L_1000: ', f'{path}/texts/Y/vigenere/KEY_5_L_1000_N_', 10000, letter_criterion.criterian23, size_l1, p_l1)

    size = 7
    p = 36
    fp_l2 = testFalse(f'criterian23 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, bigram_criterion.criterian23, size, p)
    fn_l2 = testTrue(f'criterian23 Y/vigenere/KEY_5_L_1000: ', f'{path}/texts/Y/vigenere/KEY_5_L_1000_N_', 10000, bigram_criterion.criterian23, size, p)

    output('2.3',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = .02
    fp_l1 = testFalse(f'criterian40 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, letter_criterion.criterian40, p_l1)
    fn_l1 = testTrue(f'criterian40 Y/vigenere/KEY_5_L_1000: ', f'{path}/texts/Y/vigenere/KEY_5_L_1000_N_', 10000, letter_criterion.criterian40, p_l1)
    
    p = .002
    fp_l2 = testFalse(f'criterian40 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, bigram_criterion.criterian40, p)
    fn_l2 = testTrue(f'criterian40 Y/vigenere/KEY_5_L_1000: ', f'{path}/texts/Y/vigenere/KEY_5_L_1000_N_', 10000, bigram_criterion.criterian40, p)
    
    output('4.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 100
    p_l1 = 66
    fp_l1 = testFalse(f'criterian50 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, letter_criterion.criterian50, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian50 Y/vigenere/KEY_5_L_1000: ', f'{path}/texts/Y/vigenere/KEY_5_L_1000_N_', 10000, letter_criterion.criterian50, size_l1, p_l1)

    size = 100
    p = 66
    fp_l2 = testFalse(f'criterian50 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, bigram_criterion.criterian50, size, p)
    fn_l2 = testTrue(f'criterian50 Y/vigenere/KEY_5_L_1000: ', f'{path}/texts/Y/vigenere/KEY_5_L_1000_N_', 10000, bigram_criterion.criterian50, size, p)

    output('5.0',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = 46 
    fp_l1 = testFalseStructural('structural X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, letter_criterion.structuralCriterian, p_l1)
    fn_l1 = testTrueStructural('structural Y/vigenere/KEY_5_L_1000: ', f'{path}/texts/Y/vigenere/KEY_5_L_1000_N_', 10000, letter_criterion.structuralCriterian, p_l1)

    p = 46 
    fp_l2 = testFalseStructural('structural X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, bigram_criterion.structuralCriterian, p)
    fn_l2 = testTrueStructural('structural Y/vigenere/KEY_5_L_1000: ', f'{path}/texts/Y/vigenere/KEY_5_L_1000_N_', 10000, bigram_criterion.structuralCriterian, p)

    output('struct','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)


def vigenere_L10000_K_5(letter_criterion,bigram_criterion):
    print("igenere_L10000_K_5:")

    p_l1 = 4
    fp_l1 = testFalse(f'criterian20 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, letter_criterion.criterian20, p_l1)
    fn_l1 = testTrue(f'criterian20 Y/vigenere/KEY_5_L_10000: ', f'{path}/texts/Y/vigenere/KEY_5_L_10000_N_', 1000, letter_criterion.criterian20, p_l1)

    p = 4
    fp_l2 = testFalse(f'criterian20 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, bigram_criterion.criterian20, p)
    fn_l2 = testTrue(f'criterian20 Y/vigenere/KEY_5_L_10000: ', f'{path}/texts/Y/vigenere/KEY_5_L_10000_N_', 1000, bigram_criterion.criterian20, p)

    output('2.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 7
    p_l1 = 7
    fp_l1 = testFalse(f'criterian21 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, letter_criterion.criterian21, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian21 Y/vigenere/KEY_5_L_10000: ', f'{path}/texts/Y/vigenere/KEY_5_L_10000_N_', 1000, letter_criterion.criterian21, size_l1, p_l1)

    size = 7
    p = 7
    fp_l2 = testFalse(f'criterian21 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, bigram_criterion.criterian21, size, p)
    fn_l2 = testTrue(f'criterian21 Y/vigenere/KEY_5_L_10000: ', f'{path}/texts/Y/vigenere/KEY_5_L_10000_N_', 1000, bigram_criterion.criterian21, size, p)

    output('2.1',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 1
    p_l1 = 6
    fp_l1 = testFalse(f'criterian22 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, letter_criterion.criterian22, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian22 Y/vigenere/KEY_5_L_10000: ', f'{path}/texts/Y/vigenere/KEY_5_L_10000_N_', 1000, letter_criterion.criterian22, size_l1, p_l1)

    size = 1
    p = 6
    fp_l2 = testFalse(f'criterian22 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, bigram_criterion.criterian22, size, p)
    fn_l2 = testTrue(f'criterian22 Y/vigenere/KEY_5_L_10000: ', f'{path}/texts/Y/vigenere/KEY_5_L_10000_N_', 1000, bigram_criterion.criterian22, size, p)

    output('2.2',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 7
    p_l1 = 36
    fp_l1 = testFalse(f'criterian23 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, letter_criterion.criterian23, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian23 Y/vigenere/KEY_5_L_10000: ', f'{path}/texts/Y/vigenere/KEY_5_L_10000_N_', 1000, letter_criterion.criterian23, size_l1, p_l1)

    size = 7
    p = 100
    fp_l2 = testFalse(f'criterian23 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, bigram_criterion.criterian23, size, p)
    fn_l2 = testTrue(f'criterian23 Y/vigenere/KEY_5_L_10000: ', f'{path}/texts/Y/vigenere/KEY_5_L_10000_N_', 1000, bigram_criterion.criterian23, size, p)

    output('2.3',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = .01
    fp_l1 = testFalse(f'criterian40 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, letter_criterion.criterian40, p_l1)
    fn_l1 = testTrue(f'criterian40 Y/vigenere/KEY_5_L_10000: ', f'{path}/texts/Y/vigenere/KEY_5_L_10000_N_', 1000, letter_criterion.criterian40, p_l1)
    
    p = .01
    fp_l2 = testFalse(f'criterian40 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, bigram_criterion.criterian40, p)
    fn_l2 = testTrue(f'criterian40 Y/vigenere/KEY_5_L_10000: ', f'{path}/texts/Y/vigenere/KEY_5_L_10000_N_', 1000, bigram_criterion.criterian40, p)
    
    output('4.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 100
    p_l1 = 66
    fp_l1 = testFalse(f'criterian50 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, letter_criterion.criterian50, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian50 Y/vigenere/KEY_5_L_10000: ', f'{path}/texts/Y/vigenere/KEY_5_L_10000_N_', 1000, letter_criterion.criterian50, size_l1, p_l1)

    size = 100
    p = 66
    fp_l2 = testFalse(f'criterian50 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, bigram_criterion.criterian50, size, p)
    fn_l2 = testTrue(f'criterian50 Y/vigenere/KEY_5_L_10000: ', f'{path}/texts/Y/vigenere/KEY_5_L_10000_N_', 1000, bigram_criterion.criterian50, size, p)

    output('5.0',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = 47 #problem
    fp_l1 = testFalseStructural('structural X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, letter_criterion.structuralCriterian, p_l1)
    fn_l1 = testTrueStructural('structural Y/vigenere/KEY_5_L_10000: ', f'{path}/texts/Y/vigenere/KEY_5_L_10000_N_', 1000, letter_criterion.structuralCriterian, p_l1)

    p = 60 #problem
    fp_l2 = testFalseStructural('structural X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, bigram_criterion.structuralCriterian, p)
    fn_l2 = testTrueStructural('structural Y/vigenere/KEY_5_L_10000: ', f'{path}/texts/Y/vigenere/KEY_5_L_10000_N_', 1000, bigram_criterion.structuralCriterian, p)

    output('struct','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

def vigenere_L10_K_10(letter_criterion,bigram_criterion):
    print("vigenere_L10_K_10:")
    p_l1 = 1
    fp_l1 = testFalse(f'criterian20 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, letter_criterion.criterian20, p_l1)
    fn_l1 = testTrue(f'criterian20 Y/vigenere/KEY_10_L_10: ', f'{path}/texts/Y/vigenere/KEY_10_L_10_N_', 10000, letter_criterion.criterian20, p_l1)

    p = 1
    fp_l2 = testFalse(f'criterian20 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, bigram_criterion.criterian20, p)
    fn_l2 = testTrue(f'criterian20 Y/vigenere/KEY_10_L_10: ', f'{path}/texts/Y/vigenere/KEY_10_L_10_N_', 10000, bigram_criterion.criterian20, p)

    output('2.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 7
    p_l1 = 3
    fp_l1 = testFalse(f'criterian21 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, letter_criterion.criterian21, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian21 Y/vigenere/KEY_10_L_10: ', f'{path}/texts/Y/vigenere/KEY_10_L_10_N_', 10000, letter_criterion.criterian21, size_l1, p_l1)

    size = 100
    p = 2
    fp_l2 = testFalse(f'criterian21 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, bigram_criterion.criterian21, size, p)
    fn_l2 = testTrue(f'criterian21 Y/vigenere/KEY_10_L_10: ', f'{path}/texts/Y/vigenere/KEY_10_L_10_N_', 10000, bigram_criterion.criterian21, size, p)

    output('2.1',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 1
    p_l1 = 1
    fp_l1 = testFalse(f'criterian22 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, letter_criterion.criterian22, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian22 Y/vigenere/KEY_10_L_10: ', f'{path}/texts/Y/vigenere/KEY_10_L_10_N_', 10000, letter_criterion.criterian22, size_l1, p_l1)

    size = 1
    p = 0
    fp_l2 = testFalse(f'criterian22 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, bigram_criterion.criterian22, size, p)
    fn_l2 = testTrue(f'criterian22 Y/vigenere/KEY_10_L_10: ', f'{path}/texts/Y/vigenere/KEY_10_L_10_N_', 10000, bigram_criterion.criterian22, size, p)

    output('2.2',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 7
    p_l1 = 4
    fp_l1 = testFalse(f'criterian23 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, letter_criterion.criterian23, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian23 Y/vigenere/KEY_10_L_10: ', f'{path}/texts/Y/vigenere/KEY_10_L_10_N_', 10000, letter_criterion.criterian23, size_l1, p_l1)

    size = 70
    p = 2
    fp_l2 = testFalse(f'criterian23 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, bigram_criterion.criterian23, size, p)
    fn_l2 = testTrue(f'criterian23 Y/vigenere/KEY_10_L_10: ', f'{path}/texts/Y/vigenere/KEY_10_L_10_N_', 10000, bigram_criterion.criterian23, size, p)

    output('2.3',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = .03
    fp_l1 = testFalse(f'criterian40 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, letter_criterion.criterian40, p_l1)
    fn_l1 = testTrue(f'criterian40 Y/vigenere/KEY_10_L_10: ', f'{path}/texts/Y/vigenere/KEY_10_L_10_N_', 10000, letter_criterion.criterian40, p_l1)
    
    p = .005
    fp_l2 = testFalse(f'criterian40 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, bigram_criterion.criterian40, p)
    fn_l2 = testTrue(f'criterian40 Y/vigenere/KEY_10_L_10: ', f'{path}/texts/Y/vigenere/KEY_10_L_10_N_', 10000, bigram_criterion.criterian40, p)
    
    output('4.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 20
    p_l1 = 16
    fp_l1 = testFalse(f'criterian50 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, letter_criterion.criterian50, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian50 Y/vigenere/KEY_10_L_10: ', f'{path}/texts/Y/vigenere/KEY_10_L_10_N_', 10000, letter_criterion.criterian50, size_l1, p_l1)

    size = 20
    p = 19
    fp_l2 = testFalse(f'criterian50 X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, bigram_criterion.criterian50, size, p)
    fn_l2 = testTrue(f'criterian50 Y/vigenere/KEY_10_L_10: ', f'{path}/texts/Y/vigenere/KEY_10_L_10_N_', 10000, bigram_criterion.criterian50, size, p)

    output('5.0',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = 1015 #problem
    fp_l1 = testFalseStructural('structural X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, letter_criterion.structuralCriterian, p_l1)
    fn_l1 = testTrueStructural('structural Y/vigenere/KEY_10_L_10: ', f'{path}/texts/Y/vigenere/KEY_10_L_10_N_', 10000, letter_criterion.structuralCriterian, p_l1)

    p = 1015 #problem
    fp_l2 = testFalseStructural('structural X/L_10: ', f'{path}/texts/X/L_10_N_', 10000, bigram_criterion.structuralCriterian, p)
    fn_l2 = testTrueStructural('structural Y/vigenere/KEY_10_L_10: ', f'{path}/texts/Y/vigenere/KEY_10_L_10_N_', 10000, bigram_criterion.structuralCriterian, p)

    output('struct','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)


def vigenere_L100_K_10(letter_criterion,bigram_criterion):
    print("vigenere_L100_K_10:")
    p_l1 = 10
    fp_l1 = testFalse(f'criterian20 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, letter_criterion.criterian20, p_l1)
    fn_l1 = testTrue(f'criterian20 Y/vigenere/KEY_10_L_100: ', f'{path}/texts/Y/vigenere/KEY_10_L_100_N_', 10000, letter_criterion.criterian20, p_l1)

    p = 1
    fp_l2 = testFalse(f'criterian20 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, bigram_criterion.criterian20, p)
    fn_l2 = testTrue(f'criterian20 Y/vigenere/KEY_10_L_100: ', f'{path}/texts/Y/vigenere/KEY_10_L_100_N_', 10000, bigram_criterion.criterian20, p)

    output('2.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 7
    p_l1 = 7
    fp_l1 = testFalse(f'criterian21 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, letter_criterion.criterian21, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian21 Y/vigenere/KEY_10_L_100: ', f'{path}/texts/Y/vigenere/KEY_10_L_100_N_', 10000, letter_criterion.criterian21, size_l1, p_l1)

    size = 7
    p = 1
    fp_l2 = testFalse(f'criterian21 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, bigram_criterion.criterian21, size, p)
    fn_l2 = testTrue(f'criterian21 Y/vigenere/KEY_10_L_100: ', f'{path}/texts/Y/vigenere/KEY_10_L_100_N_', 10000, bigram_criterion.criterian21, size, p)

    output('2.1',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 1
    p_l1 = 6
    fp_l1 = testFalse(f'criterian22 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, letter_criterion.criterian22, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian22 Y/vigenere/KEY_10_L_100: ', f'{path}/texts/Y/vigenere/KEY_10_L_100_N_', 10000, letter_criterion.criterian22, size_l1, p_l1)

    size = 1
    p = 1
    fp_l2 = testFalse(f'criterian22 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, bigram_criterion.criterian22, size, p)
    fn_l2 = testTrue(f'criterian22 Y/vigenere/KEY_10_L_100: ', f'{path}/texts/Y/vigenere/KEY_10_L_100_N_', 10000, bigram_criterion.criterian22, size, p)

    output('2.2',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 7
    p_l1 = 36
    fp_l1 = testFalse(f'criterian23 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, letter_criterion.criterian23, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian23 Y/vigenere/KEY_10_L_100: ', f'{path}/texts/Y/vigenere/KEY_10_L_100_N_', 10000, letter_criterion.criterian23, size_l1, p_l1)

    size = 7
    p = 1
    fp_l2 = testFalse(f'criterian23 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, bigram_criterion.criterian23, size, p)
    fn_l2 = testTrue(f'criterian23 Y/vigenere/KEY_10_L_100: ', f'{path}/texts/Y/vigenere/KEY_10_L_100_N_', 10000, bigram_criterion.criterian23, size, p)

    output('2.3',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = .01
    fp_l1 = testFalse(f'criterian40 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, letter_criterion.criterian40, p_l1)
    fn_l1 = testTrue(f'criterian40 Y/vigenere/KEY_10_L_100: ', f'{path}/texts/Y/vigenere/KEY_10_L_100_N_', 10000, letter_criterion.criterian40, p_l1)
    
    p = .003
    fp_l2 = testFalse(f'criterian40 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, bigram_criterion.criterian40, p)
    fn_l2 = testTrue(f'criterian40 Y/vigenere/KEY_10_L_100: ', f'{path}/texts/Y/vigenere/KEY_10_L_100_N_', 10000, bigram_criterion.criterian40, p)
    
    output('4.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 20
    p_l1 = 3
    fp_l1 = testFalse(f'criterian50 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, letter_criterion.criterian50, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian50 Y/vigenere/KEY_10_L_100: ', f'{path}/texts/Y/vigenere/KEY_10_L_100_N_', 10000, letter_criterion.criterian50, size_l1, p_l1)

    size = 20
    p = 19
    fp_l2 = testFalse(f'criterian50 X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, bigram_criterion.criterian50, size, p)
    fn_l2 = testTrue(f'criterian50 Y/vigenere/KEY_10_L_100: ', f'{path}/texts/Y/vigenere/KEY_10_L_100_N_', 10000, bigram_criterion.criterian50, size, p)

    output('5.0',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = 59
    fp_l1 = testFalseStructural('structural X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, letter_criterion.structuralCriterian, p_l1)
    fn_l1 = testTrueStructural('structural Y/vigenere/KEY_10_L_100: ', f'{path}/texts/Y/vigenere/KEY_10_L_100_N_', 10000, letter_criterion.structuralCriterian, p_l1)

    p = 60
    fp_l2 = testFalseStructural('structural X/L_100: ', f'{path}/texts/X/L_100_N_', 10000, bigram_criterion.structuralCriterian, p)
    fn_l2 = testTrueStructural('structural Y/vigenere/KEY_10_L_100: ', f'{path}/texts/Y/vigenere/KEY_10_L_100_N_', 10000, bigram_criterion.structuralCriterian, p)

    output('struct','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

def vigenere_L1000_K_10(letter_criterion,bigram_criterion):
    print("vigenere_L1000_K_10:")
    p_l1 = 4
    fp_l1 = testFalse(f'criterian20 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, letter_criterion.criterian20, p_l1)
    fn_l1 = testTrue(f'criterian20 Y/vigenere/KEY_10_L_1000: ', f'{path}/texts/Y/vigenere/KEY_10_L_1000_N_', 10000, letter_criterion.criterian20, p_l1)

    p = 4
    fp_l2 = testFalse(f'criterian20 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, bigram_criterion.criterian20, p)
    fn_l2 = testTrue(f'criterian20 Y/vigenere/KEY_10_L_1000: ', f'{path}/texts/Y/vigenere/KEY_10_L_1000_N_', 10000, bigram_criterion.criterian20, p)

    output('2.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 7
    p_l1 = 7
    fp_l1 = testFalse(f'criterian21 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, letter_criterion.criterian21, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian21 Y/vigenere/KEY_10_L_1000: ', f'{path}/texts/Y/vigenere/KEY_10_L_1000_N_', 10000, letter_criterion.criterian21, size_l1, p_l1)

    size = 7
    p = 7
    fp_l2 = testFalse(f'criterian21 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, bigram_criterion.criterian21, size, p)
    fn_l2 = testTrue(f'criterian21 Y/vigenere/KEY_10_L_1000: ', f'{path}/texts/Y/vigenere/KEY_10_L_1000_N_', 10000, bigram_criterion.criterian21, size, p)

    output('2.1',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 1
    p_l1 = 6
    fp_l1 = testFalse(f'criterian22 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, letter_criterion.criterian22, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian22 Y/vigenere/KEY_10_L_1000: ', f'{path}/texts/Y/vigenere/KEY_10_L_1000_N_', 10000, letter_criterion.criterian22, size_l1, p_l1)

    size = 1
    p = 6
    fp_l2 = testFalse(f'criterian22 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, bigram_criterion.criterian22, size, p)
    fn_l2 = testTrue(f'criterian22 Y/vigenere/KEY_10_L_1000: ', f'{path}/texts/Y/vigenere/KEY_10_L_1000_N_', 10000, bigram_criterion.criterian22, size, p)

    output('2.2',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)


    size_l1 = 7
    p_l1 = 36
    fp_l1 = testFalse(f'criterian23 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, letter_criterion.criterian23, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian23 Y/vigenere/KEY_10_L_1000: ', f'{path}/texts/Y/vigenere/KEY_10_L_1000_N_', 10000, letter_criterion.criterian23, size_l1, p_l1)

    size = 7
    p = 36
    fp_l2 = testFalse(f'criterian23 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, bigram_criterion.criterian23, size, p)
    fn_l2 = testTrue(f'criterian23 Y/vigenere/KEY_10_L_1000: ', f'{path}/texts/Y/vigenere/KEY_10_L_1000_N_', 10000, bigram_criterion.criterian23, size, p)

    output('2.3',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = .01
    fp_l1 = testFalse(f'criterian40 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, letter_criterion.criterian40, p_l1)
    fn_l1 = testTrue(f'criterian40 Y/vigenere/KEY_10_L_1000: ', f'{path}/texts/Y/vigenere/KEY_10_L_1000_N_', 10000, letter_criterion.criterian40, p_l1)
    
    p = .002
    fp_l2 = testFalse(f'criterian40 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, bigram_criterion.criterian40, p)
    fn_l2 = testTrue(f'criterian40 Y/vigenere/KEY_10_L_1000: ', f'{path}/texts/Y/vigenere/KEY_10_L_1000_N_', 10000, bigram_criterion.criterian40, p)
    
    output('4.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 100
    p_l1 = 66
    fp_l1 = testFalse(f'criterian50 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, letter_criterion.criterian50, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian50 Y/vigenere/KEY_10_L_1000: ', f'{path}/texts/Y/vigenere/KEY_10_L_1000_N_', 10000, letter_criterion.criterian50, size_l1, p_l1)

    size = 100
    p = 66
    fp_l2 = testFalse(f'criterian50 X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, bigram_criterion.criterian50, size, p)
    fn_l2 = testTrue(f'criterian50 Y/vigenere/KEY_10_L_1000: ', f'{path}/texts/Y/vigenere/KEY_10_L_1000_N_', 10000, bigram_criterion.criterian50, size, p)

    output('5.0',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = 47 #problem
    fp_l1 = testFalseStructural('structural X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, letter_criterion.structuralCriterian, p_l1)
    fn_l1 = testTrueStructural('structural Y/vigenere/KEY_10_L_1000: ', f'{path}/texts/Y/vigenere/KEY_10_L_1000_N_', 10000, letter_criterion.structuralCriterian, p_l1)
    
    p = 47 #problem
    fp_l2 = testFalseStructural('structural X/L_1000: ', f'{path}/texts/X/L_1000_N_', 10000, bigram_criterion.structuralCriterian, p)
    fn_l2 = testTrueStructural('structural Y/vigenere/KEY_10_L_1000: ', f'{path}/texts/Y/vigenere/KEY_10_L_1000_N_', 10000, bigram_criterion.structuralCriterian, p)

    output('struct','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

def vigenere_L10000_K_10(letter_criterion,bigram_criterion):
    print("vigenere_L10000_K_10:")
    p_l1 = 4
    fp_l1 = testFalse(f'criterian20 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, letter_criterion.criterian20, p_l1)
    fn_l1 = testTrue(f'criterian20 Y/vigenere/KEY_10_L_10000: ', f'{path}/texts/Y/vigenere/KEY_10_L_10000_N_', 1000, letter_criterion.criterian20, p_l1)

    p = 3
    fp_l2 = testFalse(f'criterian20 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, bigram_criterion.criterian20, p)
    fn_l2 = testTrue(f'criterian20 Y/vigenere/KEY_10_L_10000: ', f'{path}/texts/Y/vigenere/KEY_10_L_10000_N_', 1000, bigram_criterion.criterian20, p)

    output('2.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 7
    p_l1 = 7
    fp_l1 = testFalse(f'criterian21 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, letter_criterion.criterian21, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian21 Y/vigenere/KEY_10_L_10000: ', f'{path}/texts/Y/vigenere/KEY_10_L_10000_N_', 1000, letter_criterion.criterian21, size_l1, p_l1)

    size = 7
    p = 7
    fp_l2 = testFalse(f'criterian21 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, bigram_criterion.criterian21, size, p)
    fn_l2 = testTrue(f'criterian21 Y/vigenere/KEY_10_L_10000: ', f'{path}/texts/Y/vigenere/KEY_10_L_10000_N_', 1000, bigram_criterion.criterian21, size, p)

    output('2.1',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 1
    p_l1 = 6
    fp_l1 = testFalse(f'criterian22 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, letter_criterion.criterian22, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian22 Y/vigenere/KEY_10_L_10000: ', f'{path}/texts/Y/vigenere/KEY_10_L_10000_N_', 1000, letter_criterion.criterian22, size_l1, p_l1)

    size = 1
    p = 6
    fp_l2 = testFalse(f'criterian22 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, bigram_criterion.criterian22, size, p)
    fn_l2 = testTrue(f'criterian22 Y/vigenere/KEY_10_L_10000: ', f'{path}/texts/Y/vigenere/KEY_10_L_10000_N_', 1000, bigram_criterion.criterian22, size, p)

    output('2.2',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 7
    p_l1 = 36
    fp_l1 = testFalse(f'criterian23 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, letter_criterion.criterian23, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian23 Y/vigenere/KEY_10_L_10000: ', f'{path}/texts/Y/vigenere/KEY_10_L_10000_N_', 1000, letter_criterion.criterian23, size_l1, p_l1)

    size = 7
    p = 100
    fp_l2 = testFalse(f'criterian23 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, bigram_criterion.criterian23, size, p)
    fn_l2 = testTrue(f'criterian23 Y/vigenere/KEY_10_L_10000: ', f'{path}/texts/Y/vigenere/KEY_10_L_10000_N_', 1000, bigram_criterion.criterian23, size, p)

    output('2.3',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = .005 #problem
    fp_l1 = testFalse(f'criterian40 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, letter_criterion.criterian40, p_l1)
    fn_l1 = testTrue(f'criterian40 Y/vigenere/KEY_10_L_10000: ', f'{path}/texts/Y/vigenere/KEY_10_L_10000_N_', 1000, letter_criterion.criterian40, p_l1)
    
    p = .002
    fp_l2 = testFalse(f'criterian40 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, bigram_criterion.criterian40, p)
    fn_l2 = testTrue(f'criterian40 Y/vigenere/KEY_10_L_10000: ', f'{path}/texts/Y/vigenere/KEY_10_L_10000_N_', 1000, bigram_criterion.criterian40, p)
    
    output('4.0','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

    size_l1 = 100
    p_l1 = 66
    fp_l1 = testFalse(f'criterian50 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, letter_criterion.criterian50, size_l1, p_l1)
    fn_l1 = testTrue(f'criterian50 Y/vigenere/KEY_10_L_10000: ', f'{path}/texts/Y/vigenere/KEY_10_L_10000_N_', 1000, letter_criterion.criterian50, size_l1, p_l1)

    size = 100
    p = 66
    fp_l2 = testFalse(f'criterian50 X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, bigram_criterion.criterian50, size, p)
    fn_l2 = testTrue(f'criterian50 Y/vigenere/KEY_10_L_10000: ', f'{path}/texts/Y/vigenere/KEY_10_L_10000_N_', 1000, bigram_criterion.criterian50, size, p)

    output('5.0',size_l1,p_l1,size,p,fp_l1,fn_l1,fp_l2,fn_l2)

    p_l1 = 47 
    fp_l1 = testFalseStructural('structural X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, letter_criterion.structuralCriterian, p_l1)
    fn_l1 = testTrueStructural('structural Y/vigenere/KEY_10_L_10000: ', f'{path}/texts/Y/vigenere/KEY_10_L_10000_N_', 1000, letter_criterion.structuralCriterian, p_l1)
    
    p = 60
    fp_l2 = testFalseStructural('structural X/L_10000: ', f'{path}/texts/X/L_10000_N_', 1000, bigram_criterion.structuralCriterian, p)
    fn_l2 = testTrueStructural('structural Y/vigenere/KEY_10_L_10000: ', f'{path}/texts/Y/vigenere/KEY_10_L_10000_N_', 1000, bigram_criterion.structuralCriterian, p)

    output('struct','',p_l1,'',p,fp_l1,fn_l1,fp_l2,fn_l2)

def main_test():
    letters_frequency = json.loads(read(f'{path}/result/letter_frequency.json'))
    letter_criterion = Criterion(letters_frequency)
    bigrams_frequency =  json.loads(read(f'{path}/result/bigrams_frequency.json'))
    bigram_criterion = Criterion(bigrams_frequency)
    
    affine_L10(letter_criterion,bigram_criterion)
    affine_L100(letter_criterion,bigram_criterion)
    affine_L1000(letter_criterion,bigram_criterion)
    affine_L10000(letter_criterion,bigram_criterion)
    recursive_L10(letter_criterion,bigram_criterion)
    recursive_L100(letter_criterion,bigram_criterion)
    recursive_L1000(letter_criterion,bigram_criterion)
    recursive_L10000(letter_criterion,bigram_criterion)
    uniform_L10(letter_criterion,bigram_criterion)
    uniform_L100(letter_criterion,bigram_criterion)
    uniform_L1000(letter_criterion,bigram_criterion)
    uniform_L10000(letter_criterion,bigram_criterion)
    vigenere_L10_K1(letter_criterion,bigram_criterion)
    vigenere_L100_K_1(letter_criterion,bigram_criterion)
    vigenere_L1000_K_1(letter_criterion,bigram_criterion)
    vigenere_L10000_K_1(letter_criterion,bigram_criterion)
    vigenere_L10_K_5(letter_criterion,bigram_criterion)
    vigenere_L100_K_5(letter_criterion,bigram_criterion)
    vigenere_L1000_K_5(letter_criterion,bigram_criterion)
    vigenere_L10000_K_5(letter_criterion,bigram_criterion)
    vigenere_L10_K_10(letter_criterion,bigram_criterion)
    vigenere_L100_K_10(letter_criterion,bigram_criterion)
    vigenere_L1000_K_10(letter_criterion,bigram_criterion)
    vigenere_L10000_K_10(letter_criterion,bigram_criterion)





if __name__ == '__main__':
    main_test()