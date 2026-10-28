from enum import Enum
from typing import TypeAlias

from .easy import EasyCipherGen
from .high import HighCipherGen
from .medium import MediumCipherGen


class EncryptionLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HIGH = "high"


CipherGenerator: TypeAlias = EasyCipherGen | MediumCipherGen | HighCipherGen


class CipherFactory:
    _generators = {
        EncryptionLevel.EASY: EasyCipherGen,
        EncryptionLevel.MEDIUM: MediumCipherGen,
        EncryptionLevel.HIGH: HighCipherGen,
    }

    @classmethod
    def create(cls, level: EncryptionLevel | str) -> CipherGenerator:
        if isinstance(level, EncryptionLevel):
            normalized_level = level
        elif isinstance(level, str):
            try:
                normalized_level = EncryptionLevel(level.strip().lower())
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
