"""
voice_tracking.py

Helpers for maintaining smooth voice leading between events.
"""

from __future__ import annotations

from .models import NoteEvent


def assign_voices(
    previous: list[NoteEvent],
    current: list[NoteEvent],
) -> list[NoteEvent]:
    """
    Assign current notes to previous voices using nearest pitch.

    This is a greedy algorithm that minimizes pitch movement.
    """

    if not previous:
        return sorted(current, key=lambda n: n.pitch)

    remaining = current[:]
    result: list[NoteEvent] = []

    for old in previous:

        best = min(
            remaining,
            key=lambda n: abs(n.pitch - old.pitch),
        )

        result.append(best)
        remaining.remove(best)

    result.extend(sorted(remaining, key=lambda n: n.pitch))

    return result