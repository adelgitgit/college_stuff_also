from enum import Enum
from typing import TypeAlias

from .easy import EasyCipherGen
from .hard import HardCipherGen
from .medium import MediumCipherGen


class EncryptionLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    HIGH = "hard"


CipherGenerator: TypeAlias = EasyCipherGen | MediumCipherGen | HardCipherGen


class CipherFactory:
    _generators = {
        EncryptionLevel.EASY: EasyCipherGen,
        EncryptionLevel.MEDIUM: MediumCipherGen,
        EncryptionLevel.HARD: HardCipherGen,
    }

    @classmethod
    def create(cls, level: EncryptionLevel | str) -> CipherGenerator:
        if isinstance(level, EncryptionLevel):
            normalized_level = level
        elif isinstance(level, str):
            try:
                level_name = level.strip().lower()
                if level_name == "high":
                    level_name = EncryptionLevel.HARD.value
                normalized_level = EncryptionLevel(level_name)
            except ValueError as error:
                supported = ", ".join(item.value for item in EncryptionLevel)
                raise ValueError(
                    f"Unknown encryption level {level!r}; "
                    f"choose from: {supported}"
                ) from error
        else:
            supported = ", ".join(item.value for item in EncryptionLevel)
            raise ValueError(
                f"Unknown encryption level {level!r}; choose from: {supported}"
            )

        return cls._generators[normalized_level]()
