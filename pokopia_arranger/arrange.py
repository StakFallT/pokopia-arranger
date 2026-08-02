"""
arrange.py

High-level arranging pipeline.
"""

from __future__ import annotations

from .config import ArrangeConfig
from .matmaker import (
    clamp_to_range,
    fit_into_range,
)
from .simplify import limit_polyphony
from .models import Timeline


def arrange(
    timeline: Timeline,
    config: ArrangeConfig | None = None,
) -> Timeline:

    if config is None:
        config = config or ArrangeConfig()

    timeline = limit_polyphony(
        timeline,
        config,
    )

    timeline = fit_into_range(timeline)

    timeline = clamp_to_range(timeline)

    return timeline