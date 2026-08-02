"""
report.py

Generate human-readable statistics for a Timeline.
"""

from __future__ import annotations

from .analyze import (
    duration_ticks,
    max_polyphony,
    note_count,
    pitch_range,
    track_count,
)

from .models import Timeline


def build_report(timeline: Timeline) -> str:

    low, high = pitch_range(timeline)

    lines = []

    lines.append(f"Tracks      : {track_count(timeline)}")
    lines.append(f"Notes       : {note_count(timeline)}")
    lines.append(f"Range       : {low}-{high}")
    lines.append(f"Duration    : {duration_ticks(timeline)} ticks")
    lines.append(f"Polyphony   : {max_polyphony(timeline)}")

    return "\n".join(lines)