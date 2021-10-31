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
    bigrams_frequency = json.loads(read(f'{path}/result/bigrams_frequency.json'))
    criterion = Criterion(bigrams_frequency)
    res = []
    for i in range(1, 1001):
        res.append(criterion.structuralCriterian(f'{path}/texts/X/L_10000_N_{i}', 66.2))
    print(res.count(True))

if __name__ == '__main__':
    main_test()