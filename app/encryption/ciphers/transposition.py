

import math


class ColumnarTransposition:

    def __init__(self, key: str):
        if not key.isdigit() or len(set(key)) != len(key):
            raise ValueError("Key must contain unique digits.")

        self.key = key

    def encrypt(self, plaintext: str) -> str:
        columns = len(self.key)
        rows = math.ceil(len(plaintext) / columns)

        matrix = [
            plaintext[i:i + columns]
            for i in range(0, len(plaintext), columns)
        ]

        ciphertext = []

        for col in sorted(range(columns), key=lambda i: int(self.key[i])):
            for row in matrix:
                if col < len(row):
                    ciphertext.append(row[col])

        return ''.join(ciphertext)

    def decrypt(self, ciphertext: str) -> str:
        columns = len(self.key)
        rows, remainder = divmod(len(ciphertext), columns)
        column_lengths = [
            rows + (1 if col < remainder else 0)
            for col in range(columns)
        ]
        matrix = [[] for _ in range(columns)]

        index = 0
        for col in sorted(range(columns), key=lambda i: int(self.key[i])):
            length = column_lengths[col]
            matrix[col] = list(ciphertext[index:index + length])
            index += length

        plaintext = []
        for row in range(rows + (1 if remainder else 0)):
            for col in range(columns):
                if row < column_lengths[col]:
                    plaintext.append(matrix[col][row])
        return ''.join(plaintext)

