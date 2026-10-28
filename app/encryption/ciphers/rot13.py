class ROT13Cipher:
    def encrypt(self, text: str) -> str:
        encrypted = []

        for char in text:
            if char.isascii() and char.isalpha():
                base = ord("A") if char.isupper() else ord("a")
                encrypted.append(
                    chr((ord(char) - base + 13) % 26 + base)
                )
            else:
                encrypted.append(char)

        return "".join(encrypted)
