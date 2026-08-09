# CTF Challenge Writeup: The Leaky Sieve

- **Category:** Cryptography
- **Difficulty:** Easy
- **Focus:** LFSR (Linear Feedback Shift Register), Key Space Reduction, Known Plaintext Attack (KPA)

## 1. Challenge Overview

The challenge presents us with a customized stream cipher based on a 32-bit Linear Feedback Shift Register (LFSR). We are provided with a ciphertext file (`ciphertext.txt`) and the source code used to generate it. The goal is to crack the cipher and decrypt the flag.
## 2. Vulnerability Analysis

The developers claimed that because the feedback polynomial is mathematically optimal, the cipher is unbreakable. However, two fatal security implementation flaws completely undermine this claim:

### a. Hardcoded State Bits (Entropy Reduction)

The LFSR is 32 bits wide, which normally suggests a key space of 2^32 = 4.29 * 10^9 possibilities , not impossible to brute force, but slightly time-consuming in pure Python.

However, looking at the constructor of `WeakLFSR` in `generate.py`:

self.state = (0xAA << 24) | (seed_24bit & 0xFFFFFF)

The top 8 bits of the initial state are hardcoded to 0xAA (10101010 in binary). The user input seed only populates the lower 24 bits. This reduces the active search space to:
2^24 = 16,777,216

A search space of ~16.7 million keys is extremely small and can be entirely exhausted in less than a minute in standard Python.

### b. Known Plaintext Prefix (Known Plaintext Attack)

We know that the plaintext starts with the standard flag format: `ASUCK{`.

Because a stream cipher encrypts by performing a bitwise XOR  between the plaintext (P) and the keystream (K), we can easily reconstruct the first 6 bytes of the expected keystream

Using this known prefix, we can test candidate seeds. If a candidate seed generates a keystream that matches the expected keystream for the first 5 or 6 bytes, we have found our true seed.

## 3. Exploit Strategy

1. **Read Ciphertext:** Parse the hex-encoded ciphertext from `ciphertext.txt`.
2. **Derive Target Keystream:** XOR the first 6 bytes of the ciphertext with the ASCII bytes of `ASUCK{`.
3. **Exhaustive Search:** Loop the candidate seed space from $1$ to $0xFFFFFF$ ($2^{24}-1$):
    - Initialize the LFSR state with `(0xAA << 24) | candidate_seed`.
    - Generate the first 5 bytes of keystream.
    - Compare them with our derived target keystream.
4. **Decrypt:** Once a matching seed is found, re-initialize the generator and decrypt the entire ciphertext.
