import secrets
import string

from ..ciphers import ColumnarTransposition, MonoalphabeticCipher, VigenereCipher


class MediumCipherGen:
    def encrypt(self, plaintext: str) -> str:
        algorithm = secrets.randbelow(3)
        if algorithm == 0:
            return self._vigenere(plaintext)
        if algorithm == 1:
            return MonoalphabeticCipher().encrypt(plaintext)
        key = "".join(secrets.SystemRandom().sample("0123456789", 4))
        return ColumnarTransposition(key).encrypt(plaintext)

    @staticmethod
    def _vigenere(plaintext: str) -> str:
        key = "".join(
            secrets.choice(string.ascii_uppercase)
            for _ in range(8)
        )
        return VigenereCipher(key).encrypt(plaintext)
