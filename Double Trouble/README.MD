# CTF Challenge Writeup: Double Trouble

- **Category:** Cryptography
- **Difficulty:** Medium
- **Focus:** RSA, Common Modulus Attack, Extended Euclidean Algorithm, Bézout's Identity

## 1. Challenge Overview

In **Double Trouble**, we intercept a network transmission containing a master administrative token (the flag) that has been encrypted twice for two different validation endpoints. The fatal flaw identified in the network capture is that **both endpoints share the exact same RSA modulus N**, even though they use different public exponents (e1 and e2).

## 2. Vulnerability Analysis: The RSA Common Modulus Attack

When the same plaintext message M is encrypted under two different public exponents (e1 and e2) using the same modulus N, we obtain two ciphertexts


If the two exponents are coprime—meaning their greatest common divisor is 1 (gcd(e1, e2) = 1) , we can exploit **Bézout's Identity**. This identity guarantees that there exist integers r and s (which can be positive or negative) such that:


Using the Extended Euclidean Algorithm, we can easily calculate these coefficients r and s. Once found, we can reconstruct the original plaintext M directly from the ciphertexts without needing to factor N:


### Handling Negative Coefficients

Because r . e1 + s . e2 = 1 and both e1 , e2 > 0 , one of the coefficients (r or s) must be negative.

If r < 0 , we cannot compute a negative power directly in modular arithmetic. Instead, we rewrite the term using the modular multiplicative inverse of the ciphertext


Since -r is now a positive integer and c1^-1 Mod N is easily computed (provided gcd(c1, N) = 1, which is virtually always true), the attack succeeds cleanly.

## 3. Exploit Script

The solver script below reads the parameters from the challenge, executes the Extended Euclidean Algorithm, handles modular inversion for negative powers, and decodes the recovered integer into the plaintext flag.
