"""
timeline.py

Convert a MIDI file into a unified timeline of notes.
"""

from __future__ import annotations
from collections import defaultdict
import mido
from .models import NoteEvent, Timeline


def build_timeline(mid: mido.MidiFile) -> Timeline:
    """
    Convert every MIDI track into a unified note timeline.
    """

    timeline = Timeline(
        ticks_per_beat=mid.ticks_per_beat,
    )

    for track_number, track in enumerate(mid.tracks):
        absolute_tick = 0

        # (channel, pitch) -> [(start_tick, velocity)]
        active_notes = defaultdict(list)

        for msg in track:
            absolute_tick += msg.time

            if msg.type == "set_tempo":
                timeline.tempo = msg.tempo

            elif msg.type == "time_signature":
                timeline.time_signature = (
                    msg.numerator,
                    msg.denominator,
                )

            elif msg.type == "key_signature":
                timeline.key_signature = msg.key

                
            if msg.type == "note_on" and msg.velocity > 0:
                active_notes[(msg.channel, msg.note)].append(
                    (
                        absolute_tick,
                        msg.velocity,
                    )
                )
            elif (
                msg.type == "note_off"
                or (
                    msg.type == "note_on"
                    and msg.velocity == 0
                )
            ):
                key = (msg.channel, msg.note)

                if not active_notes[key]:
                    continue

                start_tick, velocity = active_notes[key].pop(0)

                timeline.notes.append(
                    NoteEvent(
                        pitch=msg.note,
                        velocity=velocity,
                        start_tick=start_tick,
                        end_tick=absolute_tick,
                        channel=msg.channel,
                        track=track_number,
                    )
                )

    timeline.notes.sort(
        key=lambda note: (
            note.start_tick,
            note.pitch,
        )
    )

    return timeline