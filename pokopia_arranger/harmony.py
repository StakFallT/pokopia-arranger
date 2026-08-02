"""
harmony.py

Functions for evaluating groups of notes sounding together.
"""

from __future__ import annotations

from .models import NoteEvent


def interval(a: NoteEvent, b: NoteEvent) -> int:
    """
    Return the absolute interval in semitones.
    """

    return abs(a.pitch - b.pitch)


def same_pitch_class(a: NoteEvent, b: NoteEvent) -> bool:
    """
    True if two notes are the same pitch class
    (e.g. C3 and C5).
    """

    return (a.pitch % 12) == (b.pitch % 12)


def harmony_penalty(selected: list[NoteEvent]) -> float:
    """
    Return a penalty for undesirable note combinations.

    Higher penalties indicate a poorer selection.
    """

    penalty = 0.0

    for i in range(len(selected)):

        for j in range(i + 1, len(selected)):

            a = selected[i]
            b = selected[j]

            #
            # Penalize duplicated octaves.
            #
            if same_pitch_class(a, b):
                penalty += 30.0

            #
            # Penalize very close intervals.
            #
            if interval(a, b) <= 1:
                penalty += 20.0

    return penalty