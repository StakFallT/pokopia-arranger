"""
midi.py

Low-level MIDI loading and saving.

This module intentionally does NOT contain arranging logic.
It only reads and writes Standard MIDI Files.
"""

from __future__ import annotations
from pathlib import Path

import mido

from collections import defaultdict

from .models import Timeline


def load_midi(path: str | Path) -> mido.MidiFile:
    """
    Load a MIDI file.

    Parameters
    ----------
    path
        Path to a MIDI file.

    Returns
    -------
    mido.MidiFile
    """

    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(path)

    return mido.MidiFile(path)


def save_midi(mid: mido.MidiFile, path: str | Path) -> None:
    """
    Save a MIDI file.
    """

    path = Path(path)
    mid.save(path)


def get_ticks_per_beat(mid: mido.MidiFile) -> int:
    """
    Return the MIDI resolution.
    """

    return mid.ticks_per_beat


def get_track_count(mid: mido.MidiFile) -> int:
    """
    Number of tracks in the MIDI.
    """

    return len(mid.tracks)


def iter_messages(mid: mido.MidiFile):
    """
    Iterate over every track and every message.

    Yields:
        (track_index, message)
    """

    for track_index, track in enumerate(mid.tracks):
        for msg in track:
            yield track_index, msg


def copy_structure(mid: mido.MidiFile) -> mido.MidiFile:
    """
    Create a new empty MIDI with the same type and resolution.

    Track contents are not copied.
    """

    new_mid = mido.MidiFile(
        type=mid.type,
        ticks_per_beat=mid.ticks_per_beat,
    )

    return new_mid


def timeline_to_midi(timeline: Timeline) -> mido.MidiFile:
    """
    Convert a Timeline back into a Standard MIDI File.

    Currently writes everything into a single track.
    """

    mid = mido.MidiFile(
        ticks_per_beat=timeline.ticks_per_beat,
        type=0,
    )

    track = mido.MidiTrack()

    track.append(
        mido.MetaMessage(
            "set_tempo",
            tempo=timeline.tempo,
            time=0,
        )
    )

    if timeline.time_signature is not None:
        numerator, denominator = timeline.time_signature

        track.append(
            mido.MetaMessage(
                "time_signature",
                numerator=numerator,
                denominator=denominator,
                time=0,
            )
        )

    if timeline.key_signature is not None:
        track.append(
            mido.MetaMessage(
                "key_signature",
                key=timeline.key_signature,
                time=0,
            )
        )


    mid.tracks.append(track)
    events = []

    for note in timeline.notes:
        events.append(
            (
                note.start_tick,
                1,
                note.pitch,
                note.velocity,
                note.channel,
            )
        )

        events.append(
            (
                note.end_tick,
                0,
                note.pitch,
                0,
                note.channel,
            )
        )

    #
    # IMPORTANT
    #
    # Sort by:
    #
    # tick
    # then note-offs before note-ons
    #

    events.sort(key=lambda e: (e[0], e[1]))
    previous_tick = 0

    for tick, event_type, pitch, velocity, channel in events:
        delta = tick - previous_tick
        previous_tick = tick

        if event_type == 1:
            track.append(
                mido.Message(
                    "note_on",
                    note=pitch,
                    velocity=velocity,
                    channel=channel,
                    time=delta,
                )
            )
        else:
            track.append(
                mido.Message(
                    "note_off",
                    note=pitch,
                    velocity=0,
                    channel=channel,
                    time=delta,
                )
            )

    track.append(
        mido.MetaMessage(
            "end_of_track",
            time=0,
        )
    )

    return mid