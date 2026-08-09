import sys

class ChallengeLFSR:
    def __init__(self, seed_24bit):
        self.state = (0xAA << 24) | seed_24bit
        self.taps = [32, 22, 2, 1]

    def next_bit(self):
        feedback = 0
        for tap in self.taps:
            feedback ^= (self.state >> (32 - tap)) & 1
        output = self.state & 1
        self.state = (self.state >> 1) | (feedback << 31)
        return output

    def next_byte(self):
        byte = 0
        for _ in range(8):
            byte = (byte << 1) | self.next_bit()
        return byte

def brute_force(ciphertext_hex):
    ctxt = bytes.fromhex(ciphertext_hex)
    known_prefix = b"ASUCK{"

    expected_keystream = bytes([ctxt[i] ^ known_prefix[i] for i in range(len(known_prefix))])

    print("[*] Starting brute-force attack over 24-bit seed space...")

    for candidate_seed in range(1, 0x1000000):
        lfsr = ChallengeLFSR(candidate_seed)

        match = True
        for i in range(5):
            if lfsr.next_byte() != expected_keystream[i]:
                match = False
                break

        if match:
            print(f"\n[+] Found correct initialization seed: {candidate_seed}")

            decoder = ChallengeLFSR(candidate_seed)
            plaintext = []
            for byte in ctxt:
                plaintext.append(byte ^ decoder.next_byte())

            print(f"[+] Decrypted Flag: {bytes(plaintext).decode('utf-8')}\n")
            return

    print("[-] Seed not found. Check challenge parameters.")

if __name__ == "__main__":
    with open("ciphertext.txt", "r") as f:
            target_hex = f.read().strip()

brute_force(target_hex)
