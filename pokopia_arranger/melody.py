"""
melody.py

Melody analysis.

This module attempts to identify notes that are likely to belong
to the principal melodic line. It does not make arranging
decisions—it only analyzes the music.
"""

from __future__ import annotations
from dataclasses import dataclass
from .models import Timeline


@dataclass(slots=True)
class MelodyAnalysis:
    """
    Analysis results for a single note.
    """

    probability: float

    highest: bool

    sustained: bool

    on_beat: bool


def analyze_melody(
    timeline: Timeline,
) -> dict[int, MelodyAnalysis]:
    """
    Analyze the likelihood that each note belongs to the melody.

    Returns
    -------
    dict
        Maps note index to MelodyAnalysis.
    """

    results: dict[int, MelodyAnalysis] = {}

    if not timeline.notes:
        return results

    highest_pitch = max(note.pitch for note in timeline.notes)
    beat = timeline.ticks_per_beat

    for i, note in enumerate(timeline.notes):

        probability = 0.0
        highest = note.pitch >= highest_pitch - 12

        if highest:
            probability += 0.40

        sustained = note.duration >= beat

        if sustained:
            probability += 0.30

        on_beat = (note.start_tick % beat) == 0

        if on_beat:
            probability += 0.30

        results[i] = MelodyAnalysis(
            probability=min(probability, 1.0),
            highest=highest,
            sustained=sustained,
            on_beat=on_beat,
        )

    return results