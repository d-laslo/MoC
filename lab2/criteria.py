import os
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
        if len(text_n_grams & allowed_n_grams) < threshold:
            return False
        return True

    def criterian22(self, text: str, set_size: int, threshold: int) -> bool: # 10: <1, 1>, 100: <1, 1>, 1000: <5, 4>, 10000: <30, 40>
        text_n_grams = self.__split_into_n_grams(text, self.__n_grams_len)
        allowed_n_grams = set(self.__n_grams[:set_size])

        frequencies = sorted([text_n_grams.count(i) for i in allowed_n_grams])
        if frequencies[0] >= threshold:
            return True
        return False

    def criterian23(self, text: str, set_size: int, thresholds: list[int]) -> bool: # 10: <30, 1>, 100: <7, 4>, 1000: <20, 150>, 10000: <20, 1700>
        text_n_grams = self.__split_into_n_grams(text, self.__n_grams_len)
        allowed_n_grams = set(self.__n_grams[:set_size])

        frequencies = sorted([text_n_grams.count(i) for i in allowed_n_grams])
        if sum(frequencies) >= thresholds:
            return True
        return False

    def criterian40(self, text: str, threshold: int) -> bool: #10: .03, 100: .003, 1000: .001, 10000: .00035
        I = self.__compliance_index(n_gram_frequency(text, self.__n_grams_len))

        if abs(I - self.__compliance_index_language) > threshold:
            return False
        return True

    def criterian50(self, text: str, set_size: int, threshold: int) -> bool: # 10: <500, 497>, 100: <100, 99>, 1000: <50, 49>, 10000: <50, 47>
        allowed_n_grams = set(self.__n_grams[-set_size:])
        frequency = n_gram_frequency(text, self.__n_grams_len)

        count = len(set(frequency.keys()) & allowed_n_grams)
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
        if statinfo > threshold:
            return True
        return False


