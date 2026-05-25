from base64 import b64decode
import re

CIPHERS = [
    "cx4jeE13FgUyYh4yIR8yNk0xLgwwYgQkYi4eFkBmJgtnJloxJ1gydVRicA42JltnIQg0J181I19idA41dFhmJF9ic1xlIQlhe10xJ1s2c11vdVVmJFVlcgljcwwy",
    "cAMzeE13ASQDb1RjdVgxe1VudVliI1tiIwtjJw5hcV9jclk2Jl0zdw8zdQgxdw41dQk2dVxicFphdVtlJlRidwhvdFUyelk0IA93Kx53NgUyYh4yIR8yNk0xLgww",
]

TARGET = b"CIT"
FLAG_REGEX = re.compile(rb"CIT-[0-9a-f]{64}")

def decrypt(cipher_bytes, key):
    return bytes(
        byte ^ key[i % len(key)]
        for i, byte in enumerate(cipher_bytes)
    )

def find_key(cipher_bytes):
    # try each possible location where "CIT" could appear
    for offset in range(len(cipher_bytes) - len(TARGET) + 1):
        key = bytearray(3)

        # recover the repeating XOR key from the known plaintext fragment
        for i in range(len(TARGET)):
            key[(offset + i) % 3] = cipher_bytes[offset + i] ^ TARGET[i]

        plaintext = decrypt(cipher_bytes, key)

        if FLAG_REGEX.search(plaintext):
            return bytes(key), plaintext

    return None, None

def main():
    for cipher in CIPHERS:
        cipher_bytes = b64decode(cipher)
        key, plaintext = find_key(cipher_bytes)
        print("\nKey:", key.decode())
        print(plaintext.decode("utf-8", errors="replace"))

if __name__ == "__main__":
    main()