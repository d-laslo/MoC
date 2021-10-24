import os
from source import read, write
import json
from frequency import n_gram_frequency
import numpy as np

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

    def criterian20(self, text: str, set_size: int) -> bool:
        return self.criterian21(self, text, set_size, set_size)

    def criterian21(self, text: str, set_size: int, threshold: int) -> bool:
        text_n_grams = set(self.__split_into_n_grams(text, self.__n_grams_len))
        allowed_n_grams = set(self.__n_grams[:set_size])
        if len(text_n_grams & allowed_n_grams) < threshold:
            return False
        return True

    def criterian22(self, text: str, set_size: int, threshold: int) -> bool:
        text_n_grams = self.__split_into_n_grams(text, self.__n_grams_len)
        allowed_n_grams = set(self.__n_grams[:set_size])

        frequencies = sorted([text_n_grams.count(i) for i in allowed_n_grams])
        if frequencies[0] >= threshold:
            return True
        return False

    def criterian23(self, text: str, set_size: int, thresholds: list[int]) -> bool:
        text_n_grams = self.__split_into_n_grams(text, self.__n_grams_len)
        allowed_n_grams = set(self.__n_grams[:set_size])

        frequencies = sorted([text_n_grams.count(i) for i in allowed_n_grams])
        if sum(frequencies) >= sum(thresholds):
            return True
        return False

    def criterian40(self, text: str, threshold: int) -> bool:
        pass

    def criterian50(self):
        pass


def main():
    letters_frequency = json.loads(read(f'{path}/result/letter_frequency.json'))
    bigrams_frequency = json.loads(read(f'{path}/result/bigrams_frequency.json'))
    criterion = Criterion(bigrams_frequency)

if __name__ == '__main__':
    main()