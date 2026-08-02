"""
combination_scoring.py

Evaluate a candidate combination of simultaneously sounding notes.

This module contains all of the musical decision-making logic used
by the arranger.
"""

from __future__ import annotations

from .config import ArrangeConfig
from .harmony import harmony_penalty
from .models import NoteEvent
from .scoring import score_note


def _melody_bonus(
    note: NoteEvent,
    active_notes: list[NoteEvent],
) -> float:

    highest = max(n.pitch for n in active_notes)
    distance = highest - note.pitch

    if distance <= 0:
        return 40.0
    elif distance <= 2:
        return 30.0
    elif distance <= 5:
        return 20.0
    elif distance <= 12:
        return 10.0

    return 0.0


def _bass_bonus(
    note: NoteEvent,
    active_notes: list[NoteEvent],
) -> float:

    lowest = min(n.pitch for n in active_notes)
    distance = note.pitch - lowest

    if distance <= 0:
        return 40.0
    elif distance <= 2:
        return 30.0
    elif distance <= 5:
        return 20.0
    elif distance <= 12:
        return 10.0

    return 0.0


def evaluate_combination(
    selected_indices: tuple[int, ...],
    notes: list[NoteEvent],
    active_notes: list[NoteEvent],
    phrase_scores: dict[int, float],
    motion_scores: dict[int, float],
    previous_selection: set[int],
    config: ArrangeConfig,
) -> float:
    """
    Compute the overall musical quality of a candidate note selection.
    """

    selected_notes = [notes[i] for i in selected_indices]

    score = 0.0

    #
    # Determine the true melody and bass of the ACTIVE texture.
    #
    true_melody = max(active_notes, key=lambda n: n.pitch)
    true_bass = min(active_notes, key=lambda n: n.pitch)

    #
    # Determine the melody and bass of the selected combination.
    #
    selected_melody = max(selected_notes, key=lambda n: n.pitch)
    selected_bass = min(selected_notes, key=lambda n: n.pitch)

    #
    # Strongly reward preserving the actual melody.
    #
    if selected_melody.pitch == true_melody.pitch:
        score += 50.0
    else:
        score -= 25.0

    #
    # Strongly reward preserving the actual bass.
    #
    if selected_bass.pitch == true_bass.pitch:
        score += 50.0
    else:
        score -= 25.0

    #
    # Score each selected note.
    #
    for index in selected_indices:

        note = notes[index]

        melody_bonus = 0.0
        bass_bonus = 0.0

        #
        # Only reward notes that actually preserve the
        # real melody and bass of the music.
        #
        melody_bonus = (
            _melody_bonus(note, active_notes)
            if note.pitch == true_melody.pitch
            else 0.0
        )

        bass_bonus = (
            _bass_bonus(note, active_notes)
            if note.pitch == true_bass.pitch
            else 0.0
        )

        score += score_note(
            note,
            config=config,
            melody_bonus=melody_bonus,
            bass_bonus=bass_bonus,
            phrase_bonus=phrase_scores.get(index, 0.0),
        )

        score += motion_scores.get(index, 0.0)

        if index in previous_selection:
            score += config.continuity_weight

    #
    # Harmony quality
    #
    score -= harmony_penalty(selected_notes)

    #
    # Reward good spacing.
    #
    if len(selected_notes) >= 2:

        pitches = sorted(n.pitch for n in selected_notes)

        spread = pitches[-1] - pitches[0]

        #
        # Melody and bass should usually be separated.
        #
        if 12 <= spread <= 24:
            score += 12.0

        elif 24 < spread <= 36:
            score += 8.0

        elif spread < 5:
            score -= 15.0

        elif spread < 8:
            score -= 8.0

    return score