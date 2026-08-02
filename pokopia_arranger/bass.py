"""
bass.py

Bass candidate detection.

This module assigns a bonus to notes that are likely to serve
as the harmonic foundation of the music.
"""

from __future__ import annotations
from .models import Timeline


def bass_scores(timeline: Timeline) -> dict[int, float]:
    """
    Return a mapping of note index -> bass bonus.

    Lower, longer notes receive higher scores.
    """

    scores: dict[int, float] = {}

    if not timeline.notes:
        return scores

    lowest_pitch = min(note.pitch for note in timeline.notes)

    for i, note in enumerate(timeline.notes):

        score = 0.0

        #
        # Favor notes close to the bottom of the piece.
        #
        distance = note.pitch - lowest_pitch

        score += max(0.0, 24.0 - distance) * 2.0

        #
        # Longer notes tend to be harmonic support.
        #
        score += note.duration / 150.0

        #
        # Reward notes that begin on a beat.
        #
        beat = note.start_tick % timeline.ticks_per_beat

        if beat == 0:
            score += 20.0
        elif beat <= timeline.ticks_per_beat // 8:
            score += 10.0

        scores[i] = score

    return scores