import math
import random

from pyknon.music import Note, NoteSeq

import helpers, constants


def get_absolute_seq(key, len_note, total):

    all_notes = helpers.get_all_notes(key)
    seq_notes = random.choices(all_notes, k=total)

    duration = int(4/len_note)

    note_seq = NoteSeq()
    for note in seq_notes:
        dev_5  = 5 - random.choice((3,4,5))
        octave = "'" if not dev_5 else "," * dev_5
        note_seq.append(Note(f'{note}{duration}{octave}'))

    return note_seq


def get_relative_seq(key, len_note, total):

    all_notes = helpers.get_all_notes(key)
    seq_notes = random.choices(all_notes, k=total)

    duration = int(4/len_note)
    dev_5  = 5 - random.choice((3,4,5))
    octave = "'" if not dev_5 else "," * dev_5

    note_seq = NoteSeq()
    for note in seq_notes:
        note_seq.append(Note(f'{note}{duration}{octave}'))

    return note_seq


def get_chord_seq(key, len_chord, total):

    chords = helpers.get_all_chords(key)
    seq_chords = random.choices(chords, k=total)

    duration = int(4/len_note)

    Note_Seq = []
    for chord in seq_chords:
        dev_5  = 5 - constants.root_octaves[chord.root]
        octave = "'" if not dev_5 else "," * dev_5
        note_seq = NoteSeq(' '.join([f'{chord.root}{duration}{octave}', *chord.components[1:]]))
        Note_Seq.append(note_seq)

    return Note_Seq


def get_octave_seq(key, len_note):

    all_notes = helpers.get_all_notes(key)

    duration = int(4/len_note)
    dev_5  = 5 - random.choice((3,4,5))
    octave = "'" if not dev_5 else "," * dev_5

    note_seq = NoteSeq()
    for note in all_notes:
        note_seq.append(Note(f'{note}{duration}{octave}'))

    return note_seq


def get_harmonised_seq(key, len_chord):

    chords = helpers.get_all_chords(key)

    duration = int(4/len_note)

    Note_Seq = []
    for chord in chords:
        dev_5  = 5 - constants.root_octaves[chord.root]
        octave = "'" if not dev_5 else "," * dev_5
        note_seq = NoteSeq(' '.join([f'{chord.root}{duration}{octave}', *chord.components[1:]]))
        Note_Seq.append(note_seq)

    return Note_Seq

