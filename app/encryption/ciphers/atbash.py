
class AtbashCipher:

    def encrypt(self, text: str) -> str:
        result = []

        for char in text:
            if char.isascii() and char.isalpha():
                start = ord("A") if char.isupper() else ord("a")

                result.append(
                    chr(start + (25 - (ord(char) - start)))
                )
            else:
                result.append(char)

        return "".join(result)

    def decrypt(self, text: str) -> str:
        return self.encrypt(text)