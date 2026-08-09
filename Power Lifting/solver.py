from gmpy2 import next_prime, gcd, is_prime
from Crypto.Util.number import *

exp1= 
exp2=
hint=
output2=
ciphertext=
n=
e = hint

x1 = pow(2, exp1*exp2, n)
x2 = pow(output2, exp1, n)
for i in range(10000):
    # if i % 100 == 0: print(i)
    diff = abs(pow(hint, exp2, n)*x1 - x2)
    q = gcd(diff, n)
    if q > 1:
        # print(g)
        break
    eq1 -= 1
    if is_prime(eq1):
        break
    
p = n//q
assert p*q == n
phi = (p - 1)*(q - 1)
# d = inverse(e, n)
d = pow(e, -1, phi)
print(long_to_bytes(pow(ciphertext, d, n)))
