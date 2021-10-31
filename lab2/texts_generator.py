import os
import random as rd
from source import write, read

path = os.path.dirname(os.path.abspath(__file__))

L = [10, 100, 1000, 10000]
N = [10000, 1000]

def generate_text(text, text_len):
    length = len(text)
    if text_len > length:
        raise Exception('')
    start = rd.randint(0, length - text_len)
    return text[start: start + text_len]

def generate_texts(text, text_len, num):
    return [generate_text(text, text_len) for i in range(num)]

def write_new_texts(text, L, N):
    texts = generate_texts(text, L, N)
    for i in range(N):
        write(f'{path}/texts/X/L_{L}_N_{i+1}', texts[i])
    
def generate_text_with_one_symbol(symbol,length_of_symbols):
    return symbol * length_of_symbols

if __name__ == '__main__':
    text = read(f'{path}/texts/format_text')

    for l in L[:-1]:
        write_new_texts(text, l, N[0])
    
    write_new_texts(text, L[-1], N[-1])

    # генеруємо і записуємо купу символів "ааааа..." в файл nosense_text
    write(f'{path}/texts/nosence_text',generate_text_with_one_symbol('a',L[-1]))
