from pokopia_arranger.midi import (
    load_midi,
    save_midi,
    timeline_to_midi,
)

from pokopia_arranger.timeline import build_timeline

from pokopia_arranger.matmaker import (
    fit_into_range,
    clamp_to_range,
)

mid = load_midi("samples/input/Brinstar.mid")
timeline = build_timeline(mid)
timeline = fit_into_range(timeline)
timeline = clamp_to_range(timeline)
new_mid = timeline_to_midi(timeline)

save_midi(new_mid, "samples/output/brinstar_benchmark1_matmaker.mid")
print("Done!")