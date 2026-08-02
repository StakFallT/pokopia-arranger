"""
matmaker.py

Functions specific to the Pokémon Pokopia MatMaker.

Currently handles:

- Range validation
- Automatic transposition into the supported note range
"""

from __future__ import annotations
from copy import deepcopy
from .models import Timeline


MATMAKER_LOW = 48      # C3
MATMAKER_HIGH = 73     # C#5


def note_range(timeline: Timeline) -> tuple[int, int]:
    if not timeline.notes:
        return (0, 0)

    low = min(n.pitch for n in timeline.notes)
    high = max(n.pitch for n in timeline.notes)

    return (low, high)


def is_in_range(timeline: Timeline) -> bool:
    """
    Returns True if every note is already playable.
    """

    for note in timeline.notes:
        if note.pitch < MATMAKER_LOW:
            return False

        if note.pitch > MATMAKER_HIGH:
            return False

    return True


def transpose(timeline: Timeline, semitones: int) -> Timeline:
    """
    Return a new Timeline transposed by the given number of semitones.
    """

    new = deepcopy(timeline)

    for note in new.notes:
        note.pitch += semitones

    return new


def fit_into_range(timeline: Timeline) -> Timeline:
    """
    Automatically transpose the song by octaves until it best fits
    the MatMaker range.

    This does NOT yet compress notes individually.
    It preserves intervals exactly.
    """

    low, high = note_range(timeline)

    best_shift = 0
    best_score = None

    # Search ±4 octaves.
    for shift in range(-48, 49, 12):

        shifted_low = low + shift
        shifted_high = high + shift

        penalty = 0

        if shifted_low < MATMAKER_LOW:
            penalty += MATMAKER_LOW - shifted_low

        if shifted_high > MATMAKER_HIGH:
            penalty += shifted_high - MATMAKER_HIGH

        if best_score is None or penalty < best_score:
            best_score = penalty
            best_shift = shift

    return transpose(timeline, best_shift)


def clamp_to_range(timeline: Timeline) -> Timeline:
    """
    Force every note into the MatMaker range.

    This preserves rhythm but may change octaves.
    """

    new = deepcopy(timeline)

    for note in new.notes:
        while note.pitch < MATMAKER_LOW:
            note.pitch += 12

        while note.pitch > MATMAKER_HIGH:
            note.pitch -= 12

    return new