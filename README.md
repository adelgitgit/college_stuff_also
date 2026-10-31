# Encryption Simulation

A small FastAPI application that generates fictional simulation commands with
Ollama and offers three levels of educational text ciphers.

> These classical ciphers are for learning and simulation only. They are not
> suitable for protecting sensitive information.

## Project layout

```text
app/
  api.py
  encryption/
    ciphers/
    generators/
  services/
    ollama_service.py
backend.py
tests/
```

`CipherFactory` creates generators from these difficulty groups:

- **Easy:** Caesar, Atbash, ROT13, Affine, and Rail Fence
- **Medium:** Monoalphabetic Substitution, Columnar Transposition, and
  Vigenere
- **Hard:** Playfair and XOR

XOR uses a fresh random one-time key for each message; these ciphers are
educational demonstrations, not secure messaging.

The reversible letter and transposition ciphers preserve the input's case,
spaces, and punctuation. Affine ciphers with blocks larger than one append
`A` when the final block is incomplete; Playfair strips non-letters, maps `J`
to `I`, and uses `X` (or `Q` after `X`) as a filler. Decryption of those
block-based ciphers returns the normalized/padded plaintext, since the original
formatting and filler characters cannot be inferred from ciphertext alone.
The ciphertext endpoint selects a level at random by default; pass
`?level=easy`, `?level=medium`, or `?level=hard` to choose one. The former
`?level=high` value remains accepted as an alias for `hard`.

## Play the terminal game

The terminal game sends a new encrypted commander message every minute.
Enter your interpretation to have it scored against the original message; use
`/skip` to leave a message unsolved or `/quit` to end the game. The scoreboard
tracks solved, missed, skipped, and total unsolved messages. The setting is a
fictional, World War II-inspired strategy game with abstract, non-graphic
decisions; it does not provide real-world combat instructions. The score is a
semantic similarity estimate for the whole message, not a reliable detector
of contradictions or individual missed details.

```bash
python -m app.game --level easy
```

For testing, `--show-plaintext` displays the original message. Useful options:

```text
--level easy|medium|hard       Cipher difficulty (default: easy)
--interval-seconds 60          Seconds between messages
--max-turns 5                  Stop after a fixed number of messages
--pass-threshold 0.6           Similarity required to mark a message solved
--show-plaintext               Show plaintext for testing
```

Run a short test session with:

```bash
python -m app.game --level easy --show-plaintext --interval-seconds 0 --max-turns 2
```

## Run

Install the packages listed in `requirements.txt`, make sure Ollama is running
with the `qwen2.5:1.5b` model available, then start the API:

```bash
uvicorn backend:app --reload
```

## Test

```bash
python -m unittest discover -s tests
```
