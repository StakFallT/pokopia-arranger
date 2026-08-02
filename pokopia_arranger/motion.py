"""
motion.py

Analyze which notes are part of moving lines.

Notes that change pitch from one event to the next are generally
more musically important than repeated pedal tones.
"""

from __future__ import annotations

from .models import Timeline


def motion_scores(timeline: Timeline) -> dict[int, float]:
    """
    Assign a motion score to each note.

    A note receives a higher score if another note on the same track
    and channel recently occurred at a different pitch.
    """

    scores: dict[int, float] = {}

    previous_note = {}

    #
    # Notes are already sorted by start time.
    #
    for index, note in enumerate(timeline.notes):

        key = (note.track, note.channel)

        score = 0.0

        if key in previous_note:

            previous = previous_note[key]

            interval = abs(note.pitch - previous.pitch)

            if interval == 0:
                score = -10.0

            elif interval <= 2:
                score = 25.0

            elif interval <= 5:
                score = 20.0

            elif interval <= 12:
                score = 15.0

            else:
                score = 5.0

        scores[index] = score

        previous_note[key] = note

    return scores