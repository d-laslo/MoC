def read(path):
    with open(path, 'r') as file:
        text = file.read()
        return text

def write(path, text):
    with open(path, 'w') as file:
        file.write(text)

if __name__ == '__main__':
    pass