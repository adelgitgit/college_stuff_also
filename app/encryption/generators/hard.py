import secrets
import string

from ..ciphers import OneTimePadCipher, PlayfairCipher


class HardCipherGen:
    def encrypt(self, plaintext: str) -> str:
        if secrets.randbelow(2) == 0:
            key = "".join(
                secrets.choice(string.ascii_uppercase)
                for _ in range(8)
            )
            return PlayfairCipher(key).encrypt(plaintext)

        plaintext_bytes = plaintext.encode("utf-8")
        key = secrets.token_bytes(max(1, len(plaintext_bytes))).hex()
        return OneTimePadCipher(key).encrypt(plaintext)
