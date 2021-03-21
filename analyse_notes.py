import sys
import pretty_midi


def pitch_to_note(midi_pitch):
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    notes_in_octave = 12

    octave_number = midi_pitch // notes_in_octave - 2
    note_in_octave = midi_pitch % notes_in_octave

    return notes[note_in_octave] + f"{octave_number}"


def create_chord(chords, pitch_start_time):
    '''
    TODO: make the epsilon sensitive to the track's average tempo

    chords[idx] will store the starting time of the first approached sound in a chord
    but 'the first approached' doesn't mean that this is exactly the chronogically first played sound in the chord
    the epsilon difference will refer to that starting time

    for example:
    (eps - first_sound - eps) ::: ... ::: last_sound
    first_sound ::: ... ::: (eps - n_sound - eps) ::: ... ::: last_sound
    first_sound ::: ... ::: (eps - last_sound - eps)
    '''
    chord_time_eps = 0.05

    for idx in chords:
        if abs(pitch_start_time - chords[idx]) <= chord_time_eps:
            return idx

    if chords != {}:
        new_chord_idx = list(chords.keys())[-1] + 1
    else:
        new_chord_idx = 0

    chords[new_chord_idx] = pitch_start_time
    return new_chord_idx


if len(sys.argv) == 2:
    filename = sys.argv[1]
else:
    filename = "maestro-v3.0.0/2018/MIDI-Unprocessed_Chamber3_MID--AUDIO_10_R3_2018_wav--1.midi"

midi_data = pretty_midi.PrettyMIDI(filename)

print(f"filename: {filename}")
print(f"duration: {midi_data.get_end_time()}")

header = f"{'note':^4} {'chord':^6} {'pitch':^5} {'start':^20} {'end':^20}"
print(header)

printed_notes_limit = 12
printed_notes_count = 0

chords = {}
for note in midi_data.instruments[0].notes:
    musical_note = pitch_to_note(note.pitch)
    chord_idx = create_chord(chords, note.start)

    start_color = "\033[" + f"{(chord_idx % 7 + 31)}" + "m"
    end_color = '\033[0m'

    print(f"{musical_note:<4} {start_color}{chord_idx:<6}{end_color} {note.pitch:<5} {note.start:<20} {note.end:<20}")

    printed_notes_count = printed_notes_count + 1
    if printed_notes_count >= printed_notes_limit:
        input("Continue? [enter]")
        printed_notes_count = 0
        print(header)
