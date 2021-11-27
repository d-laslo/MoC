def read(path):
    with open(path, 'r') as file:
        text = file.read()
        return text

def write(path, text):
    with open(path, 'w') as file:
        file.write(text)


def norm(x, pol):
    bx = bin(x)[2:]
    bpol = bin(pol)[2:]

    while len(bx) >= len(bpol):
        shift = len(bx) - len(bpol)
        x ^= pol << shift
        bx = bin(x)[2:]
    return x


def inverse(value, module):
    v = [0, 1]
    rem = 1
    a = module
    value %= module

    while rem > 0:
        tmp = a // value
        v[0] -= (v[1] * tmp) % module
        v[0], v[1] = v[1], v[0]
        rem = a % value
        a = value
        value = rem
    return v[0] % module


if __name__ == '__main__':
    pass