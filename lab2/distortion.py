import os
from source import read, write
from numpy.random import randint
import numpy as np
path = os.path.dirname(os.path.abspath(__file__))

L = [10, 100, 1000, 10000]
N = [10000, 1000]

letters = ['а','б','в','г','д','е','є','ж','з','и','і','ї','й','к','л','м','н','о','п','р','с','т','у','ф','х','ц','ч','ш','щ','ь','ю','я']


class Distortor:

    def __init__(self, alphabet):
        self.__alphabet_len = len(alphabet)
        self.__letter_number = {alphabet[i]: i for i in range(self.__alphabet_len)}
        self.__number_letter = {self.__letter_number[i]:i for i in self.__letter_number}

    def __code(self, text):
        return [self.__letter_number[i] for i in text]

    def __decode(self, text):
        return ''.join([self.__number_letter[i] for i in text])

    def vigenereCipher(self, text, key):
        ctext = np.array(self.__code(text))
        ckey = np.array(self.__code(key))
        if len(ckey) == 0:
            ckey = [0]
        length = len(ckey)

        crypto = []
        if (length <= len(text)):
            crypto = np.concatenate([
                (ctext[i * length : (i + 1) * length] + ckey) % self.__alphabet_len
                for i in range(int(len(text) / length))
            ])

        remainder = len(text) % length
        crypto = np.concatenate([
            crypto,
            (ctext[len(text) - remainder:] + ckey[:remainder]) % self.__alphabet_len
        ])

        return self.__decode(list(crypto))


    def affinePermutation(self, text, a, b):
        if a == 0:
            raise Exception('')
        if a == 1 and b == 0:
            return text

        ctext = np.array(self.__code(text))
        crypto = (ctext * a + b) % self.__alphabet_len
        return self.__decode(list(crypto))


    def uniformlyDistributedSequence(self, text_len):
        if text_len == 0:
            raise Exception('')

        crypto = randint(0, self.__alphabet_len - 1, text_len)
        return self.__decode(list(crypto))


    def recursiveSequence(self, text_len):
        if text_len == 0:
            raise Exception('')
        
        crypto = list(randint(0, self.__alphabet_len - 1, 2))
        for i in range(text_len - 2):
            crypto.append( (crypto[-1] + crypto[-2]) % self.__alphabet_len)
        return self.__decode(list(crypto))


def main():
    dis = Distortor(letters)

    # text = read(f'{path}/texts/X/L_10_N_1')
    res = dis.uniformlyDistributedSequence(50)
    # print(text)
    print(res)


if __name__ == '__main__':
    main()