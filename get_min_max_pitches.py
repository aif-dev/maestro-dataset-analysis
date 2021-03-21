import os
import pretty_midi


def get_min_max_pitches(midi_data):
    min_pitch = midi_data.instruments[0].notes[0].pitch
    max_pitch = midi_data.instruments[0].notes[0].pitch

    for note in midi_data.instruments[0].notes[1:]:
        pitch = note.pitch
        
        if pitch > max_pitch:
            max_pitch = pitch
        elif pitch < min_pitch:
            min_pitch = pitch

    return min_pitch, max_pitch


root_dir = "dataset/maestro-v3.0.0"

if not os.path.exists(root_dir):
    print("Directory 'dataset/maestro-v3.0.0' not found!")
    print("In the directory with this file create a directory 'dataset' then inside this directory download and unzip the dataset with MIDI tracks.")
    print("Link: https://storage.googleapis.com/magentadata/datasets/maestro/v3.0.0/maestro-v3.0.0-midi.zip")
    exit(1)

global_min_pitch = float("inf")
global_max_pitch = float("-inf")

for subdir, _, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".midi"):
            full_filename = os.path.join(subdir, file)
            min_pitch, max_pitch = get_min_max_pitches(pretty_midi.PrettyMIDI(full_filename))

            if max_pitch > global_max_pitch:
                print(f"Global max updated ({global_max_pitch} -> {max_pitch}): {full_filename}")
                global_max_pitch = max_pitch
                
            if min_pitch < global_min_pitch:
                print(f"Global min updated ({global_min_pitch} -> {min_pitch}): {full_filename}")
                global_min_pitch = min_pitch

print(f"min pitch: {global_min_pitch}, max pitch: {global_max_pitch}")
