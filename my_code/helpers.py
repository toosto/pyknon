from pychord import Chord
from pyknon.music import NoteSeq

import constants


def get_all_chords(root=None):

    all_chords = [
        Chord('Em'),
        Chord('F#dim'),
        Chord('G'),
        Chord('Am'),
        Chord('Bm'),
        Chord('C'),
        Chord('D')
    ]

    return all_chords


def chords_to_noteseq(chords):

    note_seqs = []
    for chord in chords:
        root_pitch = constants.root_octaves[chord.root]
        components_with_pitch = chord.components_with_pitch(root_pitch=root_pitch)
        note_seq = NoteSeq(' '.join(components_with_pitch))
        note_seqs.append(note_seq)

    return note_seqs

