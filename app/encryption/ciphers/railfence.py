
class RailFenceCipher:

    def __init__(self, key: int):
        if key < 2:
            raise ValueError("Key must be at least 2.")

        self.key = key

    def encrypt(self, plaintext: str) -> str:
        rails = [[] for _ in range(self.key)]

        row = 0
        direction = 1

        for char in plaintext:
            rails[row].append(char)

            if row == 0:
                direction = 1

            elif row == self.key - 1:
                direction = -1

            row += direction

        return ''.join(''.join(rail) for rail in rails)

    def decrypt(self, ciphertext: str) -> str:
        rail_lengths = [0] * self.key
        row = 0
        direction = 1

        for char in ciphertext:
            rail_lengths[row] += 1

            if row == 0:
                direction = 1

            elif row == self.key - 1:
                direction = -1

            row += direction

        index = 0
        rails = []
        for i in range(self.key):
            rails.append(list(ciphertext[index:index + rail_lengths[i]]))
            index += rail_lengths[i]

        plaintext = []
        row = 0
        direction = 1

        for _ in range(len(ciphertext)):
            plaintext.append(rails[row].pop(0))

            if row == 0:
                direction = 1

            elif row == self.key - 1:
                direction = -1

            row += direction

        return ''.join(plaintext)

