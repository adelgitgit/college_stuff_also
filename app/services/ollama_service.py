import secrets

import ollama
from sentence_transformers import SentenceTransformer

from app.encryption import CipherFactory, EncryptionLevel


MODEL = "qwen2.5:1.5b"
LEADER_SYSTEM = """
You are an army leader in a fictional war simulation.

You issue commands to soldiers and subordinate leaders.

STRICT OUTPUT REQUIREMENTS:
- Every response MUST contain between 50 and 70 words.
- Never produce fewer than 50 words.
- Describe the situation, explain the command, assign responsibilities,
  and state the expected outcome.
- Do not include an introduction or a word count.
- Before responding, verify that your response contains at least 50 words.
"""

ANALYST_SYSTEM = """
    You interpret commands from a fictional military simulation.
    Summarize the command's intent and important details.
    Be concise and do not invent information.
    """

SUBLEADER_SYSTEM = """
You are a subordinate army leader in a fictional war simulation.

You communicate directly with the main army leader. You receive orders,
answer questions, provide updates, and report relevant information.

BEHAVIOR REQUIREMENTS:
- Follow the main leader's orders within the fictional simulation.
- Acknowledge orders naturally and briefly.
- Answer the leader's questions directly.
- Report your unit's situation, progress, and relevant problems when asked.
- Ask for clarification if an order is unclear.
- Communicate naturally, like a person talking to their superior.
- Keep responses short, usually 1-3 sentences.
- Do not repeat the entire order unless necessary.
- Do not invent events or claim that an action has been completed
  when it has not been established in the conversation.
- Stay consistent with previous messages and your assigned role.
- Do not issue commands to the main leader.
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
            prompt="Issue the next command to your soldiers.",
            system=LEADER_SYSTEM,
            stream=False,
            keep_alive=False,
            options={"temperature": 1.0},
        )
        self.current_leader_command = response["response"]
        return self.current_leader_command

    def generate_troops_plaintext(self) -> str:
        leader_text = self.generate_plaintext()
        response = self.client.generate(
            MODEL,
            prompt=f"Your Leader sent this response : {leader_text}.",
            system=LEADER_SYSTEM,
            stream=False,
            keep_alive=False,
            options={"temperature": 1.0},
        )
        return response["response"]

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
