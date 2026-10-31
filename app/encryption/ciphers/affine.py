from math import gcd

import numpy as np


def _determinant(matrix: np.ndarray) -> int:
    if matrix.shape == (0, 0):
        return 1
    if matrix.shape == (1, 1):
        return int(matrix[0, 0])

    determinant = 0
    for column in range(matrix.shape[1]):
        minor = np.delete(np.delete(matrix, 0, axis=0), column, axis=1)
        determinant += (-1) ** column * int(matrix[0, column]) * _determinant(minor)
    return determinant


def _modular_inverse(matrix: np.ndarray, mod: int) -> np.ndarray:
    determinant = _determinant(matrix)
    determinant_inverse = pow(determinant, -1, mod)
    dimension = matrix.shape[0]
    adjugate = np.empty_like(matrix)

    for row in range(dimension):
        for column in range(dimension):
            minor = np.delete(np.delete(matrix, column, axis=0), row, axis=1)
            cofactor = (-1) ** (row + column) * _determinant(minor)
            adjugate[row, column] = cofactor

    return (determinant_inverse * adjugate) % mod


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

        if self.mod != 26:
            raise ValueError("mod must be 26 for the English alphabet")
        if self.matrix.ndim != 2 or self.matrix.shape[0] != self.matrix.shape[1]:
            raise ValueError("matrix must be square")
        if self.matrix.shape[0] == 0:
            raise ValueError("matrix must not be empty")
        if self.matrix.shape[0] != self.vector.shape[0]:
            raise ValueError("matrix and vector dimensions must match")

        self.matrix %= self.mod
        self.vector %= self.mod

        determinant = _determinant(self.matrix) % self.mod
        if gcd(determinant, self.mod) != 1:
            raise ValueError("matrix must be invertible modulo mod")

    def _transform(self, text: str, inverse: bool) -> str:
        letter_positions = [
            index
            for index, char in enumerate(text)
            if char.isascii() and char.isalpha()
        ]
        if not letter_positions:
            return text

        dimension = self.matrix.shape[0]
        values = np.array(
            [ord(text[index].upper()) - ord("A") for index in letter_positions],
            dtype=np.int64,
        )
        remainder = len(values) % dimension
        if remainder:
            values = np.append(values, [0] * (dimension - remainder))

        blocks = values.reshape(-1, dimension)
        if inverse:
            matrix = _modular_inverse(self.matrix, self.mod)
            transformed = (blocks - self.vector) @ matrix.T % self.mod
        else:
            transformed = (blocks @ self.matrix.T + self.vector) % self.mod

        result = list(text)
        for index, value in zip(letter_positions, transformed.flatten()):
            char = chr(int(value) + ord("A"))
            result[index] = char if text[index].isupper() else char.lower()
        result.extend(
            chr(int(value) + ord("A"))
            for value in transformed.flatten()[len(letter_positions):]
        )
        return "".join(result)

    def encrypt(self, plaintext: str) -> str:
        return self._transform(plaintext, inverse=False)

    def decrypt(self, ciphertext: str) -> str:
        return self._transform(ciphertext, inverse=True)
