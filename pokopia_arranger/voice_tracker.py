"""
voice_tracker.py

Maintains continuity of selected voices across time.

The goal is to avoid notes rapidly appearing and disappearing
when polyphony changes.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ActiveVoice:
    note_index: int
    score: float