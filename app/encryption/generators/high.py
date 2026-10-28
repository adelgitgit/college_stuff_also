import secrets
from math import gcd

import numpy as np

from ..ciphers import AffineCipher


class HighCipherGen:
    def encrypt(self, plaintext: str) -> str:
        matrix = self._random_invertible_matrix()
        vector = np.array(
            [secrets.randbelow(26), secrets.randbelow(26)],
            dtype=np.int64,
        )
        return AffineCipher(matrix, vector).encrypt(plaintext)

    @staticmethod
    def _random_invertible_matrix() -> np.ndarray:
        while True:
            matrix = np.array(
                [
                    [secrets.randbelow(26), secrets.randbelow(26)],
                    [secrets.randbelow(26), secrets.randbelow(26)],
                ],
                dtype=np.int64,
            )
            determinant = int(round(np.linalg.det(matrix))) % 26
            if gcd(determinant, 26) == 1:
                return matrix
