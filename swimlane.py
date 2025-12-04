
import matplotlib.pyplot as plt

# --- CONFIGURABLE DATA -----------------------------------------------------
lanes = ["RSE\nBaseline\nSupport", "Project 1", "Project 2", "Project 3"]

# Tasks defined as: (lane_index, start, end, color, label)
# NOTE: You can now include overlapping tasks for lane 0 (baseline)
tasks = [
    # --- Baseline (lane 0) — you MAY overlap these times ---
    (0, 0.0, 1.5, 'lightgreen', 'Self-directed\ntraining'),
    (0, 1.0, 2.0, 'skyblue',    'Project 1\nsupport'),      # overlaps with training
    (0, 2.0, 7.0, 'lightgreen', 'Tooling\ndevelopment'),
    (0, 4.0, 5.0, 'yellow',     'Project 3\nsupport'),
    # overlaps with tooling
    (0, 9.0, 10.0, 'skyblue',     'Project 1\nmaintenance'),
    (0, 6.5, 7.3, 'skyblue',       'Project 1\nsupport'),  # overlaps with tooling
    (0, 7.0, 8.5, 'skyblue',    'Project 1\ndeployment'),
    (0, 8.5, 9.5, 'pink',       'Project 2\ndeployment'),
    (0, 9.5, 10.5, 'yellow',    'Project 3\nsupport'),
    (0, 10.5, 12.0, 'yellow',   'Project 3\ndeployment'),
    (0, 11.5, 12.5, 'pink',  'Project 2\nmaintenance'),
    (0, 12.5, 13.5, 'yellow',   'Project 3\nmaintenance'),

    # --- Other lanes (unchanged) ---
    (1, 1.0, 7.0, 'skyblue',    'Project 1\nPDRA'),
    (2, 2.0, 8.0, 'pink',       'Project 2 development\nRSE'),
    (3, 4.0, 10.0, 'yellow',    'Project 3\nPDRA'),
]

# --- UTILITIES -------------------------------------------------------------


def assign_two_tracks_no_overlap(baseline_tasks):
    """
    Assign baseline tasks to two tracks (0 bottom, 1 top) to avoid overlap.
    If both tracks overlap at a given start time, place on track 0 and warn.
    Returns list of tuples: (lane, start, end, color, label, track)
    """
    # sort by start to make greedy placement reliable
    baseline_sorted = sorted(baseline_tasks, key=lambda x: (x[1], x[2]))
    last_end = {0: -float('inf'), 1: -float('inf')}
    assigned = []
    for lane, start, end, color, label in baseline_sorted:
        placed = False
        # try bottom then top
        for trk in (0, 1):
            if start >= last_end[trk]:
                assigned.append((lane, start, end, color, label, trk))
                last_end[trk] = end
                placed = True
                break
        if not placed:
            # more than two overlaps at the same time
            print(f"WARNING: >2 overlapping baseline tasks around t={start}. "
                  f"Placing '{label}' on bottom track; it will visually overlap.")
            assigned.append((lane, start, end, color, label, 0))
            # do not update last_end to force the warning if pattern continues
    return assigned


# --- PREPARE DATA ----------------------------------------------------------
baseline = [t for t in tasks if t[0] == 0]
others = [t for t in tasks if t[0] != 0]

baseline_with_tracks = assign_two_tracks_no_overlap(baseline)

# --- PLOT ------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(14, 7))

bar_height = 0.8   # full lane height
lane_offset = 0.4   # half-height for positioning
gap = 0.06  # small gap between the halves
half_height = (bar_height - gap) / 2.0

# Plot baseline with two tracks
for lane_idx, start, end, color, label, track in baseline_with_tracks:
    duration = end - start
    base_ymin = lane_idx - lane_offset
    if track == 0:  # bottom half
        ymin = base_ymin
    else:           # top half
        ymin = base_ymin + half_height + gap
    yheight = half_height

    # bar
    ax.broken_barh([(start, duration)], (ymin, yheight),
                   facecolors=color, edgecolor='black')
    # centered text within the sub-bar
    text_x = start + duration / 2
    text_y = ymin + yheight / 2
    max_font_size = 18
    min_font_size = 8.5
    font_size = max(min_font_size, min(max_font_size, duration * 8))
    ax.text(text_x, text_y, label, ha='center', va='center',
            fontsize=font_size, color='black', weight='bold', wrap=True)

# Plot other lanes normally (full-height bars)
for lane_idx, start, end, color, label in others:
    duration = end - start
    ymin = lane_idx - lane_offset
    yheight = bar_height
    ax.broken_barh([(start, duration)], (ymin, yheight),
                   facecolors=color, edgecolor='black')

    text_x = start + duration / 2
    text_y = lane_idx
    max_font_size = 18
    min_font_size = 8.5
    font_size = max(min_font_size, min(max_font_size, duration * 8))
    ax.text(text_x, text_y, label, ha='center', va='center',
            fontsize=font_size, color='black', weight='bold', wrap=True)

# Y axis: lanes
ax.set_yticks(range(len(lanes)))
ax.set_yticklabels(lanes)
ax.tick_params(axis='y', labelsize=14)

# Labels and title
ax.set_xlabel('Time')
ax.set_xticklabels([''] * len(ax.get_xticks()))  # No numbers on x axis
