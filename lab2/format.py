import re
import os
from source import write, read

path = os.path.dirname(os.path.abspath(__file__))
text_names = ['Putivnyk-po-halaktyci-dlya-kosmoturystiv.txt', 'Pravda.txt']

def format(text):
    return re.sub(r'ґ', 'г', re.sub(r'[\(\)\?\!\-\s\"\',\.\^\\\/\<\#\:\№\&\d\¦A-Za-z;\*\{\}\[\]\$\–\…\>\’\%\«\»]','', text).lower())


if __name__ == '__main__':
    write(
        f'{path}/texts/{"format_text"}', 
        ''.join([format(read(f'{path}/texts/{i}')) for i in text_names])
    )