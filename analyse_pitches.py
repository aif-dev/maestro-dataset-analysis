import os
import pretty_midi
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.graphics.gofplots import qqplot


def get_pitch_data(midi_data):
    pitches = []
    time_spans = []

    for note in midi_data.instruments[0].notes:
        pitches.append(note.pitch)
        time_spans.append(note.end - note.start)

    return pitches, time_spans


root_dir = "dataset/maestro-v3.0.0"

if not os.path.exists(root_dir):
    print("Directory 'dataset/maestro-v3.0.0' not found!")
    print("In the directory with this file create a directory 'dataset' then inside this directory download and unzip the dataset with MIDI tracks.")
    print("Link: https://storage.googleapis.com/magentadata/datasets/maestro/v3.0.0/maestro-v3.0.0-midi.zip")
    exit(1)

pitches = []
pitch_time_spans = []
for subdir, _, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".midi"):
            full_filename = os.path.join(subdir, file)
            midi_data = pretty_midi.PrettyMIDI(full_filename)
            track_pitches, track_pitch_time_spans = get_pitch_data(midi_data)
            pitches.extend(track_pitches)
            pitch_time_spans.extend(track_pitch_time_spans)

fig, axes = plt.subplots(2, 3)

fig.canvas.set_window_title('Histograms / Boxplots')
fig.suptitle("MIDI pitches from the Maestro dataset")

sorted_pitch_counter = Counter(sorted(pitches))
axes[0, 0].set_title("MIDI pitches")
axes[0, 0].bar(sorted_pitch_counter.keys(), sorted_pitch_counter.values())
axes[0, 0].set_ylabel("n")
axes[0, 0].set_xlabel("pitch")
axes[0, 0].set_xlim([21, 108])

df_pitches = pd.DataFrame(pitches, columns=['pitch'])
axes[1, 0].set_title("MIDI pitches - qqplot (normal distribution)")
qqplot(df_pitches['pitch'], line="s", ax=axes[1, 0])

df_time_spans = pd.DataFrame(pitch_time_spans, columns=['time_span'])
axes[0, 1].set_title("time span")
axes[0, 1].boxplot(df_time_spans)
axes[0, 1].set_ylabel("seconds")
axes[0, 1].set_ylim([0, None])

axes[1, 1].set_title("time span - qqplot (normal distribution)")
qqplot(df_time_spans['time_span'], line="s", ax=axes[1, 1])

# remove outliers
Q1 = df_time_spans['time_span'].quantile(0.25)
Q3 = df_time_spans['time_span'].quantile(0.75)
IQR = Q3 - Q1
df_filter = (df_time_spans['time_span'] >= Q1 - 1.5 * IQR) & (df_time_spans['time_span'] <= Q3 + 1.5 * IQR)
df_time_spans_clean = df_time_spans.loc[df_filter]
remaining_points_percentage = round(100 * len(df_time_spans_clean.index) / len(df_time_spans.index), 2)

axes[0, 2].set_title(f"time span without outliers ({remaining_points_percentage}% points left)")
axes[0, 2].boxplot(df_time_spans_clean, whis=[0, 100])
axes[0, 2].set_ylabel("seconds")
axes[0, 2].set_ylim([0, None])

axes[1, 2].set_title("time span without outliers - qqplot (normal distribution)")
qqplot(df_time_spans_clean['time_span'], line="s", ax=axes[1, 2])

plt.show()
