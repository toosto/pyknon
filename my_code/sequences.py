import math
import random

import helpers

def get_absolute_seq(key, len_note, len_track):

    all_notes = list(helpers.get_all_notes(key))

    iterations = math.ceil(len_track/(len_note*len(all_notes)))

    seq_notes = []
    for _ in range(iterations+1):
        random.shuffle(all_notes)
        seq_notes.extend(all_notes)

    # Add pitches
    pitches = ('3', '4', '5')
    seq_notes = tuple(_+random.choice(pitches) for _ in seq_notes)


def get_relative_seq(key, len_note, len_track):
    pass


def get_chord_seq(key, len_chord, len_track):

    chords = helpers.get_all_chords(root=root)

    note_seqs = []
    for chord in chords:
        root_pitch = constants.root_octaves[chord.root]
        components_with_pitch = chord.components_with_pitch(root_pitch=root_pitch)
        note_seq = NoteSeq(' '.join(components_with_pitch))
        note_seqs.append(note_seq)

    return note_seqs

