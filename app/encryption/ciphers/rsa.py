import math
import random


class RSA:

    def __init__(self, p=None, q=None, e=None):

        # Small primes intentionally used for weak RSA
        weak_primes = [
            11, 13, 17, 19, 23,
            29, 31, 37, 41, 43
        ]

        self.p = p or random.choice(weak_primes)

        available = [x for x in weak_primes if x != self.p]
        self.q = q or random.choice(available)

        if self.p == self.q:
            raise ValueError("p and q must be different")

        self.n = self.p * self.q

        self.phi = (self.p - 1) * (self.q - 1)

        self.e = e or 3

        while math.gcd(self.e, self.phi) != 1:
            self.e += 2

        self.d = pow(self.e, -1, self.phi)

        self.public_key = (self.e, self.n)
        self.private_key = (self.d, self.n)

    def encrypt(self, message):

        return [
            pow(ord(char), self.e, self.n)
            for char in message
        ]

    def decrypt(self, ciphertext):

        return ''.join(
            chr(pow(value, self.d, self.n))
            for value in ciphertext
        )

    def get_public_key(self):

        return self.public_key

    def get_ciphertext(self, message):

        return self.encrypt(message)
