"""
scoring.py
"""

from __future__ import annotations

from .config import ArrangeConfig
from .models import NoteEvent


def score_note(
    note: NoteEvent,
    config: ArrangeConfig,
    melody_bonus: float = 0.0,
    bass_bonus: float = 0.0,
    phrase_bonus: float = 0.0,
) -> float:

    score = 0.0

    score += melody_bonus * config.melody_weight
    score += bass_bonus * config.bass_weight
    score += phrase_bonus

    score += note.duration * config.duration_weight
    score += note.pitch * config.pitch_weight

    return score