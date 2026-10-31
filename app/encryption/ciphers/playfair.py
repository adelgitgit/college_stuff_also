
class PlayfairCipher:

    def __init__(self, key: str):
        if not key.isascii() or not key.isalpha():
            raise ValueError("Playfair key must contain ASCII letters only")
        self.key = key.upper().replace("J", "I")
        self.matrix = self._generate_matrix()

        self.positions = {
            char: (row, col)
            for row, values in enumerate(self.matrix)
            for col, char in enumerate(values)
        }

    def _generate_matrix(self):
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        key_chars = list(dict.fromkeys(self.key))
        key_chars.extend(char for char in alphabet if char not in key_chars)

        return [
            key_chars[i:i + 5]
            for i in range(0, 25, 5)
        ]

    def _prepare_text(self, plaintext: str):
        if not plaintext.isascii():
            raise ValueError("Playfair text must contain ASCII letters only")
        plaintext = ''.join(
            char for char in plaintext.upper() if char.isalpha()
        ).replace("J", "I")

        pairs = []
        i = 0

        while i < len(plaintext):
            first = plaintext[i]
            if i + 1 >= len(plaintext):
                second = "X"
                i += 1
            elif plaintext[i] == plaintext[i + 1]:
                second = "Q" if first == "X" else "X"
                i += 1
            else:
                second = plaintext[i + 1]
                i += 2

            pairs.append((first, second))

        return pairs

    def encrypt(self, plaintext: str) -> str:
        pairs = self._prepare_text(plaintext)
        ciphertext = []

        for first, second in pairs:
            r1, c1 = self.positions[first]
            r2, c2 = self.positions[second]

            if r1 == r2:
                ciphertext.append(self.matrix[r1][(c1 + 1) % 5])
                ciphertext.append(self.matrix[r2][(c2 + 1) % 5])
            elif c1 == c2:
                ciphertext.append(self.matrix[(r1 + 1) % 5][c1])
                ciphertext.append(self.matrix[(r2 + 1) % 5][c2])
            else:
                ciphertext.append(self.matrix[r1][c2])
                ciphertext.append(self.matrix[r2][c1])

        return ''.join(ciphertext)

    def decrypt(self, ciphertext: str) -> str:
        if not ciphertext.isascii() or (ciphertext and not ciphertext.isalpha()):
            raise ValueError("Playfair ciphertext must contain ASCII letters only")
        if len(ciphertext) % 2:
            raise ValueError("Playfair ciphertext must have an even number of letters")

        ciphertext = ciphertext.upper().replace("J", "I")
        plaintext = []

        for index in range(0, len(ciphertext), 2):
            first, second = ciphertext[index:index + 2]
            r1, c1 = self.positions[first]
            r2, c2 = self.positions[second]

            if r1 == r2:
                plaintext.append(self.matrix[r1][(c1 - 1) % 5])
                plaintext.append(self.matrix[r2][(c2 - 1) % 5])
            elif c1 == c2:
                plaintext.append(self.matrix[(r1 - 1) % 5][c1])
                plaintext.append(self.matrix[(r2 - 1) % 5][c2])
            else:
                plaintext.append(self.matrix[r1][c2])
                plaintext.append(self.matrix[r2][c1])

        return ''.join(plaintext)
