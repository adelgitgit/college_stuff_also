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

`CipherFactory` creates an easy (ROT13 or Caesar), medium (Vigenere), or high
(affine block) generator. The ciphertext endpoint selects a level at random by
default; pass `?level=easy`, `?level=medium`, or `?level=high` to choose one.

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