def main_test():
    letters_frequency = json.loads(read(f'{path}/result/letter_frequency.json'))
    criterion_letters = Criterion(letters_frequency);
    
    #criterian20

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian20(f'{path}/texts/X/L_10_N_{n}', 1))
    print(f'criterian20 X/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian20(f'{path}/texts/X/L_100_N_{n}', 1))
    print(f'criterian20 X/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian20(f'{path}/texts/X/L_1000_N_{n}', 30))
    print(f'criterian20 X/L_1000: {res.count(True)}')

    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.criterian20(f'{path}/texts/X/L_10000_N_{n}', 210))
    print(f'criterian20 X/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian20(f'{path}/texts/Y/affine/L_10_N_{n}.log', 1))
    print(f'criterian20 Y/affine/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian20(f'{path}/texts/Y/affine/L_100_N_{n}.log', 1))
    print(f'criterian20 Y/affine/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian20(f'{path}/texts/Y/affine/L_1000_N_{n}.log', 30))
    print(f'criterian20 Y/affine/L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.criterian20(f'{path}/texts/Y/affine/L_10000_N_{n}.log', 210))
    print(f'criterian20 Y/affine/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian20(f'{path}/texts/Y/recursive/L_10_N_{n}.log', 1))
    print(f'criterian20 Y/recursive/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian20(f'{path}/texts/Y/recursive/L_100_N_{n}.log', 1))
    print(f'criterian20 Y/recursive/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian20(f'{path}/texts/Y/recursive/L_1000_N_{n}.log', 30))
    print(f'criterian20 Y/recursive/L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.criterian20(f'{path}/texts/Y/recursive/L_10000_N_{n}.log', 210))
    print(f'criterian20 Y/recursive/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian20(f'{path}/texts/Y/uniform/L_10_N_{n}.log', 1))
    print(f'criterian20 Y/uniform/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian20(f'{path}/texts/Y/uniform/L_100_N_{n}.log', 1))
    print(f'criterian20 Y/uniform/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian20(f'{path}/texts/Y/uniform/L_1000_N_{n}.log', 30))
    print(f'criterian20 Y/uniform/L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.criterian20(f'{path}/texts/Y/uniform/L_10000_N_{n}.log', 210))
    print(f'criterian20 Y/uniform/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian20(f'{path}/texts/Y/vigenere/KEY_1_L_10_N_{n}.log', 1))
    print(f'criterian20 Y/vigenere/KEY_1_L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian20(f'{path}/texts/Y/vigenere/KEY_1_L_100_N_{n}.log', 1))
    print(f'criterian20 Y/vigenere/KEY_1_L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian20(f'{path}/texts/Y/vigenere/KEY_1_L_1000_N_{n}.log', 30))
    print(f'criterian20 Y/vigenere/KEY_1_L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.criterian20(f'{path}/texts/Y/vigenere/KEY_1_L_10000_N_{n}.log', 210))
    print(f'criterian20 Y/vigenere/KEY_1_L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian20(f'{path}/texts/Y/vigenere/KEY_5_L_10_N_{n}.log', 1))
    print(f'criterian20 Y/vigenere/KEY_5_L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian20(f'{path}/texts/Y/vigenere/KEY_5_L_100_N_{n}.log', 1))
    print(f'criterian20 Y/vigenere/KEY_5_L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian20(f'{path}/texts/Y/vigenere/KEY_5_L_1000_N_{n}.log', 30))
    print(f'criterian20 Y/vigenere/KEY_5_L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.criterian20(f'{path}/texts/Y/vigenere/KEY_5_L_10000_N_{n}.log', 210))
    print(f'criterian20 Y/vigenere/KEY_5_L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian20(f'{path}/texts/Y/vigenere/KEY_10_L_10_N_{n}.log', 1))
    print(f'criterian20 Y/vigenere/KEY_10_L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian20(f'{path}/texts/Y/vigenere/KEY_10_L_100_N_{n}.log', 1))
    print(f'criterian20 Y/vigenere/KEY_10_L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian20(f'{path}/texts/Y/vigenere/KEY_10_L_1000_N_{n}.log', 30))
    print(f'criterian20 Y/vigenere/KEY_10_L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.criterian20(f'{path}/texts/Y/vigenere/KEY_10_L_10000_N_{n}.log', 210))
    print(f'criterian20 Y/vigenere/KEY_10_L_10000: {res.count(True)}')


    #criterian21

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian21(f'{path}/texts/X/L_10_N_{n}', 50, 1))
    print(f'criterian21 X/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian21(f'{path}/texts/X/L_100_N_{n}', 5, 2))
    print(f'criterian21 X/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian21(f'{path}/texts/X/L_1000_N_{n}', 50, 49))
    print(f'criterian21 X/L_1000: {res.count(True)}')

    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.criterian21(f'{path}/texts/X/L_10000_N_{n}', 210, 210))
    print(f'criterian21 X/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian21(f'{path}/texts/Y/affine/L_10_N_{n}.log', 50, 1))
    print(f'criterian21 Y/affine/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian21(f'{path}/texts/Y/affine/L_100_N_{n}.log', 5, 2))
    print(f'criterian21 Y/affine/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian21(f'{path}/texts/Y/affine/L_1000_N_{n}.log', 50, 49))
    print(f'criterian21 Y/affine/L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.criterian21(f'{path}/texts/Y/affine/L_10000_N_{n}.log', 210, 210))
    print(f'criterian21 Y/affine/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian21(f'{path}/texts/Y/recursive/L_10_N_{n}.log', 50, 1))
    print(f'criterian21 Y/recursive/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian21(f'{path}/texts/Y/recursive/L_100_N_{n}.log', 5, 2))
    print(f'criterian21 Y/recursive/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian21(f'{path}/texts/Y/recursive/L_1000_N_{n}.log', 50, 49))
    print(f'criterian21 Y/recursive/L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.criterian21(f'{path}/texts/Y/recursive/L_10000_N_{n}.log', 210, 210))
    print(f'criterian21 Y/recursive/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian21(f'{path}/texts/Y/uniform/L_10_N_{n}.log', 50, 1))
    print(f'criterian21 Y/uniform/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian21(f'{path}/texts/Y/uniform/L_100_N_{n}.log', 5, 2))
    print(f'criterian21 Y/uniform/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian21(f'{path}/texts/Y/uniform/L_1000_N_{n}.log', 50, 49))
    print(f'criterian21 Y/uniform/L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.criterian21(f'{path}/texts/Y/uniform/L_10000_N_{n}.log', 210, 210))
    print(f'criterian21 Y/uniform/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian21(f'{path}/texts/Y/vigenere/KEY_1_L_10_N_{n}.log', 50, 1))
    print(f'criterian21 Y/vigenere/KEY_1_L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian21(f'{path}/texts/Y/vigenere/KEY_1_L_100_N_{n}.log', 5, 2))
    print(f'criterian21 Y/vigenere/KEY_1_L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian21(f'{path}/texts/Y/vigenere/KEY_1_L_1000_N_{n}.log', 50, 49))
    print(f'criterian21 Y/vigenere/KEY_1_L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.criterian21(f'{path}/texts/Y/vigenere/KEY_1_L_10000_N_{n}.log', 210, 210))
    print(f'criterian21 Y/vigenere/KEY_1_L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian21(f'{path}/texts/Y/vigenere/KEY_5_L_10_N_{n}.log', 50, 1))
    print(f'criterian21 Y/vigenere/KEY_5_L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian21(f'{path}/texts/Y/vigenere/KEY_5_L_100_N_{n}.log', 5, 2))
    print(f'criterian21 Y/vigenere/KEY_5_L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian21(f'{path}/texts/Y/vigenere/KEY_5_L_1000_N_{n}.log', 50, 49))
    print(f'criterian21 Y/vigenere/KEY_5_L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.criterian21(f'{path}/texts/Y/vigenere/KEY_5_L_10000_N_{n}.log', 210, 210))
    print(f'criterian21 Y/vigenere/KEY_5_L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian21(f'{path}/texts/Y/vigenere/KEY_10_L_10_N_{n}.log', 50, 1))
    print(f'criterian21 Y/vigenere/KEY_10_L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian21(f'{path}/texts/Y/vigenere/KEY_10_L_100_N_{n}.log', 5, 2))
    print(f'criterian21 Y/vigenere/KEY_10_L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian21(f'{path}/texts/Y/vigenere/KEY_10_L_1000_N_{n}.log', 50, 49))
    print(f'criterian21 Y/vigenere/KEY_10_L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.criterian21(f'{path}/texts/Y/vigenere/KEY_10_L_10000_N_{n}.log', 210, 210))
    print(f'criterian21 Y/vigenere/KEY_10_L_10000: {res.count(True)}')

    #criterian22

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian22(f'{path}/texts/X/L_10_N_{n}', 1, 1))
    print(f'criterian22 X/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian22(f'{path}/texts/X/L_100_N_{n}', 1, 1))
    print(f'criterian22 X/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian22(f'{path}/texts/X/L_1000_N_{n}', 5, 4))
    print(f'criterian22 X/L_1000: {res.count(True)}')

    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.criterian22(f'{path}/texts/X/L_10000_N_{n}', 30, 40))
    print(f'criterian22 X/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian22(f'{path}/texts/Y/affine/L_10_N_{n}.log', 1, 1))
    print(f'criterian22 Y/affine/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian22(f'{path}/texts/Y/affine/L_100_N_{n}.log', 1, 1))
    print(f'criterian22 Y/affine/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian22(f'{path}/texts/Y/affine/L_1000_N_{n}.log', 5, 4))
    print(f'criterian22 Y/affine/L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.criterian22(f'{path}/texts/Y/affine/L_10000_N_{n}.log', 30, 40))
    print(f'criterian22 Y/affine/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian22(f'{path}/texts/Y/recursive/L_10_N_{n}.log', 1, 1))
    print(f'criterian22 Y/recursive/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian22(f'{path}/texts/Y/recursive/L_100_N_{n}.log', 1, 1))
    print(f'criterian22 Y/recursive/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian22(f'{path}/texts/Y/recursive/L_1000_N_{n}.log', 5, 4))
    print(f'criterian22 Y/recursive/L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.criterian22(f'{path}/texts/Y/recursive/L_10000_N_{n}.log', 30, 40))
    print(f'criterian22 Y/recursive/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian22(f'{path}/texts/Y/uniform/L_10_N_{n}.log', 1, 1))
    print(f'criterian22 Y/uniform/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian22(f'{path}/texts/Y/uniform/L_100_N_{n}.log', 1, 1))
    print(f'criterian22 Y/uniform/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian22(f'{path}/texts/Y/uniform/L_1000_N_{n}.log', 5, 4))
    print(f'criterian22 Y/uniform/L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.criterian22(f'{path}/texts/Y/uniform/L_10000_N_{n}.log', 30, 40))
    print(f'criterian22 Y/uniform/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian22(f'{path}/texts/Y/vigenere/KEY_1_L_10_N_{n}.log', 1, 1))
    print(f'criterian22 Y/vigenere/KEY_1_L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian22(f'{path}/texts/Y/vigenere/KEY_1_L_100_N_{n}.log', 1, 1))
    print(f'criterian22 Y/vigenere/KEY_1_L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian22(f'{path}/texts/Y/vigenere/KEY_1_L_1000_N_{n}.log', 5, 4))
    print(f'criterian22 Y/vigenere/KEY_1_L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.criterian22(f'{path}/texts/Y/vigenere/KEY_1_L_10000_N_{n}.log', 30, 40))
    print(f'criterian22 Y/vigenere/KEY_1_L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian22(f'{path}/texts/Y/vigenere/KEY_5_L_10_N_{n}.log', 1, 1))
    print(f'criterian22 Y/vigenere/KEY_5_L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian22(f'{path}/texts/Y/vigenere/KEY_5_L_100_N_{n}.log', 1, 1))
    print(f'criterian22 Y/vigenere/KEY_5_L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian22(f'{path}/texts/Y/vigenere/KEY_5_L_1000_N_{n}.log', 5, 4))
    print(f'criterian22 Y/vigenere/KEY_5_L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.criterian22(f'{path}/texts/Y/vigenere/KEY_5_L_10000_N_{n}.log', 30, 40))
    print(f'criterian22 Y/vigenere/KEY_5_L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian22(f'{path}/texts/Y/vigenere/KEY_10_L_10_N_{n}.log', 1, 1))
    print(f'criterian22 Y/vigenere/KEY_10_L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian22(f'{path}/texts/Y/vigenere/KEY_10_L_100_N_{n}.log', 1, 1))
    print(f'criterian22 Y/vigenere/KEY_10_L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian22(f'{path}/texts/Y/vigenere/KEY_10_L_1000_N_{n}.log', 5, 4))
    print(f'criterian22 Y/vigenere/KEY_10_L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.criterian22(f'{path}/texts/Y/vigenere/KEY_10_L_10000_N_{n}.log', 30, 40))
    print(f'criterian22 Y/vigenere/KEY_10_L_10000: {res.count(True)}')


    #criterian23

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian23(f'{path}/texts/X/L_10_N_{n}', 30, 1))
    print(f'criterian23 X/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian23(f'{path}/texts/X/L_100_N_{n}', 7, 4))
    print(f'criterian23 X/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian23(f'{path}/texts/X/L_1000_N_{n}', 20, 150))
    print(f'criterian23 X/L_1000: {res.count(True)}')

    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.criterian23(f'{path}/texts/X/L_10000_N_{n}', 20, 1700))
    print(f'criterian23 X/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian23(f'{path}/texts/Y/affine/L_10_N_{n}.log', 30, 1))
    print(f'criterian23 Y/affine/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian23(f'{path}/texts/Y/affine/L_100_N_{n}.log', 7, 4))
    print(f'criterian23 Y/affine/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian23(f'{path}/texts/Y/affine/L_1000_N_{n}.log', 20, 150))
    print(f'criterian23 Y/affine/L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.criterian23(f'{path}/texts/Y/affine/L_10000_N_{n}.log', 20, 1700))
    print(f'criterian23 Y/affine/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian23(f'{path}/texts/Y/recursive/L_10_N_{n}.log', 30, 1))
    print(f'criterian23 Y/recursive/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian23(f'{path}/texts/Y/recursive/L_100_N_{n}.log', 7, 4))
    print(f'criterian23 Y/recursive/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian23(f'{path}/texts/Y/recursive/L_1000_N_{n}.log', 20, 150))
    print(f'criterian23 Y/recursive/L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.criterian23(f'{path}/texts/Y/recursive/L_10000_N_{n}.log', 20, 1700))
    print(f'criterian23 Y/recursive/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian23(f'{path}/texts/Y/uniform/L_10_N_{n}.log', 30, 1))
    print(f'criterian23 Y/uniform/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian23(f'{path}/texts/Y/uniform/L_100_N_{n}.log', 7, 4))
    print(f'criterian23 Y/uniform/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian23(f'{path}/texts/Y/uniform/L_1000_N_{n}.log', 20, 150))
    print(f'criterian23 Y/uniform/L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.criterian23(f'{path}/texts/Y/uniform/L_10000_N_{n}.log', 20, 1700))
    print(f'criterian23 Y/uniform/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian23(f'{path}/texts/Y/vigenere/KEY_1_L_10_N_{n}.log', 30, 1))
    print(f'criterian23 Y/vigenere/KEY_1_L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian23(f'{path}/texts/Y/vigenere/KEY_1_L_100_N_{n}.log', 7, 4))
    print(f'criterian23 Y/vigenere/KEY_1_L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian23(f'{path}/texts/Y/vigenere/KEY_1_L_1000_N_{n}.log', 20, 150))
    print(f'criterian23 Y/vigenere/KEY_1_L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.criterian23(f'{path}/texts/Y/vigenere/KEY_1_L_10000_N_{n}.log', 20, 1700))
    print(f'criterian23 Y/vigenere/KEY_1_L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian23(f'{path}/texts/Y/vigenere/KEY_5_L_10_N_{n}.log', 30, 1))
    print(f'criterian23 Y/vigenere/KEY_5_L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian23(f'{path}/texts/Y/vigenere/KEY_5_L_100_N_{n}.log', 7, 4))
    print(f'criterian23 Y/vigenere/KEY_5_L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian23(f'{path}/texts/Y/vigenere/KEY_5_L_1000_N_{n}.log', 20, 150))
    print(f'criterian23 Y/vigenere/KEY_5_L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.criterian23(f'{path}/texts/Y/vigenere/KEY_5_L_10000_N_{n}.log', 20, 1700))
    print(f'criterian23 Y/vigenere/KEY_5_L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian23(f'{path}/texts/Y/vigenere/KEY_10_L_10_N_{n}.log', 30, 1))
    print(f'criterian23 Y/vigenere/KEY_10_L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian23(f'{path}/texts/Y/vigenere/KEY_10_L_100_N_{n}.log', 7, 4))
    print(f'criterian23 Y/vigenere/KEY_10_L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian23(f'{path}/texts/Y/vigenere/KEY_10_L_1000_N_{n}.log', 20, 150))
    print(f'criterian23 Y/vigenere/KEY_10_L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.criterian23(f'{path}/texts/Y/vigenere/KEY_10_L_10000_N_{n}.log', 20, 1700))
    print(f'criterian23 Y/vigenere/KEY_10_L_10000: {res.count(True)}')

    #criterian40

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian40(f'{path}/texts/X/L_10_N_{n}', .03))
    print(f'criterian40 X/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian40(f'{path}/texts/X/L_100_N_{n}', .003))
    print(f'criterian40 X/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian40(f'{path}/texts/X/L_1000_N_{n}', .001))
    print(f'criterian40 X/L_1000: {res.count(True)}')

    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.criterian40(f'{path}/texts/X/L_10000_N_{n}', .00035))
    print(f'criterian40 X/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian40(f'{path}/texts/Y/affine/L_10_N_{n}.log', .03))
    print(f'criterian40 Y/affine/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian40(f'{path}/texts/Y/affine/L_100_N_{n}.log', .003))
    print(f'criterian40 Y/affine/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian40(f'{path}/texts/Y/affine/L_1000_N_{n}.log', .001))
    print(f'criterian40 Y/affine/L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.criterian40(f'{path}/texts/Y/affine/L_10000_N_{n}.log', .00035))
    print(f'criterian40 Y/affine/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian40(f'{path}/texts/Y/recursive/L_10_N_{n}.log', .03))
    print(f'criterian40 Y/recursive/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian40(f'{path}/texts/Y/recursive/L_100_N_{n}.log', .003))
    print(f'criterian40 Y/recursive/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian40(f'{path}/texts/Y/recursive/L_1000_N_{n}.log', .001))
    print(f'criterian40 Y/recursive/L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.criterian40(f'{path}/texts/Y/recursive/L_10000_N_{n}.log', .00035))
    print(f'criterian40 Y/recursive/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian40(f'{path}/texts/Y/uniform/L_10_N_{n}.log', .03))
    print(f'criterian40 Y/uniform/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian40(f'{path}/texts/Y/uniform/L_100_N_{n}.log', .003))
    print(f'criterian40 Y/uniform/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian40(f'{path}/texts/Y/uniform/L_1000_N_{n}.log', .001))
    print(f'criterian40 Y/uniform/L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.criterian40(f'{path}/texts/Y/uniform/L_10000_N_{n}.log', .00035))
    print(f'criterian40 Y/uniform/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian40(f'{path}/texts/Y/vigenere/KEY_1_L_10_N_{n}.log', .03))
    print(f'criterian40 Y/vigenere/KEY_1_L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian40(f'{path}/texts/Y/vigenere/KEY_1_L_100_N_{n}.log', .003))
    print(f'criterian40 Y/vigenere/KEY_1_L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian40(f'{path}/texts/Y/vigenere/KEY_1_L_1000_N_{n}.log', .001))
    print(f'criterian40 Y/vigenere/KEY_1_L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.criterian40(f'{path}/texts/Y/vigenere/KEY_1_L_10000_N_{n}.log', .00035))
    print(f'criterian40 Y/vigenere/KEY_1_L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian40(f'{path}/texts/Y/vigenere/KEY_5_L_10_N_{n}.log', .03))
    print(f'criterian40 Y/vigenere/KEY_5_L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian40(f'{path}/texts/Y/vigenere/KEY_5_L_100_N_{n}.log', .003))
    print(f'criterian40 Y/vigenere/KEY_5_L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian40(f'{path}/texts/Y/vigenere/KEY_5_L_1000_N_{n}.log', .001))
    print(f'criterian40 Y/vigenere/KEY_5_L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.criterian40(f'{path}/texts/Y/vigenere/KEY_5_L_10000_N_{n}.log', .00035))
    print(f'criterian40 Y/vigenere/KEY_5_L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian40(f'{path}/texts/Y/vigenere/KEY_10_L_10_N_{n}.log', .03))
    print(f'criterian40 Y/vigenere/KEY_10_L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian40(f'{path}/texts/Y/vigenere/KEY_10_L_100_N_{n}.log', .003))
    print(f'criterian40 Y/vigenere/KEY_10_L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian40(f'{path}/texts/Y/vigenere/KEY_10_L_1000_N_{n}.log', .001))
    print(f'criterian40 Y/vigenere/KEY_10_L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.criterian40(f'{path}/texts/Y/vigenere/KEY_10_L_10000_N_{n}.log', .00035))
    print(f'criterian40 Y/vigenere/KEY_10_L_10000: {res.count(True)}')

    #criterian50

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian50(f'{path}/texts/X/L_10_N_{n}', 500,497))
    print(f'criterian50 X/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian50(f'{path}/texts/X/L_100_N_{n}', 100, 99))
    print(f'criterian50 X/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian50(f'{path}/texts/X/L_1000_N_{n}', 50, 49))
    print(f'criterian50 X/L_1000: {res.count(True)}')

    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.criterian50(f'{path}/texts/X/L_10000_N_{n}', 50, 47))
    print(f'criterian50 X/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian50(f'{path}/texts/Y/affine/L_10_N_{n}.log', 500, 497))
    print(f'criterian50 Y/affine/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian50(f'{path}/texts/Y/affine/L_100_N_{n}.log', 100, 99))
    print(f'criterian50 Y/affine/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian50(f'{path}/texts/Y/affine/L_1000_N_{n}.log', 50, 49))
    print(f'criterian50 Y/affine/L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.criterian50(f'{path}/texts/Y/affine/L_10000_N_{n}.log', 50, 47))
    print(f'criterian50 Y/affine/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian50(f'{path}/texts/Y/recursive/L_10_N_{n}.log', 500, 497))
    print(f'criterian50 Y/recursive/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian50(f'{path}/texts/Y/recursive/L_100_N_{n}.log', 100, 99))
    print(f'criterian50 Y/recursive/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian50(f'{path}/texts/Y/recursive/L_1000_N_{n}.log', 50, 49))
    print(f'criterian50 Y/recursive/L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.criterian50(f'{path}/texts/Y/recursive/L_10000_N_{n}.log', 50, 47))
    print(f'criterian50 Y/recursive/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian50(f'{path}/texts/Y/uniform/L_10_N_{n}.log', 500, 497))
    print(f'criterian50 Y/uniform/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian50(f'{path}/texts/Y/uniform/L_100_N_{n}.log', 100, 99))
    print(f'criterian50 Y/uniform/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian50(f'{path}/texts/Y/uniform/L_1000_N_{n}.log', 50, 49))
    print(f'criterian50 Y/uniform/L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.criterian50(f'{path}/texts/Y/uniform/L_10000_N_{n}.log', 50, 47))
    print(f'criterian50 Y/uniform/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian50(f'{path}/texts/Y/vigenere/KEY_1_L_10_N_{n}.log', 500, 497))
    print(f'criterian50 Y/vigenere/KEY_1_L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian50(f'{path}/texts/Y/vigenere/KEY_1_L_100_N_{n}.log', 100, 99))
    print(f'criterian50 Y/vigenere/KEY_1_L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian50(f'{path}/texts/Y/vigenere/KEY_1_L_1000_N_{n}.log', 50, 49))
    print(f'criterian50 Y/vigenere/KEY_1_L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.criterian50(f'{path}/texts/Y/vigenere/KEY_1_L_10000_N_{n}.log', 50, 47))
    print(f'criterian50 Y/vigenere/KEY_1_L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian50(f'{path}/texts/Y/vigenere/KEY_5_L_10_N_{n}.log', 500, 497))
    print(f'criterian50 Y/vigenere/KEY_5_L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian50(f'{path}/texts/Y/vigenere/KEY_5_L_100_N_{n}.log', 100, 99))
    print(f'criterian50 Y/vigenere/KEY_5_L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian50(f'{path}/texts/Y/vigenere/KEY_5_L_1000_N_{n}.log', 50, 49))
    print(f'criterian50 Y/vigenere/KEY_5_L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.criterian50(f'{path}/texts/Y/vigenere/KEY_5_L_10000_N_{n}.log', 50, 47))
    print(f'criterian50 Y/vigenere/KEY_5_L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian50(f'{path}/texts/Y/vigenere/KEY_10_L_10_N_{n}.log', 500, 497))
    print(f'criterian50 Y/vigenere/KEY_10_L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian50(f'{path}/texts/Y/vigenere/KEY_10_L_100_N_{n}.log', 100, 99))
    print(f'criterian50 Y/vigenere/KEY_10_L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.criterian50(f'{path}/texts/Y/vigenere/KEY_10_L_1000_N_{n}.log', 50, 49))
    print(f'criterian50 Y/vigenere/KEY_10_L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.criterian50(f'{path}/texts/Y/vigenere/KEY_10_L_10000_N_{n}.log', 50, 47))
    print(f'criterian50 Y/vigenere/KEY_10_L_10000: {res.count(True)}')

    # structual

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.structuralCriterian(f'{path}/texts/X/L_1000_N_{n}', 48))
    print(f'structual X/L_1000: {res.count(True)}')

    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.structuralCriterian(f'{path}/texts/X/L_10000_N_{n}', 66.2))
    print(f'structual X/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.structuralCriterian(f'{path}/texts/Y/affine/L_1000_N_{n}.log', 48))
    print(f'structual Y/affine/L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.structuralCriterian(f'{path}/texts/Y/affine/L_10000_N_{n}.log', 66.2))
    print(f'structual Y/affine/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.structuralCriterian(f'{path}/texts/Y/recursive/L_1000_N_{n}.log', 48))
    print(f'structual Y/recursive/L_1000: {res.count(True)}')

    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.structuralCriterian(f'{path}/texts/Y/recursive/L_10000_N_{n}.log', 66.2))
    print(f'structual Y/recursive/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.structuralCriterian(f'{path}/texts/Y/uniform/L_1000_N_{n}.log', 48))
    print(f'structual Y/uniform/L_1000: {res.count(True)}')

    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.structuralCriterian(f'{path}/texts/Y/uniform/L_10000_N_{n}.log', 66.2))
    print(f'structual Y/uniform/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.structuralCriterian(f'{path}/texts/Y/vigenere/KEY_1_L_1000_N_{n}.log', 48))
    print(f'structual Y/vigenere/KEY_1_L_1000: {res.count(True)}')

    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.structuralCriterian(f'{path}/texts/Y/vigenere/KEY_1_L_10000_N_{n}.log', 66.2))
    print(f'structual Y/vigenere/KEY_1_L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.structuralCriterian(f'{path}/texts/Y/vigenere/KEY_5_L_1000_N_{n}.log', 48))
    print(f'structual Y/vigenere/KEY_5_L_1000: {res.count(True)}')

    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.structuralCriterian(f'{path}/texts/Y/vigenere/KEY_5_L_10000_N_{n}.log', 66.2))
    print(f'structual Y/vigenere/KEY_5_L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_letters.structuralCriterian(f'{path}/texts/Y/vigenere/KEY_10_L_1000_N_{n}.log', 48))
    print(f'structual Y/vigenere/KEY_10_L_1000: {res.count(True)}')

    res = []
    for n in range(1, 1001):
        res.append(criterion_letters.structuralCriterian(f'{path}/texts/Y/vigenere/KEY_10_L_10000_N_{n}.log', 66.2))
    print(f'structual Y/vigenere/KEY_10_L_10000: {res.count(True)}')
    
    
   #=======================================================

    bigrams_frequency = json.loads(read(f'{path}/result/bigrams_frequency.json'))
    criterion_bigrams = Criterion(bigrams_frequency)

    #criterian20

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian20(f'{path}/texts/X/L_10_N_{n}', 1))
    print(f'criterian20 X/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian20(f'{path}/texts/X/L_100_N_{n}', 1))
    print(f'criterian20 X/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian20(f'{path}/texts/X/L_1000_N_{n}', 30))
    print(f'criterian20 X/L_1000: {res.count(True)}')

    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.criterian20(f'{path}/texts/X/L_10000_N_{n}', 210))
    print(f'criterian20 X/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian20(f'{path}/texts/Y/affine/L_10_N_{n}.log', 1))
    print(f'criterian20 Y/affine/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian20(f'{path}/texts/Y/affine/L_100_N_{n}.log', 1))
    print(f'criterian20 Y/affine/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian20(f'{path}/texts/Y/affine/L_1000_N_{n}.log', 30))
    print(f'criterian20 Y/affine/L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.criterian20(f'{path}/texts/Y/affine/L_10000_N_{n}.log', 210))
    print(f'criterian20 Y/affine/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian20(f'{path}/texts/Y/recursive/L_10_N_{n}.log', 1))
    print(f'criterian20 Y/recursive/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian20(f'{path}/texts/Y/recursive/L_100_N_{n}.log', 1))
    print(f'criterian20 Y/recursive/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian20(f'{path}/texts/Y/recursive/L_1000_N_{n}.log', 30))
    print(f'criterian20 Y/recursive/L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.criterian20(f'{path}/texts/Y/recursive/L_10000_N_{n}.log', 210))
    print(f'criterian20 Y/recursive/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian20(f'{path}/texts/Y/uniform/L_10_N_{n}.log', 1))
    print(f'criterian20 Y/uniform/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian20(f'{path}/texts/Y/uniform/L_100_N_{n}.log', 1))
    print(f'criterian20 Y/uniform/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian20(f'{path}/texts/Y/uniform/L_1000_N_{n}.log', 30))
    print(f'criterian20 Y/uniform/L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.criterian20(f'{path}/texts/Y/uniform/L_10000_N_{n}.log', 210))
    print(f'criterian20 Y/uniform/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian20(f'{path}/texts/Y/vigenere/KEY_1_L_10_N_{n}.log', 1))
    print(f'criterian20 Y/vigenere/KEY_1_L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian20(f'{path}/texts/Y/vigenere/KEY_1_L_100_N_{n}.log', 1))
    print(f'criterian20 Y/vigenere/KEY_1_L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian20(f'{path}/texts/Y/vigenere/KEY_1_L_1000_N_{n}.log', 30))
    print(f'criterian20 Y/vigenere/KEY_1_L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.criterian20(f'{path}/texts/Y/vigenere/KEY_1_L_10000_N_{n}.log', 210))
    print(f'criterian20 Y/vigenere/KEY_1_L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian20(f'{path}/texts/Y/vigenere/KEY_5_L_10_N_{n}.log', 1))
    print(f'criterian20 Y/vigenere/KEY_5_L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian20(f'{path}/texts/Y/vigenere/KEY_5_L_100_N_{n}.log', 1))
    print(f'criterian20 Y/vigenere/KEY_5_L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian20(f'{path}/texts/Y/vigenere/KEY_5_L_1000_N_{n}.log', 30))
    print(f'criterian20 Y/vigenere/KEY_5_L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.criterian20(f'{path}/texts/Y/vigenere/KEY_5_L_10000_N_{n}.log', 210))
    print(f'criterian20 Y/vigenere/KEY_5_L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian20(f'{path}/texts/Y/vigenere/KEY_10_L_10_N_{n}.log', 1))
    print(f'criterian20 Y/vigenere/KEY_10_L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian20(f'{path}/texts/Y/vigenere/KEY_10_L_100_N_{n}.log', 1))
    print(f'criterian20 Y/vigenere/KEY_10_L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian20(f'{path}/texts/Y/vigenere/KEY_10_L_1000_N_{n}.log', 30))
    print(f'criterian20 Y/vigenere/KEY_10_L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.criterian20(f'{path}/texts/Y/vigenere/KEY_10_L_10000_N_{n}.log', 210))
    print(f'criterian20 Y/vigenere/KEY_10_L_10000: {res.count(True)}')


    #criterian21

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian21(f'{path}/texts/X/L_10_N_{n}', 50, 1))
    print(f'criterian21 X/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian21(f'{path}/texts/X/L_100_N_{n}', 5, 2))
    print(f'criterian21 X/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian21(f'{path}/texts/X/L_1000_N_{n}', 50, 49))
    print(f'criterian21 X/L_1000: {res.count(True)}')

    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.criterian21(f'{path}/texts/X/L_10000_N_{n}', 210, 210))
    print(f'criterian21 X/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian21(f'{path}/texts/Y/affine/L_10_N_{n}.log', 50, 1))
    print(f'criterian21 Y/affine/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian21(f'{path}/texts/Y/affine/L_100_N_{n}.log', 5, 2))
    print(f'criterian21 Y/affine/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian21(f'{path}/texts/Y/affine/L_1000_N_{n}.log', 50, 49))
    print(f'criterian21 Y/affine/L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.criterian21(f'{path}/texts/Y/affine/L_10000_N_{n}.log', 210, 210))
    print(f'criterian21 Y/affine/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian21(f'{path}/texts/Y/recursive/L_10_N_{n}.log', 50, 1))
    print(f'criterian21 Y/recursive/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian21(f'{path}/texts/Y/recursive/L_100_N_{n}.log', 5, 2))
    print(f'criterian21 Y/recursive/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian21(f'{path}/texts/Y/recursive/L_1000_N_{n}.log', 50, 49))
    print(f'criterian21 Y/recursive/L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.criterian21(f'{path}/texts/Y/recursive/L_10000_N_{n}.log', 210, 210))
    print(f'criterian21 Y/recursive/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian21(f'{path}/texts/Y/uniform/L_10_N_{n}.log', 50, 1))
    print(f'criterian21 Y/uniform/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian21(f'{path}/texts/Y/uniform/L_100_N_{n}.log', 5, 2))
    print(f'criterian21 Y/uniform/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian21(f'{path}/texts/Y/uniform/L_1000_N_{n}.log', 50, 49))
    print(f'criterian21 Y/uniform/L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.criterian21(f'{path}/texts/Y/uniform/L_10000_N_{n}.log', 210, 210))
    print(f'criterian21 Y/uniform/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian21(f'{path}/texts/Y/vigenere/KEY_1_L_10_N_{n}.log', 50, 1))
    print(f'criterian21 Y/vigenere/KEY_1_L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian21(f'{path}/texts/Y/vigenere/KEY_1_L_100_N_{n}.log', 5, 2))
    print(f'criterian21 Y/vigenere/KEY_1_L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian21(f'{path}/texts/Y/vigenere/KEY_1_L_1000_N_{n}.log', 50, 49))
    print(f'criterian21 Y/vigenere/KEY_1_L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.criterian21(f'{path}/texts/Y/vigenere/KEY_1_L_10000_N_{n}.log', 210, 210))
    print(f'criterian21 Y/vigenere/KEY_1_L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian21(f'{path}/texts/Y/vigenere/KEY_5_L_10_N_{n}.log', 50, 1))
    print(f'criterian21 Y/vigenere/KEY_5_L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian21(f'{path}/texts/Y/vigenere/KEY_5_L_100_N_{n}.log', 5, 2))
    print(f'criterian21 Y/vigenere/KEY_5_L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian21(f'{path}/texts/Y/vigenere/KEY_5_L_1000_N_{n}.log', 50, 49))
    print(f'criterian21 Y/vigenere/KEY_5_L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.criterian21(f'{path}/texts/Y/vigenere/KEY_5_L_10000_N_{n}.log', 210, 210))
    print(f'criterian21 Y/vigenere/KEY_5_L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian21(f'{path}/texts/Y/vigenere/KEY_10_L_10_N_{n}.log', 50, 1))
    print(f'criterian21 Y/vigenere/KEY_10_L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian21(f'{path}/texts/Y/vigenere/KEY_10_L_100_N_{n}.log', 5, 2))
    print(f'criterian21 Y/vigenere/KEY_10_L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian21(f'{path}/texts/Y/vigenere/KEY_10_L_1000_N_{n}.log', 50, 49))
    print(f'criterian21 Y/vigenere/KEY_10_L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.criterian21(f'{path}/texts/Y/vigenere/KEY_10_L_10000_N_{n}.log', 210, 210))
    print(f'criterian21 Y/vigenere/KEY_10_L_10000: {res.count(True)}')

    #criterian22

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian22(f'{path}/texts/X/L_10_N_{n}', 1, 1))
    print(f'criterian22 X/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian22(f'{path}/texts/X/L_100_N_{n}', 1, 1))
    print(f'criterian22 X/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian22(f'{path}/texts/X/L_1000_N_{n}', 5, 4))
    print(f'criterian22 X/L_1000: {res.count(True)}')

    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.criterian22(f'{path}/texts/X/L_10000_N_{n}', 30, 40))
    print(f'criterian22 X/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian22(f'{path}/texts/Y/affine/L_10_N_{n}.log', 1, 1))
    print(f'criterian22 Y/affine/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian22(f'{path}/texts/Y/affine/L_100_N_{n}.log', 1, 1))
    print(f'criterian22 Y/affine/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian22(f'{path}/texts/Y/affine/L_1000_N_{n}.log', 5, 4))
    print(f'criterian22 Y/affine/L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.criterian22(f'{path}/texts/Y/affine/L_10000_N_{n}.log', 30, 40))
    print(f'criterian22 Y/affine/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian22(f'{path}/texts/Y/recursive/L_10_N_{n}.log', 1, 1))
    print(f'criterian22 Y/recursive/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian22(f'{path}/texts/Y/recursive/L_100_N_{n}.log', 1, 1))
    print(f'criterian22 Y/recursive/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian22(f'{path}/texts/Y/recursive/L_1000_N_{n}.log', 5, 4))
    print(f'criterian22 Y/recursive/L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.criterian22(f'{path}/texts/Y/recursive/L_10000_N_{n}.log', 30, 40))
    print(f'criterian22 Y/recursive/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian22(f'{path}/texts/Y/uniform/L_10_N_{n}.log', 1, 1))
    print(f'criterian22 Y/uniform/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian22(f'{path}/texts/Y/uniform/L_100_N_{n}.log', 1, 1))
    print(f'criterian22 Y/uniform/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian22(f'{path}/texts/Y/uniform/L_1000_N_{n}.log', 5, 4))
    print(f'criterian22 Y/uniform/L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.criterian22(f'{path}/texts/Y/uniform/L_10000_N_{n}.log', 30, 40))
    print(f'criterian22 Y/uniform/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian22(f'{path}/texts/Y/vigenere/KEY_1_L_10_N_{n}.log', 1, 1))
    print(f'criterian22 Y/vigenere/KEY_1_L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian22(f'{path}/texts/Y/vigenere/KEY_1_L_100_N_{n}.log', 1, 1))
    print(f'criterian22 Y/vigenere/KEY_1_L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian22(f'{path}/texts/Y/vigenere/KEY_1_L_1000_N_{n}.log', 5, 4))
    print(f'criterian22 Y/vigenere/KEY_1_L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.criterian22(f'{path}/texts/Y/vigenere/KEY_1_L_10000_N_{n}.log', 30, 40))
    print(f'criterian22 Y/vigenere/KEY_1_L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian22(f'{path}/texts/Y/vigenere/KEY_5_L_10_N_{n}.log', 1, 1))
    print(f'criterian22 Y/vigenere/KEY_5_L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian22(f'{path}/texts/Y/vigenere/KEY_5_L_100_N_{n}.log', 1, 1))
    print(f'criterian22 Y/vigenere/KEY_5_L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian22(f'{path}/texts/Y/vigenere/KEY_5_L_1000_N_{n}.log', 5, 4))
    print(f'criterian22 Y/vigenere/KEY_5_L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.criterian22(f'{path}/texts/Y/vigenere/KEY_5_L_10000_N_{n}.log', 30, 40))
    print(f'criterian22 Y/vigenere/KEY_5_L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian22(f'{path}/texts/Y/vigenere/KEY_10_L_10_N_{n}.log', 1, 1))
    print(f'criterian22 Y/vigenere/KEY_10_L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian22(f'{path}/texts/Y/vigenere/KEY_10_L_100_N_{n}.log', 1, 1))
    print(f'criterian22 Y/vigenere/KEY_10_L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian22(f'{path}/texts/Y/vigenere/KEY_10_L_1000_N_{n}.log', 5, 4))
    print(f'criterian22 Y/vigenere/KEY_10_L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.criterian22(f'{path}/texts/Y/vigenere/KEY_10_L_10000_N_{n}.log', 30, 40))
    print(f'criterian22 Y/vigenere/KEY_10_L_10000: {res.count(True)}')


    #criterian23

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian23(f'{path}/texts/X/L_10_N_{n}', 30, 1))
    print(f'criterian23 X/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian23(f'{path}/texts/X/L_100_N_{n}', 7, 4))
    print(f'criterian23 X/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian23(f'{path}/texts/X/L_1000_N_{n}', 20, 150))
    print(f'criterian23 X/L_1000: {res.count(True)}')

    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.criterian23(f'{path}/texts/X/L_10000_N_{n}', 20, 1700))
    print(f'criterian23 X/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian23(f'{path}/texts/Y/affine/L_10_N_{n}.log', 30, 1))
    print(f'criterian23 Y/affine/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian23(f'{path}/texts/Y/affine/L_100_N_{n}.log', 7, 4))
    print(f'criterian23 Y/affine/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian23(f'{path}/texts/Y/affine/L_1000_N_{n}.log', 20, 150))
    print(f'criterian23 Y/affine/L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.criterian23(f'{path}/texts/Y/affine/L_10000_N_{n}.log', 20, 1700))
    print(f'criterian23 Y/affine/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian23(f'{path}/texts/Y/recursive/L_10_N_{n}.log', 30, 1))
    print(f'criterian23 Y/recursive/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian23(f'{path}/texts/Y/recursive/L_100_N_{n}.log', 7, 4))
    print(f'criterian23 Y/recursive/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian23(f'{path}/texts/Y/recursive/L_1000_N_{n}.log', 20, 150))
    print(f'criterian23 Y/recursive/L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.criterian23(f'{path}/texts/Y/recursive/L_10000_N_{n}.log', 20, 1700))
    print(f'criterian23 Y/recursive/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian23(f'{path}/texts/Y/uniform/L_10_N_{n}.log', 30, 1))
    print(f'criterian23 Y/uniform/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian23(f'{path}/texts/Y/uniform/L_100_N_{n}.log', 7, 4))
    print(f'criterian23 Y/uniform/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian23(f'{path}/texts/Y/uniform/L_1000_N_{n}.log', 20, 150))
    print(f'criterian23 Y/uniform/L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.criterian23(f'{path}/texts/Y/uniform/L_10000_N_{n}.log', 20, 1700))
    print(f'criterian23 Y/uniform/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian23(f'{path}/texts/Y/vigenere/KEY_1_L_10_N_{n}.log', 30, 1))
    print(f'criterian23 Y/vigenere/KEY_1_L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian23(f'{path}/texts/Y/vigenere/KEY_1_L_100_N_{n}.log', 7, 4))
    print(f'criterian23 Y/vigenere/KEY_1_L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian23(f'{path}/texts/Y/vigenere/KEY_1_L_1000_N_{n}.log', 20, 150))
    print(f'criterian23 Y/vigenere/KEY_1_L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.criterian23(f'{path}/texts/Y/vigenere/KEY_1_L_10000_N_{n}.log', 20, 1700))
    print(f'criterian23 Y/vigenere/KEY_1_L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian23(f'{path}/texts/Y/vigenere/KEY_5_L_10_N_{n}.log', 30, 1))
    print(f'criterian23 Y/vigenere/KEY_5_L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian23(f'{path}/texts/Y/vigenere/KEY_5_L_100_N_{n}.log', 7, 4))
    print(f'criterian23 Y/vigenere/KEY_5_L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian23(f'{path}/texts/Y/vigenere/KEY_5_L_1000_N_{n}.log', 20, 150))
    print(f'criterian23 Y/vigenere/KEY_5_L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.criterian23(f'{path}/texts/Y/vigenere/KEY_5_L_10000_N_{n}.log', 20, 1700))
    print(f'criterian23 Y/vigenere/KEY_5_L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian23(f'{path}/texts/Y/vigenere/KEY_10_L_10_N_{n}.log', 30, 1))
    print(f'criterian23 Y/vigenere/KEY_10_L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian23(f'{path}/texts/Y/vigenere/KEY_10_L_100_N_{n}.log', 7, 4))
    print(f'criterian23 Y/vigenere/KEY_10_L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian23(f'{path}/texts/Y/vigenere/KEY_10_L_1000_N_{n}.log', 20, 150))
    print(f'criterian23 Y/vigenere/KEY_10_L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.criterian23(f'{path}/texts/Y/vigenere/KEY_10_L_10000_N_{n}.log', 20, 1700))
    print(f'criterian23 Y/vigenere/KEY_10_L_10000: {res.count(True)}')

    #criterian40

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian40(f'{path}/texts/X/L_10_N_{n}', .03))
    print(f'criterian40 X/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian40(f'{path}/texts/X/L_100_N_{n}', .003))
    print(f'criterian40 X/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian40(f'{path}/texts/X/L_1000_N_{n}', .001))
    print(f'criterian40 X/L_1000: {res.count(True)}')

    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.criterian40(f'{path}/texts/X/L_10000_N_{n}', .00035))
    print(f'criterian40 X/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian40(f'{path}/texts/Y/affine/L_10_N_{n}.log', .03))
    print(f'criterian40 Y/affine/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian40(f'{path}/texts/Y/affine/L_100_N_{n}.log', .003))
    print(f'criterian40 Y/affine/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian40(f'{path}/texts/Y/affine/L_1000_N_{n}.log', .001))
    print(f'criterian40 Y/affine/L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.criterian40(f'{path}/texts/Y/affine/L_10000_N_{n}.log', .00035))
    print(f'criterian40 Y/affine/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian40(f'{path}/texts/Y/recursive/L_10_N_{n}.log', .03))
    print(f'criterian40 Y/recursive/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian40(f'{path}/texts/Y/recursive/L_100_N_{n}.log', .003))
    print(f'criterian40 Y/recursive/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian40(f'{path}/texts/Y/recursive/L_1000_N_{n}.log', .001))
    print(f'criterian40 Y/recursive/L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.criterian40(f'{path}/texts/Y/recursive/L_10000_N_{n}.log', .00035))
    print(f'criterian40 Y/recursive/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian40(f'{path}/texts/Y/uniform/L_10_N_{n}.log', .03))
    print(f'criterian40 Y/uniform/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian40(f'{path}/texts/Y/uniform/L_100_N_{n}.log', .003))
    print(f'criterian40 Y/uniform/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian40(f'{path}/texts/Y/uniform/L_1000_N_{n}.log', .001))
    print(f'criterian40 Y/uniform/L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.criterian40(f'{path}/texts/Y/uniform/L_10000_N_{n}.log', .00035))
    print(f'criterian40 Y/uniform/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian40(f'{path}/texts/Y/vigenere/KEY_1_L_10_N_{n}.log', .03))
    print(f'criterian40 Y/vigenere/KEY_1_L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian40(f'{path}/texts/Y/vigenere/KEY_1_L_100_N_{n}.log', .003))
    print(f'criterian40 Y/vigenere/KEY_1_L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian40(f'{path}/texts/Y/vigenere/KEY_1_L_1000_N_{n}.log', .001))
    print(f'criterian40 Y/vigenere/KEY_1_L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.criterian40(f'{path}/texts/Y/vigenere/KEY_1_L_10000_N_{n}.log', .00035))
    print(f'criterian40 Y/vigenere/KEY_1_L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian40(f'{path}/texts/Y/vigenere/KEY_5_L_10_N_{n}.log', .03))
    print(f'criterian40 Y/vigenere/KEY_5_L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian40(f'{path}/texts/Y/vigenere/KEY_5_L_100_N_{n}.log', .003))
    print(f'criterian40 Y/vigenere/KEY_5_L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian40(f'{path}/texts/Y/vigenere/KEY_5_L_1000_N_{n}.log', .001))
    print(f'criterian40 Y/vigenere/KEY_5_L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.criterian40(f'{path}/texts/Y/vigenere/KEY_5_L_10000_N_{n}.log', .00035))
    print(f'criterian40 Y/vigenere/KEY_5_L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian40(f'{path}/texts/Y/vigenere/KEY_10_L_10_N_{n}.log', .03))
    print(f'criterian40 Y/vigenere/KEY_10_L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian40(f'{path}/texts/Y/vigenere/KEY_10_L_100_N_{n}.log', .003))
    print(f'criterian40 Y/vigenere/KEY_10_L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian40(f'{path}/texts/Y/vigenere/KEY_10_L_1000_N_{n}.log', .001))
    print(f'criterian40 Y/vigenere/KEY_10_L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.criterian40(f'{path}/texts/Y/vigenere/KEY_10_L_10000_N_{n}.log', .00035))
    print(f'criterian40 Y/vigenere/KEY_10_L_10000: {res.count(True)}')

    #criterian50

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian50(f'{path}/texts/X/L_10_N_{n}', 500,497))
    print(f'criterian50 X/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian50(f'{path}/texts/X/L_100_N_{n}', 100, 99))
    print(f'criterian50 X/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian50(f'{path}/texts/X/L_1000_N_{n}', 50, 49))
    print(f'criterian50 X/L_1000: {res.count(True)}')

    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.criterian50(f'{path}/texts/X/L_10000_N_{n}', 50, 47))
    print(f'criterian50 X/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian50(f'{path}/texts/Y/affine/L_10_N_{n}.log', 500, 497))
    print(f'criterian50 Y/affine/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian50(f'{path}/texts/Y/affine/L_100_N_{n}.log', 100, 99))
    print(f'criterian50 Y/affine/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian50(f'{path}/texts/Y/affine/L_1000_N_{n}.log', 50, 49))
    print(f'criterian50 Y/affine/L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.criterian50(f'{path}/texts/Y/affine/L_10000_N_{n}.log', 50, 47))
    print(f'criterian50 Y/affine/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian50(f'{path}/texts/Y/recursive/L_10_N_{n}.log', 500, 497))
    print(f'criterian50 Y/recursive/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian50(f'{path}/texts/Y/recursive/L_100_N_{n}.log', 100, 99))
    print(f'criterian50 Y/recursive/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian50(f'{path}/texts/Y/recursive/L_1000_N_{n}.log', 50, 49))
    print(f'criterian50 Y/recursive/L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.criterian50(f'{path}/texts/Y/recursive/L_10000_N_{n}.log', 50, 47))
    print(f'criterian50 Y/recursive/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian50(f'{path}/texts/Y/uniform/L_10_N_{n}.log', 500, 497))
    print(f'criterian50 Y/uniform/L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian50(f'{path}/texts/Y/uniform/L_100_N_{n}.log', 100, 99))
    print(f'criterian50 Y/uniform/L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian50(f'{path}/texts/Y/uniform/L_1000_N_{n}.log', 50, 49))
    print(f'criterian50 Y/uniform/L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.criterian50(f'{path}/texts/Y/uniform/L_10000_N_{n}.log', 50, 47))
    print(f'criterian50 Y/uniform/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian50(f'{path}/texts/Y/vigenere/KEY_1_L_10_N_{n}.log', 500, 497))
    print(f'criterian50 Y/vigenere/KEY_1_L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian50(f'{path}/texts/Y/vigenere/KEY_1_L_100_N_{n}.log', 100, 99))
    print(f'criterian50 Y/vigenere/KEY_1_L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian50(f'{path}/texts/Y/vigenere/KEY_1_L_1000_N_{n}.log', 50, 49))
    print(f'criterian50 Y/vigenere/KEY_1_L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.criterian50(f'{path}/texts/Y/vigenere/KEY_1_L_10000_N_{n}.log', 50, 47))
    print(f'criterian50 Y/vigenere/KEY_1_L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian50(f'{path}/texts/Y/vigenere/KEY_5_L_10_N_{n}.log', 500, 497))
    print(f'criterian50 Y/vigenere/KEY_5_L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian50(f'{path}/texts/Y/vigenere/KEY_5_L_100_N_{n}.log', 100, 99))
    print(f'criterian50 Y/vigenere/KEY_5_L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian50(f'{path}/texts/Y/vigenere/KEY_5_L_1000_N_{n}.log', 50, 49))
    print(f'criterian50 Y/vigenere/KEY_5_L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.criterian50(f'{path}/texts/Y/vigenere/KEY_5_L_10000_N_{n}.log', 50, 47))
    print(f'criterian50 Y/vigenere/KEY_5_L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian50(f'{path}/texts/Y/vigenere/KEY_10_L_10_N_{n}.log', 500, 497))
    print(f'criterian50 Y/vigenere/KEY_10_L_10: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian50(f'{path}/texts/Y/vigenere/KEY_10_L_100_N_{n}.log', 100, 99))
    print(f'criterian50 Y/vigenere/KEY_10_L_100: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.criterian50(f'{path}/texts/Y/vigenere/KEY_10_L_1000_N_{n}.log', 50, 49))
    print(f'criterian50 Y/vigenere/KEY_10_L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.criterian50(f'{path}/texts/Y/vigenere/KEY_10_L_10000_N_{n}.log', 50, 47))
    print(f'criterian50 Y/vigenere/KEY_10_L_10000: {res.count(True)}')

    # structual

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.structuralCriterian(f'{path}/texts/X/L_1000_N_{n}', 48))
    print(f'structual X/L_1000: {res.count(True)}')

    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.structuralCriterian(f'{path}/texts/X/L_10000_N_{n}', 66.2))
    print(f'structual X/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.structuralCriterian(f'{path}/texts/Y/affine/L_1000_N_{n}.log', 48))
    print(f'structual Y/affine/L_1000: {res.count(True)}')
    
    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.structuralCriterian(f'{path}/texts/Y/affine/L_10000_N_{n}.log', 66.2))
    print(f'structual Y/affine/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.structuralCriterian(f'{path}/texts/Y/recursive/L_1000_N_{n}.log', 48))
    print(f'structual Y/recursive/L_1000: {res.count(True)}')

    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.structuralCriterian(f'{path}/texts/Y/recursive/L_10000_N_{n}.log', 66.2))
    print(f'structual Y/recursive/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.structuralCriterian(f'{path}/texts/Y/uniform/L_1000_N_{n}.log', 48))
    print(f'structual Y/uniform/L_1000: {res.count(True)}')

    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.structuralCriterian(f'{path}/texts/Y/uniform/L_10000_N_{n}.log', 66.2))
    print(f'structual Y/uniform/L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.structuralCriterian(f'{path}/texts/Y/vigenere/KEY_1_L_1000_N_{n}.log', 48))
    print(f'structual Y/vigenere/KEY_1_L_1000: {res.count(True)}')

    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.structuralCriterian(f'{path}/texts/Y/vigenere/KEY_1_L_10000_N_{n}.log', 66.2))
    print(f'structual Y/vigenere/KEY_1_L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.structuralCriterian(f'{path}/texts/Y/vigenere/KEY_5_L_1000_N_{n}.log', 48))
    print(f'structual Y/vigenere/KEY_5_L_1000: {res.count(True)}')

    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.structuralCriterian(f'{path}/texts/Y/vigenere/KEY_5_L_10000_N_{n}.log', 66.2))
    print(f'structual Y/vigenere/KEY_5_L_10000: {res.count(True)}')

    res = []
    for n in range(1, 10001):
        res.append(criterion_bigrams.structuralCriterian(f'{path}/texts/Y/vigenere/KEY_10_L_1000_N_{n}.log', 48))
    print(f'structual Y/vigenere/KEY_10_L_1000: {res.count(True)}')

    res = []
    for n in range(1, 1001):
        res.append(criterion_bigrams.structuralCriterian(f'{path}/texts/Y/vigenere/KEY_10_L_10000_N_{n}.log', 66.2))
    print(f'structual Y/vigenere/KEY_10_L_10000: {res.count(True)}')

if __name__ == '__main__':
    main_test()