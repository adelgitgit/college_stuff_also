import unittest
from unittest.mock import patch

from app.encryption import EncryptionLevel
from app.game import run_game


class FakeService:
    def __init__(self):
        self.commands = iter(
            [
                ("first command", "First team lead reply"),
                ("second command", "Second team lead reply"),
                ("third command", "Third team lead reply"),
            ]
        )
        self.scores = iter([0.9, 0.2])

    def generate_team_exchange(self):
        return next(self.commands)

    def evaluate_analysis(self, _analysis):
        return next(self.scores)


class CipherGameTests(unittest.TestCase):
    def test_game_tracks_solved_missed_skipped_and_unsolved(self):
        service = FakeService()
        answers = iter(["correct summary", "wrong summary", "/skip"])
        output = []

        with patch("app.game.CipherFactory.create", return_value=IdentityCipher()):
            scoreboard = run_game(
                service=service,
                level=EncryptionLevel.EASY,
                interval_seconds=0,
                show_plaintext=True,
                max_turns=3,
                input_fn=lambda _prompt: next(answers),
                output_fn=output.append,
                sleep_fn=lambda _seconds: None,
            )

        self.assertEqual(scoreboard.solved, 1)
        self.assertEqual(scoreboard.missed, 1)
        self.assertEqual(scoreboard.skipped, 1)
        self.assertEqual(scoreboard.unsolved, 2)
        self.assertTrue(
            any("[DEBUG plaintext] first command" in line for line in output)
        )
        self.assertTrue(any("Unsolved: 2" in line for line in output))
        self.assertTrue(
            any("Team lead: First team lead reply" in line for line in output)
        )

    def test_quitting_marks_current_message_unsolved(self):
        output = []
        with patch("app.game.CipherFactory.create", return_value=IdentityCipher()):
            scoreboard = run_game(
                service=FakeService(),
                level=EncryptionLevel.HARD,
                max_turns=2,
                input_fn=lambda _prompt: "/quit",
                output_fn=output.append,
                sleep_fn=lambda _seconds: None,
            )

        self.assertEqual(scoreboard.skipped, 1)
        self.assertEqual(scoreboard.unsolved, 1)


class IdentityCipher:
    def encrypt(self, plaintext):
        return plaintext


if __name__ == "__main__":
    unittest.main()
