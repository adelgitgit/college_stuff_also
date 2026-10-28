import secrets
import string

from ..ciphers import VigenereCipher


class MediumCipherGen:
    def encrypt(self, plaintext: str) -> str:
        key = "".join(
            secrets.choice(string.ascii_uppercase)
            for _ in range(8)
        )
        return VigenereCipher(key).encrypt(plaintext)
