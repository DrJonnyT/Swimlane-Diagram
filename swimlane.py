
import matplotlib.pyplot as plt

# --- CONFIGURABLE DATA -----------------------------------------------------
lanes = ["RSE\nBaseline\nSupport", "Project 1", "Project 2", "Project 3"]

# Tasks defined as: (lane_index, start, end, color, label)
# NOTE: You can now include overlapping tasks for lane 0 (baseline)
tasks = [
    # --- Baseline (lane 0) — you MAY overlap these times ---
    (0, 0.0, 2.5, 'lightgreen', 'Self-directed\ntraining'),
    (0, 1.0, 2.0, 'skyblue',    'Project 1\nsupport'),      # overlaps with training
    (0, 2.5, 7.0, 'lightgreen', 'Tooling\ndevelopment'),
    (0, 4.0, 5.0, 'yellow',     'Project 3\nsupport'),      # overlaps with tooling
    (0, 10.0, 11.0, 'skyblue',   'Project 1\nmaint    \n   enance'),
    (0, 6.0, 7.0, 'skyblue',    'Project 1\nsupport'),      # overlaps with tooling
    (0, 7.0, 8.5, 'skyblue',    'Project 1\ndeployment'),
    (0, 8.5, 9.5, 'pink',       'Project 2\ndeployment'),
    (0, 9.0, 10.0, 'yellow',    'Project 3\nsupport'),
    (0, 10.5, 12.0, 'yellow',   'Project 3\ndeployment'),
    (0, 11.5, 12.5, 'pink',     'Project 2\nmaint    \n   enance'),
    (0, 12.5, 13.5, 'yellow',   'Project 3\nmaint    \n   enance'),

    # --- Other lanes (unchanged) ---
    (1, 1.0, 7.0, 'skyblue',    'Project 1\nPDRA'),
    (2, 2.0, 8.0, 'pink',       'Project 2 development\nRSE'),
    (3, 4.0, 10.0, 'yellow',    'Project 3\nPDRA'),
]

# Separate baseline vs other lanes
baseline_tasks = [t for t in tasks if t[0] == 0]
other_tasks = [t for t in tasks if t[0] != 0]

# --- UTILITIES -------------------------------------------------------------


def assign_two_tracks_no_overlap(baseline_tasks):
    """
    Assign baseline tasks to two tracks (0 bottom, 1 top) to avoid overlap.
    If >2 tasks overlap at the same time, place on track 0 and print a warning.
    Returns list of tuples: (lane, start, end, color, label, track)
    """
    baseline_sorted = sorted(baseline_tasks, key=lambda x: (x[1], x[2]))
    last_end = {0: -float('inf'), 1: -float('inf')}
    assigned = []
    for lane, start, end, color, label in baseline_sorted:
        placed = False
        for trk in (0, 1):  # try bottom then top
            if start >= last_end[trk]:
                assigned.append((lane, start, end, color, label, trk))
                last_end[trk] = end
                placed = True
                break
        if not placed:
            print(f"WARNING: >2 overlapping baseline tasks around t={start}. "
                  f"Placing '{label}' on bottom track; it may visually overlap.")
            assigned.append((lane, start, end, color, label, 0))
    return assigned


baseline_with_tracks = assign_two_tracks_no_overlap(baseline_tasks)

# --- PLOT ------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(14, 7))

bar_height = 0.8   # full lane height
lane_offset = 0.4   # half-height for positioning
gap = 0.06  # small gap between halves
half_height = (bar_height - gap) / 2.0

# --- Font settings ---------------------------------------------------------
fixed_bottom_font = 9.0   # fixed font for baseline bottom track (track 0)
fixed_top_font = None  # set to a number to fix top track too; None = dynamic
max_font_size = 18.0
min_font_size = 8.5


def dynamic_font(duration):
    return max(min_font_size, min(max_font_size, duration * 8))


# Plot baseline (two-track)
for lane_idx, start, end, color, label, track in baseline_with_tracks:
    duration = end - start
    base_ymin = lane_idx - lane_offset
    ymin = base_ymin if track == 0 else base_ymin + half_height + gap
    yheight = half_height

    ax.broken_barh([(start, duration)], (ymin, yheight),
                   facecolors=color, edgecolor='black')

    text_x = start + duration / 2
    text_y = ymin + yheight / 2

    # FONT LOGIC: fixed on bottom track, optional fixed on top track, dynamic otherwise
    if track == 0:
        font_size = fixed_bottom_font
    elif fixed_top_font is not None:
        font_size = fixed_top_font
    else:
        font_size = dynamic_font(duration)

    ax.text(text_x, text_y, label, ha='center', va='center',
            fontsize=font_size, color='black', weight='bold', wrap=True)

# Plot project lanes (full-height bars, dynamic font)
for lane_idx, start, end, color, label in other_tasks:
    duration = end - start
    ymin = lane_idx - lane_offset
    yheight = bar_height

    ax.broken_barh([(start, duration)], (ymin, yheight),
                   facecolors=color, edgecolor='black')

    text_x = start + duration / 2
    text_y = lane_idx

    font_size = dynamic_font(duration)  # dynamic for main tasks

    ax.text(text_x, text_y, label, ha='center', va='center',
            fontsize=font_size, color='black', weight='bold', wrap=True)

# Y axis: lanes
ax.set_yticks(range(len(lanes)))
ax.set_yticklabels(lanes)
ax.tick_params(axis='y', labelsize=14)

# Labels and title
ax.set_xlabel('Time')
ax.set_xticklabels([''] * len(ax.get_xticks()))  # No numbers on x axis
ax.set_title('Project Staffing Model')

# Grid and limits
min_time = min(t[1] for t in tasks)
max_time = max(t[2] for t in tasks)
span = max_time - min_time
ax.set_xlim(0 - 0.5*span*0.05, max_time + 0.5*span*0.05)  # small padding
ax.set_ylim(-0.5, len(lanes) - 0.5)
ax.grid(axis='x', linestyle='--', alpha=0.3)

fig.tight_layout()
fig.savefig('swimlane.png', dpi=150)
print('Swimlane diagram saved as swimlane.png')
