import secrets

from ..ciphers import CaesarCipher, ROT13Cipher


class EasyCipherGen:
    def encrypt(self, plaintext: str) -> str:
        if secrets.randbelow(2) == 0:
            return ROT13Cipher().encrypt(plaintext)
        return CaesarCipher(secrets.randbelow(25) + 1).encrypt(plaintext)
