
class OneTimePadCipher:
    def __init__(self, key: str):
        clean_key = key.replace(" ", "")
        if not clean_key or len(clean_key) % 2 != 0:
            raise ValueError("OTP key must be a valid non-empty hex string")
        self.key = [int(clean_key[i:i + 2], 16) for i in range(0, len(clean_key), 2)]

    def encrypt(self, plaintext: str) -> str:
        plaintext_bytes = plaintext.encode("utf-8")
        if len(self.key) < len(plaintext_bytes):
            raise ValueError("Key must be at least as long as the plaintext")

        return " ".join(
            f"{plain_byte ^ key_byte:02X}"
            for plain_byte, key_byte in zip(plaintext_bytes, self.key)
        )

    def decrypt(self, ciphertext: str) -> str:
        cipher_bytes = bytes(int(byte, 16) for byte in ciphertext.split())
        if len(self.key) < len(cipher_bytes):
            raise ValueError("Key must be at least as long as the ciphertext")

        decrypted_bytes = bytes(
            cipher_byte ^ key_byte
            for cipher_byte, key_byte in zip(cipher_bytes, self.key)
        )
        return decrypted_bytes.decode("utf-8")
