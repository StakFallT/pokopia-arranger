from dataclasses import dataclass, field


@dataclass(slots=True)
class NoteEvent:
    pitch: int
    velocity: int

    start_tick: int
    end_tick: int

    channel: int
    track: int

    @property
    def duration(self) -> int:
        return self.end_tick - self.start_tick


@dataclass
class Timeline:
    ticks_per_beat: int
    notes: list[NoteEvent] = field(default_factory=list)
    tempo: int = 500000
    time_signature: tuple[int, int] | None = None
    key_signature: str | None = None