
import string
import random

class MonoalphabeticCipher:

    def __init__(self):
        self.alphabet = string.ascii_uppercase

        shuffled = list(self.alphabet)
        random.shuffle(shuffled)

        self.key = dict(zip(self.alphabet, shuffled))

        self.reverse_key = {
            value: key
            for key, value in self.key.items()
        }

    def encrypt(self, plaintext: str) -> str:
        result = []

        for char in plaintext:
            if char.isascii() and char.isalpha():
                mapped = self.key[char.upper()]
                result.append(mapped if char.isupper() else mapped.lower())
            else:
                result.append(char)

        return ''.join(result)

    def decrypt(self, ciphertext: str) -> str:
        result = []

        for char in ciphertext:
            if char.isascii() and char.isalpha():
                mapped = self.reverse_key[char.upper()]
                result.append(mapped if char.isupper() else mapped.lower())
            else:
                result.append(char)

        return ''.join(result)
