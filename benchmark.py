"""
benchmark.py

Run the arranger over every MIDI file in the samples directory.
"""

from pathlib import Path

from pokopia_arranger.reader import read_midi
from pokopia_arranger.writer import write_midi
from pokopia_arranger.simplify import limit_polyphony
from pokopia_arranger.config import ArrangeConfig


INPUT_DIR = Path("samples")
OUTPUT_DIR = Path("output")

OUTPUT_DIR.mkdir(exist_ok=True)


config = ArrangeConfig(
    max_polyphony=2,)


for midi_file in sorted(INPUT_DIR.glob("*.mid")):

    print(f"Processing {midi_file.name}")

    timeline = read_midi(midi_file)

    arranged = limit_polyphony(
        timeline,
        config,
    )

    output_file = OUTPUT_DIR / midi_file.name

    write_midi(
        arranged,
        output_file,
    )

print("Done.")