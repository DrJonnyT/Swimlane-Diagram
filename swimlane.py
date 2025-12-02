
import matplotlib.pyplot as plt

# --- CONFIGURABLE DATA -----------------------------------------------------
# Lanes (rows)
lanes = ["RSE\nBaseline\nSupport", "Project 1", "Project 2", "Project 3"]

# Tasks defined as: (lane_index, start, end, color, label)
# Replace the sample values with your own start/end (numbers or datetime converted to numbers)
tasks = [
    # RSE Baseline Support broken into segments
    (0, 0.0, 1.0, 'lightgreen',    'Self-directed\ntraining'),
    (0, 1.0, 2.0, 'skyblue',    'Project 1\nsupport'),
    (0, 2.0, 3.0, 'lightgreen', 'Tooling\ndevelopment'),
    (0, 3.0, 4.0, 'yellow', 'Project 3\nsupport'),
    (0, 4.0, 6.0, 'lightgreen', 'Tooling development'),
    (0, 6.0, 7.0, 'skyblue',     'Project 1\nsupport'),
    (0, 7.0, 8.0, 'skyblue',     'Project 1\ndeployment'),
    (0, 8.0, 9.0, 'yellow',     'Project 3\nsupport'),
    (0, 9.0, 10.0, 'yellow',     'Project 3\ndeployment'),
    (0, 10.0, 11.0, 'skyblue',     'Project 1\nmaintenence'),
    (0, 11.0, 12.0, 'yellow',     'Project 3\nmaintenence'),


    # Project 1
    (1, 1.0, 7.0, 'skyblue',     'Project 1\nPDRA'),

    # Project 2
    (2, 2.0, 8.0, 'pink',       'Project 2 development\nRSE'),
    (2, 8.0, 9.0, 'pink',       'Project 2\ndeployment'),

    # Project 3
    (3, 3.0, 9.0, 'yellow',     'Project 3\nPDRA'),
]

# --- PLOT ------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(15, 6))

bar_height = 0.8  # height of each lane bar
lane_offset = 0.4  # half-height for positioning

for lane_idx, start, end, color, label in tasks:
    duration = end - start
    # Draw the bar using start and duration
    ax.broken_barh([(start, duration)], (lane_idx - lane_offset, bar_height),
                   facecolors=color, edgecolor='black')

    # Center the text inside the bar
    text_x = start + duration / 2
    text_y = lane_idx
    ax.text(text_x, text_y, label, ha='center', va='center', fontsize=9,
            color='black', weight='bold', wrap=True)

# Y axis: lanes
ax.set_yticks(range(len(lanes)))
ax.set_yticklabels(lanes)

# Labels and title
ax.set_xlabel('Time')
ax.set_xticklabels([''] * len(ax.get_xticks()))  # No numbers on x axis
ax.set_title('Project Staffing Model')

# Grid and limits
min_time = min(t[1] for t in tasks)
max_time = max(t[2] for t in tasks)
span = max_time - min_time
ax.set_xlim(0 - 0.5*span*0.05, max_time +
            0.5*span*0.05)  # small padding
ax.set_ylim(-0.5, len(lanes) - 0.5)
ax.grid(axis='x', linestyle='--', alpha=0.3)

fig.tight_layout()
fig.savefig('swimlane.png', dpi=150)
print('Swimlane diagram saved as swimlane.png')
