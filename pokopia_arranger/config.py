"""
config.py

Configuration for the arranger.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class ArrangeConfig:
    #
    # Maximum simultaneous notes.
    #
    max_polyphony: int = 2

    #
    # Supported MatMaker range.
    #
    lowest_pitch: int = 48
    highest_pitch: int = 73

    #
    # Musical weights.
    #
    melody_weight: float = 1.0

    bass_weight: float = 1.0

    continuity_margin: float = 8.0
    continuity_weight: float = 30.0

    duration_weight: float = 0.01

    pitch_weight: float = 0.25

    #
    # Future options.
    #
    preserve_drums: bool = False

    remove_duplicate_octaves: bool = True

    simplify_repeated_notes: bool = True