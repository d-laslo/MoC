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


    #Vigenere distortion
    key1 = dis.uniformlyDistributedSequence(1)#'ж'
    key5 = dis.uniformlyDistributedSequence(5)#'блять'
    key10 = dis.uniformlyDistributedSequence(10)#'йобанийрот'
    keys = [key1,key5,key10]
    for n in range(N[0]):
        text_L10 = read(f'{path}/texts/X/L_10_N_{n+1}')
        text_L100 = read(f'{path}/texts/X/L_100_N_{n+1}')
        text_L1000 = read(f'{path}/texts/X/L_1000_N_{n+1}')
        for key in keys:
            keylen = len(key)
            write(f'{path}/texts/Y/vigenere/KEY_{keylen}_L_10_N_{n+1}',dis.vigenereCipher(text_L10,key))
            write(f'{path}/texts/Y/vigenere/KEY_{keylen}_L_100_N_{n+1}',dis.vigenereCipher(text_L100,key))
            write(f'{path}/texts/Y/vigenere/KEY_{keylen}_L_1000_N_{n+1}',dis.vigenereCipher(text_L1000,key))

    for n in range(N[1]):
        text_L10000 = read(f'{path}/texts/X/L_10000_N_{n+1}')
        for key in keys:
            keylen = len(key)
            write(f'{path}/texts/Y/vigenere/KEY_{keylen}_L_10000_N_{n+1}',dis.vigenereCipher(text_L10000,key))

    #Affine distortion
    a = randint(0,len(letters)-1)
    b = randint(0,len(letters)-1)
    for n in range(N[0]):
        text_L10 = read(f'{path}/texts/X/L_10_N_{n+1}')
        text_L100 = read(f'{path}/texts/X/L_100_N_{n+1}')
        text_L1000 = read(f'{path}/texts/X/L_1000_N_{n+1}')
        #print(dis.affinePermutation("текс",4,5))
        write(f'{path}/texts/Y/affine/L_10_N_{n+1}',dis.affinePermutation(text_L10,a,b))
        write(f'{path}/texts/Y/affine/L_100_N_{n+1}',dis.affinePermutation(text_L100,a,b))
        write(f'{path}/texts/Y/affine/L_1000_N_{n+1}',dis.affinePermutation(text_L1000,a,b))

    for n in range(N[1]):
        text_L10000 = read(f'{path}/texts/X/L_10000_N_{n+1}')
        write(f'{path}/texts/Y/affine/L_10000_N_{n+1}',dis.affinePermutation(text_L10000,a,b))

    #Uniform distortion
    for n in range(N[0]):
        write(f'{path}/texts/Y/uniform/L_10_N_{n+1}',dis.uniformlyDistributedSequence(10))
        write(f'{path}/texts/Y/uniform/L_100_N_{n+1}',dis.uniformlyDistributedSequence(100))
        write(f'{path}/texts/Y/uniform/L_1000_N_{n+1}',dis.uniformlyDistributedSequence(1000))
    
    for n in range(N[1]):
        write(f'{path}/texts/Y/uniform/L_10000_N_{n+1}',dis.uniformlyDistributedSequence(10000))


    #Recursive distortion
    for n in range(N[0]):
        write(f'{path}/texts/Y/recursive/L_10_N_{n+1}',dis.recursiveSequence(10))
        write(f'{path}/texts/Y/recursive/L_100_N_{n+1}',dis.recursiveSequence(100))
        write(f'{path}/texts/Y/recursive/L_1000_N_{n+1}',dis.recursiveSequence(1000))

    for n in range(N[1]):
        text_L10000 = read(f'{path}/texts/X/L_10000_N_{n+1}')
        write(f'{path}/texts/Y/recursive/L_10000_N_{n+1}',dis.recursiveSequence(10000))


if __name__ == '__main__':
    main()