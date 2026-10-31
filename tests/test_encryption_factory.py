import unittest
from unittest.mock import patch

from app.encryption import CipherFactory, EncryptionLevel
from app.encryption.generators.easy import EasyCipherGen
from app.encryption.generators.hard import HardCipherGen
from app.encryption.generators.high import HighCipherGen
from app.encryption.generators.medium import MediumCipherGen


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

    def test_high_level_remains_a_compatibility_alias(self):
        self.assertIsInstance(CipherFactory.create("high"), HardCipherGen)
        self.assertIs(EncryptionLevel.HIGH, EncryptionLevel.HARD)
        self.assertIs(HighCipherGen, HardCipherGen)

    def test_easy_generator_selects_its_ciphers(self):
        with patch("app.encryption.generators.easy.secrets.randbelow", return_value=0):
            self.assertEqual(EasyCipherGen().encrypt("Hello!"), "Uryyb!")
        with patch(
            "app.encryption.generators.easy.secrets.randbelow",
            return_value=1,
        ):
            self.assertEqual(EasyCipherGen().encrypt("Hello!"), "Svool!")
        with patch(
            "app.encryption.generators.easy.secrets.randbelow",
            side_effect=[2, 0],
        ):
            self.assertEqual(EasyCipherGen().encrypt("Hello!"), "Ifmmp!")
        with patch(
            "app.encryption.generators.easy.secrets.randbelow",
            side_effect=[3, 0],
        ), patch(
            "app.encryption.generators.easy.secrets.choice",
            return_value=5,
        ):
            self.assertEqual(EasyCipherGen().encrypt("AB"), "AF")
        with patch(
            "app.encryption.generators.easy.secrets.randbelow",
            side_effect=[4, 0],
        ):
            self.assertEqual(EasyCipherGen().encrypt("HELLO"), "HLOEL")

    def test_medium_generator_selects_its_ciphers(self):
        with patch(
            "app.encryption.generators.medium.secrets.randbelow",
            return_value=0,
        ), patch(
            "app.encryption.generators.medium.secrets.choice",
            return_value="B",
        ):
            self.assertEqual(MediumCipherGen().encrypt("Hello!"), "Ifmmp!")

        with patch(
            "app.encryption.generators.medium.secrets.randbelow",
            return_value=1,
        ), patch(
            "app.encryption.ciphers.mono_alph.random.shuffle",
            side_effect=lambda values: values.reverse(),
        ):
            self.assertEqual(MediumCipherGen().encrypt("HELLO"), "SVOOL")
        with patch(
            "app.encryption.generators.medium.secrets.randbelow",
            return_value=2,
        ), patch(
            "app.encryption.generators.medium.secrets.SystemRandom.sample",
            return_value=list("3120"),
        ):
            self.assertEqual(MediumCipherGen().encrypt("HELLO"), "LELHO")

    def test_hard_generator_encrypts_utf8_as_xor_hex(self):
        with patch(
            "app.encryption.generators.hard.secrets.token_bytes",
            return_value=b"\x00\x00",
        ), patch(
            "app.encryption.generators.hard.secrets.randbelow",
            return_value=1,
        ):
            self.assertEqual(HardCipherGen().encrypt("é"), "C3 A9")

    def test_hard_generator_selects_playfair(self):
        with patch(
            "app.encryption.generators.hard.secrets.randbelow",
            return_value=0,
        ), patch(
            "app.encryption.generators.hard.secrets.choice",
            return_value="A",
        ):
            ciphertext = HardCipherGen().encrypt("HELLO")
        self.assertEqual(len(ciphertext), 6)
        self.assertNotEqual(ciphertext, "HELLO")


if __name__ == "__main__":
    unittest.main()
