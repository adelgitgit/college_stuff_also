import secrets

from math import gcd

import numpy as np

from ..ciphers import (
    AffineCipher,
    AtbashCipher,
    CaesarCipher,
    RailFenceCipher,
    ROT13Cipher,
)


class EasyCipherGen:
    def encrypt(self, plaintext: str) -> str:
        algorithm = secrets.randbelow(5)
        if algorithm == 0:
            return ROT13Cipher().encrypt(plaintext)
        if algorithm == 1:
            return AtbashCipher().encrypt(plaintext)
        if algorithm == 2:
            return CaesarCipher(secrets.randbelow(25) + 1).encrypt(plaintext)
        if algorithm == 3:
            return self._affine(plaintext)
        return RailFenceCipher(secrets.randbelow(3) + 2).encrypt(plaintext)

    @staticmethod
    def _affine(plaintext: str) -> str:
        multipliers = tuple(value for value in range(1, 26) if gcd(value, 26) == 1)
        matrix = np.array([[secrets.choice(multipliers)]], dtype=np.int64)
        vector = np.array([secrets.randbelow(26)], dtype=np.int64)
        return AffineCipher(matrix, vector).encrypt(plaintext)
