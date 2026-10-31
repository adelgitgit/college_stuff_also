class CaesarCipher:
    def __init__(self, shift: int):
        self.shift = shift % 26

    def encrypt(self, text: str) -> str:
        result = []

        for char in text:
            if char.isascii() and char.isalpha():
                start = ord("A") if char.isupper() else ord("a")
                result.append(
                    chr(start + (ord(char) - start + self.shift) % 26)
                )
            else:
                result.append(char)

        return "".join(result)

    def decrypt(self, text: str) -> str:
        result = []

        for char in text:
            if char.isascii() and char.isalpha():
                start = ord("A") if char.isupper() else ord("a")
                result.append(
                    chr(start + (ord(char) - start - self.shift) % 26)
                )
            else:
                result.append(char)

        return "".join(result)
