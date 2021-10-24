import os
import json
from source import write, read

path = os.path.dirname(os.path.abspath(__file__))

# def  letter_frequency(text):
#     letters = list(set(text))
#     return {i:text.count(i) for i in letters}

# def bigram_frequency(text):
#     bigrams_list = [ text[i:i+2] for i in range(len(text) - 1)]
#     bigrams = list(set(bigrams_list))
#     return {i:bigrams_list.count(i) for i in bigrams}

def letter_frequency(text):
    return n_gram_frequency(text, 1)

def bigram_frequency(text):
    return n_gram_frequency(text, 2)

def n_gram_frequency(text, n):
    n_grams_list =  [text[i:i+n] for i in range(len(text) - 1)]
    n_grams = list(set(n_grams_list))
    return {i:n_grams_list.count(i) for i in n_grams}

if __name__ == '__main__':
    text = read(f'{path}/texts/{"format_text"}')

    write(
        f'{path}/result/letter_frequency.json',
        json.dumps(letter_frequency(text))
    )

    write(
        f'{path}/result/bigrams_frequency.json',
        json.dumps(bigram_frequency(text))
    )
    

    