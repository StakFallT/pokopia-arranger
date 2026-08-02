"""
debug.py

Simple debugging logger for the arranger.
"""

from __future__ import annotations

from pathlib import Path


class DebugLogger:
    def __init__(self, enabled: bool = False):
        self.enabled = enabled
        self.lines: list[str] = []

    def log(self, message: str) -> None:
        if self.enabled:
            self.lines.append(message)

    def separator(self) -> None:
        if self.enabled:
            self.lines.append("-" * 60)

    def save(self, filename: str | Path) -> None:
        if not self.enabled:
            return

        Path(filename).write_text(
            "\n".join(self.lines),
            encoding="utf-8",
        )