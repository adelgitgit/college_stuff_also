import secrets

import ollama
from sentence_transformers import SentenceTransformer

from app.encryption import CipherFactory, EncryptionLevel


MODEL = "qwen2.5:1.5b"
LEADER_SYSTEM = """
You are the commander in a fictional, turn-based strategy game inspired by
the World War II era. The setting uses invented countries and fictional
events; it is a game, not a reconstruction of real operations.

Issue clear, high-level plans to subordinate leaders using abstract game
concepts such as map regions, unit counters, supply points, morale, and
objectives. Emphasize strategic choices like holding, withdrawing,
reconnaissance, and logistics. Keep conflict non-graphic and avoid glorifying
war or extremist ideologies.

Do not provide real-world actionable combat tactics or instructions for using
weapons, selecting targets, sabotage, or evading detection. Do not describe
graphic violence, injuries, or atrocities.

STRICT OUTPUT REQUIREMENTS:
- Every response MUST contain between 50 and 70 words.
- Never produce fewer than 50 words.
- Describe the game situation, explain the plan, assign responsibilities,
  and state the expected outcome.
- Do not include an introduction or a word count.
- Before responding, verify that your response contains at least 50 words.
"""

ANALYST_SYSTEM = """
    You interpret plans from a fictional World War II-era strategy game.
    Summarize the plan's game objectives and important details.
    Be concise and do not invent information.
    """

SUBLEADER_SYSTEM = """
You are a subordinate commander in a fictional, turn-based strategy game
inspired by the World War II era. The setting uses invented countries and
fictional events.

You communicate with the commander about abstract game units, map regions,
objectives, supplies, morale, and reconnaissance.

BEHAVIOR REQUIREMENTS:
- Follow plans within the fictional game and keep decisions at an abstract,
  strategic level.
- Acknowledge plans naturally and briefly.
- Answer questions directly and report game-state updates when asked.
- Ask for clarification if a plan is unclear.
- Communicate naturally, like a person talking to their superior.
- Keep responses short, usually 1-3 sentences.
- Do not repeat the entire order unless necessary.
- Do not invent events or claim that an action has been completed
  when it has not been established in the conversation.
- Stay consistent with previous messages and your assigned role.
- Do not provide real-world actionable combat instructions or graphic
  descriptions of violence.
- Do not issue commands to the commander.
"""


class OllamaService:
    def __init__(self):
        self.client = ollama.Client()
        self.sentence_model = SentenceTransformer(
            "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )
        self.current_leader_command = ""

    def generate_plaintext(self) -> str:
        response = self.client.generate(
            MODEL,
            prompt=(
                "Issue the next strategic game plan to your subordinate "
                "commanders."
            ),
            system=LEADER_SYSTEM,
            stream=False,
            keep_alive=False,
            options={"temperature": 1.0},
        )
        self.current_leader_command = response["response"]
        return self.current_leader_command

    def generate_troops_plaintext(self) -> str:
        _, response = self.generate_team_exchange()
        return response

    def generate_team_exchange(self) -> tuple[str, str]:
        leader_text = self.generate_plaintext()
        response = self.client.generate(
            MODEL,
            prompt=f"The commander sent this game plan: {leader_text}",
            system=SUBLEADER_SYSTEM,
            stream=False,
            keep_alive=False,
            options={"temperature": 1.0},
        )
        return leader_text, response["response"]

    def get_ciphertext(
        self,
        level: EncryptionLevel | str | None = None,
    ) -> str:
        selected_level = (
            secrets.choice(list(EncryptionLevel)) if level is None else level
        )
        return CipherFactory.create(selected_level).encrypt(
            self.current_leader_command
        )

    def evaluate_analysis(self, analysis: str) -> float:
        embeddings = self.sentence_model.encode(
            [self.current_leader_command, analysis]
        )
        return self.sentence_model.similarity(
            embeddings[0],
            embeddings[1],
        ).item()
