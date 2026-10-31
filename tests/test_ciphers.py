import unittest
from unittest.mock import patch

import numpy as np

from app.encryption.ciphers import (
    AffineCipher,
    AtbashCipher,
    CaesarCipher,
    ColumnarTransposition,
    MonoalphabeticCipher,
    OneTimePadCipher,
    PlayfairCipher,
    RailFenceCipher,
    ROT13Cipher,
    VigenereCipher,
)


class CipherRoundTripTests(unittest.TestCase):
    def test_letter_substitution_ciphers_preserve_case_and_formatting(self):
        plaintext = "Meet at 9, café!"
        ciphers = (
            AtbashCipher(),
            CaesarCipher(7),
            ROT13Cipher(),
            VigenereCipher("LEMON"),
        )

        for cipher in ciphers:
            with self.subTest(cipher=type(cipher).__name__):
                ciphertext = cipher.encrypt(plaintext)
                self.assertEqual(cipher.decrypt(ciphertext), plaintext)

    def test_monoalphabetic_cipher_preserves_case_and_formatting(self):
        with patch(
            "app.encryption.ciphers.mono_alph.random.shuffle",
            side_effect=lambda values: values.reverse(),
        ):
            cipher = MonoalphabeticCipher()

        plaintext = "Abc, XYZ!"
        ciphertext = cipher.encrypt(plaintext)
        self.assertEqual(cipher.decrypt(ciphertext), plaintext)

    def test_affine_cipher_uses_exact_modular_matrix_inverse(self):
        cipher = AffineCipher(
            np.array([[2, 3], [3, 2]]),
            np.array([4, 7]),
        )
        plaintext = "AbCd!"
        ciphertext = cipher.encrypt(plaintext)
        self.assertEqual(cipher.decrypt(ciphertext), plaintext)

    def test_affine_cipher_handles_one_character_blocks(self):
        cipher = AffineCipher(np.array([[5]]), np.array([8]))
        plaintext = "Affine, Z!"
        self.assertEqual(cipher.decrypt(cipher.encrypt(plaintext)), plaintext)

    def test_affine_cipher_pads_incomplete_blocks(self):
        cipher = AffineCipher(np.array([[3, 3], [2, 5]]), np.array([1, 4]))
        ciphertext = cipher.encrypt("CAT")
        self.assertEqual(cipher.decrypt(ciphertext), "CATA")

    def test_affine_cipher_rejects_non_alphabet_modulus(self):
        with self.assertRaisesRegex(ValueError, "mod must be 26"):
            AffineCipher(np.array([[5]]), np.array([8]), mod=29)

    def test_rail_fence_preserves_whitespace_and_punctuation(self):
        cipher = RailFenceCipher(3)
        plaintext = "Meet at 9!"
        self.assertEqual(cipher.decrypt(cipher.encrypt(plaintext)), plaintext)

    def test_columnar_transposition_preserves_ragged_text(self):
        cipher = ColumnarTransposition("3142")
        for plaintext in ("Meet at 9!", "Ends with X", ""):
            with self.subTest(plaintext=plaintext):
                self.assertEqual(cipher.decrypt(cipher.encrypt(plaintext)), plaintext)

    def test_playfair_decrypts_prepared_plaintext_with_fillers(self):
        cipher = PlayfairCipher("MONARCHY")
        ciphertext = cipher.encrypt("Balloon, J!")
        self.assertEqual(cipher.decrypt(ciphertext), "BALXLOONIX")
        self.assertEqual(cipher.decrypt(""), "")

    def test_playfair_rejects_malformed_ciphertext(self):
        cipher = PlayfairCipher("MONARCHY")
        with self.assertRaisesRegex(ValueError, "even number"):
            cipher.decrypt("ABC")

    def test_one_time_pad_round_trips_utf8(self):
        plaintext = "Cipher: café"
        key = bytes(range(len(plaintext.encode("utf-8")))).hex()
        cipher = OneTimePadCipher(key)
        self.assertEqual(cipher.decrypt(cipher.encrypt(plaintext)), plaintext)


if __name__ == "__main__":
    unittest.main()
