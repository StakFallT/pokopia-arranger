"""
benchmark.py

Run the arranger against every MIDI file in a directory.
"""

from __future__ import annotations

from pathlib import Path

from .arrange import arrange
from .config import ArrangeConfig
from .midi import load_midi, save_midi, timeline_to_midi
from .report import build_report
from .timeline import build_timeline


def run_benchmark(
    input_dir: Path,
    output_dir: Path,
    report_dir: Path,
    config: ArrangeConfig,
) -> None:

    output_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)

    midi_files = sorted(input_dir.glob("*.mid"))
    midi_files.extend(sorted(input_dir.glob("*.midi")))

    if not midi_files:
        print("No MIDI files found.")
        return

    print(f"Found {len(midi_files)} MIDI file(s).\n")

    for midi_file in midi_files:

        print(f"Processing {midi_file.name}...")

        mid = load_midi(midi_file)

        original = build_timeline(mid)

        arranged = arrange(original, config)

        out_mid = timeline_to_midi(arranged)

        output_path = output_dir / midi_file.name

        save_midi(out_mid, output_path)

        report = []

        report.append("Original")
        report.append("--------")
        report.append(build_report(original))
        report.append("")
        report.append("Arranged")
        report.append("---------")
        report.append(build_report(arranged))

        report_path = report_dir / f"{midi_file.stem}.txt"

        report_path.write_text(
            "\n".join(report),
            encoding="utf-8",
        )

        print("  ✓ MIDI written")
        print("  ✓ Report written\n")

    print("Benchmark complete.")