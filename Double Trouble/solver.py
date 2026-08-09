import os
import sys
from Crypto.Util.number import long_to_bytes

def extended_gcd(a, b):
    
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def common_modulus_attack(N, e1, e2, c1, c2):
    
    gcd, r, s = extended_gcd(e1, e2)

    if gcd != 1:
        raise ValueError("Exponents e1 and e2 are not coprime. Attack failed.")

    if r < 0:
        c1 = pow(c1, -1, N)
        r = -r
    if s < 0:
        c2 = pow(c2, -1, N)
        s = -s

    m = (pow(c1, r, N) * pow(c2, s, N)) % N
    return m

def run_solver():
    vars_dict = {}
    with open("challenge_data.txt", "r") as f:
        for line in f:
            if "=" in line:
                key, val = line.split("=")
                vars_dict[key.strip()] = int(val.strip())

    N = vars_dict["N"]
    e1 = vars_dict["e1"]
    c1 = vars_dict["c1"]
    e2 = vars_dict["e2"]
    c2 = vars_dict["c2"]

    print("[*] Performing Extended Euclidean analysis over shared modulus N...")
    message_long = common_modulus_attack(N, e1, e2, c1, c2)

    flag = long_to_bytes(message_long)
    print(f"\n[+] Decrypted Flag successfully:")
    print(flag.decode('utf-8'))

if __name__ == "__main__":
    if not os.path.exists("challenge_data.txt"):
        print("[-] Run 'generate.py' first to produce 'challenge_data.txt'")
    else:
        run_solver()
