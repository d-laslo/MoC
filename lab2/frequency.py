import os
import json
from source import write, read

path = os.path.dirname(os.path.abspath(__file__))

def  letter_frequency(text):
    letters = list(set(text))
    return {i:text.count(i) for i in letters}

def bigram_frequency(text):
    bigrams_list = [ text[i:i+2] for i in range(len(text) - 1)]
    bigrams = list(set(bigrams_list))
    return {i:bigrams_list.count(i) for i in bigrams}

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
    

    