import unittest

from app.encryption import CipherFactory, EncryptionLevel


class CipherFactoryTests(unittest.TestCase):
    def test_factory_creates_generator_for_each_level(self):
        for level in EncryptionLevel:
            with self.subTest(level=level):
                generator = CipherFactory.create(level)
                self.assertTrue(callable(generator.encrypt))

    def test_each_level_encrypts_text(self):
        for level in EncryptionLevel:
            with self.subTest(level=level):
                ciphertext = CipherFactory.create(level).encrypt(
                    "Meet at 9!"
                )
                self.assertTrue(ciphertext)
                self.assertNotEqual(ciphertext, "Meet at 9!")

    def test_factory_accepts_case_insensitive_level(self):
        self.assertTrue(CipherFactory.create("MEDIUM").encrypt("hello"))

    def test_factory_rejects_unknown_level(self):
        with self.assertRaisesRegex(ValueError, "Unknown encryption level"):
            CipherFactory.create("extreme")

    def test_factory_rejects_empty_level(self):
        with self.assertRaisesRegex(ValueError, "Unknown encryption level"):
            CipherFactory.create("")


if __name__ == "__main__":
    unittest.main()
