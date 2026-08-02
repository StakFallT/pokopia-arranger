"""
phrase.py

Detect melodic phrases by linking notes that are likely to belong
to the same musical line.
"""

from __future__ import annotations

from .models import Timeline


def phrase_scores(
    timeline: Timeline,
) -> dict[int, float]:
    """
    Reward notes that continue a nearby melodic line.

    Returns a bonus for each note.
    """

    scores: dict[int, float] = {}

    if not timeline.notes:
        return scores

    previous = None

    for i, note in enumerate(timeline.notes):

        score = 0.0

        if previous is not None:

            #
            # Small melodic intervals are common.
            #
            interval = abs(note.pitch - previous.pitch)

            if interval <= 2:
                score += 30.0

            elif interval <= 5:
                score += 20.0

            elif interval <= 12:
                score += 10.0

            #
            # Notes beginning shortly after the previous note
            # are likely part of the same phrase.
            #
            gap = note.start_tick - previous.end_tick

            if abs(gap) <= timeline.ticks_per_beat // 8:
                score += 20.0

        scores[i] = score

        previous = note

    return scores