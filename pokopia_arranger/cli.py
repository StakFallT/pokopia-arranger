"""
cli.py

Command-line interface for the Pokopia Arranger.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from .arrange import arrange
from .config import ArrangeConfig
from .midi import (
    load_midi,
    save_midi,
    timeline_to_midi,
)
from .report import build_report
from .timeline import build_timeline


def main() -> None:

    parser = argparse.ArgumentParser(
        description="Arrange MIDI files for Pokémon Pokopia MatMaker."
    )

    parser.add_argument(
        "input",
        help="Input MIDI file",
    )

    parser.add_argument(
        "output",
        help="Output MIDI file",
    )

    parser.add_argument(
        "--polyphony",
        type=int,
        default=2,
        help="Maximum simultaneous notes.",
    )

    parser.add_argument(
        "--report",
        action="store_true",
        help="Print arranger statistics.",
    )

    parser.add_argument(
        "--benchmark",
        action="store_true",
        help="Arrange every MIDI in samples/input.",
    )

    args = parser.parse_args()

    config = ArrangeConfig(
        max_polyphony=args.polyphony,
    )

    from pathlib import Path
    from .benchmark import run_benchmark

    if args.benchmark:
        run_benchmark(
            Path("samples/input"),
            Path("samples/output"),
            Path("samples/reports"),
            config,
        )

        return

    mid = load_midi(args.input)

    timeline = build_timeline(mid)

    arranged = arrange(
        timeline,
        config,
    )

    if args.report:

        print("Original")
        print("--------")
        print(build_report(timeline))
        print()

        print("Arranged")
        print("---------")
        print(build_report(arranged))
        print()

    out = timeline_to_midi(arranged)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    save_midi(out, output_path)

    print(f"Wrote {output_path}")


main();