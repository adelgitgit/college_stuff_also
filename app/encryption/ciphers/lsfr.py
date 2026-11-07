import random


class LFSR:
    """
    Linear Feedback Shift Register cipher.

    Educational stream cipher for cryptography game.
    """

    def __init__(self, register_size=8, taps=None, seed=None):

        self.register_size = register_size

        # Default feedback configuration
        self.taps = taps if taps is not None else [0, 2, 3, 4]

        self.mask = (1 << register_size) - 1

        # Generate initial state
        self.seed = (
            seed if seed is not None
            else random.randint(1, self.mask)
        )

        if not 1 <= self.seed <= self.mask:
            raise ValueError("Invalid LFSR seed")

        if any(t < 0 or t >= register_size for t in self.taps):
            raise ValueError("Invalid feedback tap position")

        if not self.taps:
            raise ValueError("At least one feedback tap is required")

    def _generate_bit(self, state):
        """
        Generate one output bit and update register state.
        """

        output = state & 1

        feedback = 0

        for tap in self.taps:
            feedback ^= (state >> tap) & 1

        state = (state >> 1) | (
            feedback << (self.register_size - 1)
        )

        return output, state

    def generate_keystream(self, length, seed=None):

        state = self.seed if seed is None else seed

        if not 1 <= state <= self.mask:
            raise ValueError("Invalid LFSR state")

        keystream = []

        for _ in range(length):

            bit, state = self._generate_bit(state)

            keystream.append(bit)

        return keystream

    def encrypt(self, plaintext):

        plaintext_bits = []

        for char in plaintext:

            bits = format(ord(char), "08b")

            plaintext_bits.extend(
                int(bit) for bit in bits
            )

        keystream = self.generate_keystream(
            len(plaintext_bits)
        )

        ciphertext = [
            p ^ k
            for p, k in zip(plaintext_bits, keystream)
        ]

        return ciphertext

    def decrypt(self, ciphertext):

        keystream = self.generate_keystream(
            len(ciphertext)
        )

        plaintext_bits = [
            c ^ k
            for c, k in zip(ciphertext, keystream)
        ]

        plaintext = []

        for i in range(0, len(plaintext_bits), 8):

            byte = plaintext_bits[i:i + 8]

            if len(byte) < 8:
                break

            value = int(
                "".join(map(str, byte)), 2
            )

            plaintext.append(chr(value))

        return "".join(plaintext)

    def get_public_information(self):

        """
        Information available to the player.
        The initial seed remains secret.
        """

        return {
            "algorithm": "LFSR",
            "register_size": self.register_size,
            "feedback_taps": self.taps,
        }

    def get_ciphertext(self, plaintext):

        return self.encrypt(plaintext)
