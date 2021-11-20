import os
import json
from source import read, write


path = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    letters_frequency = json.loads(read(f'{path}/result/letter_frequency.json'))
    bigrams_frequency =  json.loads(read(f'{path}/result/bigrams_frequency.json'))
    sorted_letters_decrease = sorted(letters_frequency.items(),key=lambda x: x[1],reverse=True)
    sorted_letters_increase = sorted(letters_frequency.items(),key=lambda x: x[1],reverse=False)
    sorted_bigrams_decrease = sorted(bigrams_frequency.items(),key=lambda x: x[1],reverse=True)
    sorted_bigrams_increase = sorted(bigrams_frequency.items(),key=lambda x: x[1],reverse=False)
    print("Часті символи:")
    for i in sorted_letters_decrease[:10]:
        print(i)
    print("Заборонені символи:")
    for i in sorted_letters_increase[:10]:
        print(i)
    print("============")
    print("Часті біграми:")
    for i in sorted_bigrams_decrease[:10]:
        print(i)
    print("Заборонені біграми:")
    for i in sorted_bigrams_increase[:10]:
        print(i)