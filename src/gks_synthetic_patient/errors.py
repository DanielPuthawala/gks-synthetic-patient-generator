"""Pipeline exceptions and stable rejection reason codes."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CandidateRejected(ValueError):
    """A source candidate that cannot enter the deterministic pilot pipeline."""

    code: str
    message: str

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"
