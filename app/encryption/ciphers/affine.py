from math import gcd

import numpy as np


class AffineCipher:
    def __init__(
        self,
        matrix: np.ndarray,
        vector: np.ndarray,
        mod: int = 26,
    ):
        self.matrix = np.asarray(matrix, dtype=np.int64)
        self.vector = np.asarray(vector, dtype=np.int64).reshape(-1)
        self.mod = mod

        if self.mod < 2:
            raise ValueError("mod must be at least 2")
        if self.matrix.ndim != 2 or self.matrix.shape[0] != self.matrix.shape[1]:
            raise ValueError("matrix must be square")
        if self.matrix.shape[0] != self.vector.shape[0]:
            raise ValueError("matrix and vector dimensions must match")

        self.matrix %= self.mod
        self.vector %= self.mod

        determinant = int(round(np.linalg.det(self.matrix))) % self.mod
        if gcd(determinant, self.mod) != 1:
            raise ValueError("matrix must be invertible modulo mod")

    def encrypt(self, plaintext: str) -> str:
        letters = [
            char.upper()
            for char in plaintext
            if char.isascii() and char.isalpha()
        ]
        if not letters:
            return ""

        dimension = self.matrix.shape[0]
        values = np.array(
            [ord(char) - ord("A") for char in letters],
            dtype=np.int64,
        )
        remainder = len(values) % dimension
        if remainder:
            values = np.append(values, [0] * (dimension - remainder))

        blocks = values.reshape(-1, dimension)
        encrypted = (blocks @ self.matrix.T + self.vector) % self.mod
        return "".join(
            chr(int(value) + ord("A"))
            for value in encrypted.flatten()
        )
