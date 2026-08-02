"""
analyze.py

Functions for analyzing a Timeline.
"""

from __future__ import annotations
from collections import defaultdict
from .models import Timeline


def note_count(timeline: Timeline) -> int:
    """Return the total number of notes."""
    return len(timeline.notes)


def pitch_range(timeline: Timeline) -> tuple[int, int]:
    """
    Return (lowest_pitch, highest_pitch).
    """
    if not timeline.notes:
        return (0, 0)

    lowest = min(note.pitch for note in timeline.notes)
    highest = max(note.pitch for note in timeline.notes)

    return (lowest, highest)


def track_count(timeline: Timeline) -> int:
    """
    Return the number of tracks that contain notes.
    """
    return len({note.track for note in timeline.notes})


def duration_ticks(timeline: Timeline) -> int:
    """
    Return the duration of the piece in ticks.
    """
    if not timeline.notes:
        return 0

    return max(note.end_tick for note in timeline.notes)


def max_polyphony(timeline: Timeline) -> int:
    """
    Return the maximum number of simultaneously sounding notes.
    """

    events = []

    for note in timeline.notes:
        # 1 = note on
        events.append((note.start_tick, 1))

        # 0 = note off
        events.append((note.end_tick, 0))

    # At the same tick, process note-offs before note-ons.
    events.sort()

    current = 0
    maximum = 0

    for _, event_type in events:
        if event_type == 0:
            current -= 1
        else:
            current += 1
            maximum = max(maximum, current)

    return maximum


def pitch_histogram(timeline: Timeline) -> dict[int, int]:
    """
    Return a histogram of pitch usage.
    """
    histogram = defaultdict(int)

    for note in timeline.notes:
        histogram[note.pitch] += 1

    return dict(sorted(histogram.items()))


NOTE_NAMES = (
    "C",
    "C#",
    "D",
    "D#",
    "E",
    "F",
    "F#",
    "G",
    "G#",
    "A",
    "A#",
    "B",
)


def pitch_name(pitch: int) -> str:
    octave = (pitch // 12) - 1
    name = NOTE_NAMES[pitch % 12]
    return f"{name}{octave}"