
import matplotlib.pyplot as plt

# Define lanes and tasks with start and end times
lanes = ["RSE Baseline Support", "Project 1", "Project 2", "Project 3"]

# Example tasks: (lane index, start, duration, color, label)
tasks = [
    # RSE Baseline Support broken into segments
    (0, 1, 2, 'skyblue', 'RSE Segment 1'),
    (0, 4, 1.5, 'lightgreen', 'RSE Segment 2'),
    (0, 6, 2, 'orange', 'RSE Segment 3'),

    # Project 1 tasks
    (1, 2, 3, 'purple', 'Project 1 Task'),

    # Project 2 tasks
    (2, 1, 4, 'pink', 'Project 2 Task'),

    # Project 3 tasks
    (3, 5, 2, 'yellow', 'Project 3 Task')
]

# Create figure and axis
fig, ax = plt.subplots(figsize=(10, 6))

# Plot each task as a horizontal bar
for lane_idx, start, duration, color, label in tasks:
    ax.broken_barh([(start, duration)], (lane_idx - 0.4, 0.8),
                   facecolors=color, edgecolor='black')

# Set y-ticks and labels
ax.set_yticks(range(len(lanes)))
ax.set_yticklabels(lanes)

# Set axis labels and title
ax.set_xlabel('Time')
ax.set_ylabel('Lanes')
ax.set_title('Swimlane Diagram')

# Create legend dynamically from tasks
legend_patches = []
for _, _, _, color, label in tasks:
    if label not in [p.get_label() for p in legend_patches]:
        legend_patches.append(mpatches.Patch(color=color, label=label))

ax.legend(handles=legend_patches, loc='upper right')

# Set limits for better visualization
ax.set_xlim(0, 10)
ax.set_ylim(-0.5, len(lanes) - 0.5)

# Save outputs
fig.tight_layout()
fig.savefig('swimlane_diagram.png')
print("Swimlane diagram saved as swimlane_diagram.png")
