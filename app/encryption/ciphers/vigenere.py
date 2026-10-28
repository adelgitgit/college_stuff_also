class VigenereCipher:
    def __init__(self, key: str):
        if not key or not key.isascii() or not key.isalpha():
            raise ValueError("Vigenere key must contain ASCII letters only")
        self.key = key.upper()

    def encrypt(self, plaintext: str) -> str:
        ciphertext = []
        key_position = 0

        for char in plaintext:
            if char.isascii() and char.isalpha():
                base = ord("A") if char.isupper() else ord("a")
                plain_value = ord(char) - base
                key_value = ord(self.key[key_position % len(self.key)]) - ord("A")
                ciphertext.append(
                    chr((plain_value + key_value) % 26 + base)
                )
                key_position += 1
            else:
                ciphertext.append(char)

        return "".join(ciphertext)
