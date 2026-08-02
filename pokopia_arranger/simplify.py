"""
simplify.py

Basic arranging algorithms.

These functions always return a NEW Timeline and never modify
the input Timeline.
"""
from __future__ import annotations

from .debug import DebugLogger

from .config import ArrangeConfig
from copy import deepcopy
from .models import Timeline
#from .scoring import score_note
from .phrase import phrase_scores
from .voice_selection import choose_notes
from .motion import motion_scores


def limit_polyphony(
    timeline: Timeline,
    config: ArrangeConfig,
) -> Timeline:

    new = Timeline(
        ticks_per_beat=timeline.ticks_per_beat,
        tempo=timeline.tempo,
        time_signature=timeline.time_signature,
        key_signature=timeline.key_signature,
    )

    notes = deepcopy(timeline.notes)

    new.notes = notes

    debug = DebugLogger(enabled=True)

    phrases = phrase_scores(new)
    motions = motion_scores(new)

    keep = set()

    previous_selection = set()

    event_ticks = sorted(
        {n.start_tick for n in notes}
        |
        {n.end_tick for n in notes}
    )

    for tick in event_ticks:

        active = [
            i
            for i, note in enumerate(notes)
            if note.start_tick <= tick < note.end_tick
        ]

        selected = choose_notes(
            notes=notes,
            note_indices=active,
            current_tick=tick,
            phrase_scores=phrases,
            motion_scores=motions,
            config=config,
            previous_selection=previous_selection,
            debug=debug,
        )

        keep.update(selected)

        previous_selection = selected

    new.notes = [
        note
        for i, note in enumerate(notes)
        if i in keep
    ]

    debug.save("arranger_debug.txt")

    return new