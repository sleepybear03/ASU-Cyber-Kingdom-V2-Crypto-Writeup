import os
import random
import socketserver

class WeakLFSR:
    def __init__(self, seed_24bit):
        self.state = (0xAA << 24) | (seed_24bit & 0xFFFFFF)
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

def encrypt(plaintext, seed):
    lfsr = WeakLFSR(seed)
    ciphertext = []
    for char in plaintext:
        keystream_byte = lfsr.next_byte()
        ciphertext.append(char ^ keystream_byte)
    return bytes(ciphertext)

class ChallengeHandler(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            # Read flag from local flag.txt file
            flag_path = os.path.join(os.path.dirname(__file__), "flag.txt")
            try:
                with open(flag_path, "rb") as f:
                    flag = f.read().strip()
            except FileNotFoundError:
                flag = b"ASUCK{dummy_flag_for_local_testing}"

            secret_seed = random.randint(1, 0xFFFFFF)
            ctxt = encrypt(flag, secret_seed)

            welcome_msg = (
                "=== The Leaky Sieve CTF Challenge ===\n"
                f"Encrypted Flag (hex): {ctxt.hex()}\n"
            )
            self.request.sendall(welcome_msg.encode())
        except Exception as e:
            print(f"[-] Error handling client: {e}")
        finally:
            self.request.close()

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 1337
    print(f"[+] Server listening on {HOST}:{PORT}...")
    server = ThreadedTCPServer((HOST, PORT), ChallengeHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Shutting down server.")
        server.shutdown()
