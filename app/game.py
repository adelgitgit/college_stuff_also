"""Terminal cipher game for the fictional response-team simulation."""

import argparse
import time
from dataclasses import dataclass
from typing import Callable, Protocol

from app.encryption import CipherFactory, EncryptionLevel


@dataclass
class Scoreboard:
    solved: int = 0
    missed: int = 0
    skipped: int = 0

    @property
    def unsolved(self) -> int:
        return self.missed + self.skipped


class GameService(Protocol):
    def generate_team_exchange(self) -> tuple[str, str]: ...

    def evaluate_analysis(self, analysis: str) -> float: ...


def run_game(
    service: GameService,
    level: EncryptionLevel,
    interval_seconds: float = 60,
    show_plaintext: bool = False,
    max_turns: int | None = None,
    pass_threshold: float = 0.6,
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[[str], None] = print,
    sleep_fn: Callable[[float], None] = time.sleep,
) -> Scoreboard:
    scoreboard = Scoreboard()
    turn = 0

    try:
        while max_turns is None or turn < max_turns:
            turn += 1
            plaintext, team_lead_reply = service.generate_team_exchange()
            ciphertext = CipherFactory.create(level).encrypt(plaintext)

            output_fn(f"\n--- Exchange {turn} ---")
            output_fn(f"Encrypted message ({level.value}):")
            output_fn(ciphertext)
            if show_plaintext:
                output_fn(f"[DEBUG plaintext] {plaintext}")

            answer = input_fn(
                "Your interpretation (/skip or /quit): "
            ).strip()
            if answer.lower() == "/quit":
                scoreboard.skipped += 1
                break
            if answer.lower() == "/skip" or not answer:
                scoreboard.skipped += 1
                output_fn("Message skipped; it remains unsolved.")
            else:
                similarity = service.evaluate_analysis(answer)
                if similarity >= pass_threshold:
                    scoreboard.solved += 1
                    output_fn(
                        "Interpretation understood "
                        f"(similarity: {similarity:.2f})."
                    )
                    output_fn(
                        "Sub-leader: Understood. The response team will "
                        "follow the assigned plan and report back."
                    )
                else:
                    scoreboard.missed += 1
                    output_fn(
                        "Interpretation needs work "
                        f"(similarity: {similarity:.2f})."
                    )
                    output_fn(
                        "Sub-leader: We may have misunderstood. Please "
                        "clarify before the team proceeds."
                    )

            output_fn(f"Team lead: {team_lead_reply}")
            output_fn(
                "Score — "
                f"Solved: {scoreboard.solved} | "
                f"Missed: {scoreboard.missed} | "
                f"Skipped: {scoreboard.skipped} | "
                f"Unsolved: {scoreboard.unsolved}"
            )

            if max_turns is not None and turn >= max_turns:
                break
            output_fn(
                f"Next message in {interval_seconds:g} seconds "
                "(Ctrl+C to stop)."
            )
            sleep_fn(interval_seconds)
    except KeyboardInterrupt:
        output_fn("\nGame stopped.")

    output_fn(
        "Final score — "
        f"Solved: {scoreboard.solved} | "
        f"Missed: {scoreboard.missed} | "
        f"Skipped: {scoreboard.skipped} | "
        f"Unsolved: {scoreboard.unsolved}"
    )
    return scoreboard


def _positive_int(value: str) -> int:
    parsed = int(value)
    if parsed < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return parsed


def _non_negative_float(value: str) -> float:
    parsed = float(value)
    if parsed < 0:
        raise argparse.ArgumentTypeError("must be zero or greater")
    return parsed


def _unit_float(value: str) -> float:
    parsed = float(value)
    if not 0 <= parsed <= 1:
        raise argparse.ArgumentTypeError("must be between 0 and 1")
    return parsed


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Play the terminal cipher-message simulation."
    )
    parser.add_argument(
        "--level",
        choices=[level.value for level in EncryptionLevel],
        default=EncryptionLevel.EASY.value,
        help="cipher difficulty (default: easy)",
    )
    parser.add_argument(
        "--interval-seconds",
        type=_non_negative_float,
        default=60,
        help="time between messages (default: 60)",
    )
    parser.add_argument(
        "--show-plaintext",
        action="store_true",
        help="print the original message for testing",
    )
    parser.add_argument(
        "--max-turns",
        type=_positive_int,
        help="stop after this many messages",
    )
    parser.add_argument(
        "--pass-threshold",
        type=_unit_float,
        default=0.6,
        help="minimum semantic similarity to count as solved (default: 0.6)",
    )
    args = parser.parse_args()

    from app.services.ollama_service import OllamaService

    run_game(
        service=OllamaService(),
        level=EncryptionLevel(args.level),
        interval_seconds=args.interval_seconds,
        show_plaintext=args.show_plaintext,
        max_turns=args.max_turns,
        pass_threshold=args.pass_threshold,
    )


if __name__ == "__main__":
    main()
