import os
import math
import socketserver
from Crypto.Util.number import getPrime, bytes_to_long

def generate_params(flag_bytes):
    while True:
        p = getPrime(1024)
        q = getPrime(1024)
        N = p * q
        
        e1 = 65537
        e2 = 65539
        
        phi = (p - 1) * (q - 1)
        if math.gcd(e1, phi) == 1 and math.gcd(e2, phi) == 1:
            M = bytes_to_long(flag_bytes)
            if M >= N:
                raise ValueError("Flag is too long for 2048-bit modulus N.")
            
            c1 = pow(M, e1, N)
            c2 = pow(M, e2, N)
            return N, e1, c1, e2, c2

class ChallengeHandler(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            flag_path = os.path.join(os.path.dirname(__file__), "flag.txt")
            try:
                with open(flag_path, "rb") as f:
                    flag = f.read().strip()
            except FileNotFoundError:
                flag = b"ASUCK{dummy_flag_for_local_testing}"

            N, e1, c1, e2, c2 = generate_params(flag)

            response = (
                "=== Double Trouble CTF Challenge ===\n"
                f"N = {N}\n"
                f"e1 = {e1}\n"
                f"c1 = {c1}\n"
                f"e2 = {e2}\n"
                f"c2 = {c2}\n"
            )
            self.request.sendall(response.encode())
        except Exception as e:
            print(f"[-] Error handling client: {e}")
        finally:
            self.request.close()

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 8888
    print(f"[+] Double Trouble RSA Server listening on {HOST}:{PORT}...")
    server = ThreadedTCPServer((HOST, PORT), ChallengeHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Shutting down server.")
        server.shutdown()
