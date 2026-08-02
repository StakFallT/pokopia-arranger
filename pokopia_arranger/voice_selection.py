"""
voice_selection.py

Select which notes to keep when too many notes are sounding
simultaneously.
"""

from __future__ import annotations

from .debug import DebugLogger

from itertools import combinations

from .config import ArrangeConfig
from .models import NoteEvent
from .combination_scoring import evaluate_combination


from dataclasses import dataclass

@dataclass(slots=True)
class VoiceState:
    melody: NoteEvent | None = None
    bass: NoteEvent | None = None

def choose_notes(
    notes: list[NoteEvent],
    note_indices: list[int],
    current_tick: int,
    phrase_scores: dict[int, float],
    motion_scores: dict[int, float],
    config: ArrangeConfig,
    previous_selection: set[int] | None = None,
    debug: DebugLogger | None = None,
) -> set[int]:

    best_score = float("-inf")
    best_selection: set[int] = set()

    active_notes = [notes[i] for i in note_indices]

    for combo in combinations(note_indices, config.max_polyphony):

        score = evaluate_combination(
            selected_indices=combo,
            notes=notes,
            active_notes=active_notes,
            phrase_scores=phrase_scores,
            motion_scores=motion_scores,
            previous_selection=previous_selection,
            config=config,
        )

        if debug is not None and debug.enabled:
            debug.log(
                f"Candidate {list(combo)} -> {score:.2f}"
            )

        if score > best_score + config.continuity_margin:
            best_score = score
            best_selection = set(combo)

        elif abs(score - best_score) <= config.continuity_margin:

            overlap = len(set(combo) & previous_selection)
            best_overlap = len(best_selection & previous_selection)

            if overlap > best_overlap:
                best_score = score
                best_selection = set(combo)

    if debug is not None and debug.enabled:
        debug.log(f"Tick {current_tick}")
        debug.log("Active notes:")

        for index in note_indices:
            note = notes[index]
            debug.log(
                f"  [{index}] "
                f"pitch={note.pitch} "
                f"start={note.start_tick} "
                f"end={note.end_tick}"
            )

        debug.log(f"Winner: {sorted(best_selection)}")
        debug.log(f"Winning Score: {best_score:.2f}")
        debug.separator()
        debug.log("")

    return best_selection