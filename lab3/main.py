import numpy as np
n =  20
e = 65537

t = np.array(np.arange(2**n), dtype=object)
tt = np.exp(t).astype(int)
# t = [i**e for i in range(2**n)]
print("ok")
input()