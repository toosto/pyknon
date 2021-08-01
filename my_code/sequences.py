import math
import random
import logging

from pyknon.music import Note, NoteSeq
from pychord import utils

import helpers, constants


def get_absolute_seq(key, len_note, total):

    all_notes = helpers.get_all_notes(key)
    logging.debug('All the notes in the key are %s.', all_notes)
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
    logging.debug('All the notes in the key are %s.', all_notes)
    seq_notes = random.choices(all_notes, k=total)

    duration = int(4/len_note)
    dev_5  = 5 - random.choice((3,4,5))
    octave = "'" if not dev_5 else "," * dev_5

    note_seq = NoteSeq()
    for note in seq_notes:
        note_seq.append(Note(f'{note}{duration}{octave}'))

    return note_seq


def get_chords_seq(key, len_chord, total):

    chords = helpers.get_all_chords(key)
    logging.debug('All the chords in the key are %s.', chords)
    seq_chords = random.choices(chords, k=total)

    duration = int(4/len_chord)

    Note_Seq = []
    for chord in seq_chords:
        dev_5  = 5 - constants.root_octaves[chord.root]
        octave = "'" if not dev_5 else "," * dev_5
        note_seq = NoteSeq(' '.join([f'{chord.root}{duration}{octave}', *chord.components()[1:]]))
        Note_Seq.append(note_seq)

    return Note_Seq


def get_octave_seq(key, len_note, *args):

    all_notes = helpers.get_all_notes(key)
    logging.debug('All the notes in the key are %s.', all_notes)

    duration = int(4/len_note)
    dev_5 = 5 - random.choice((2, 3, 4))

    note_seq = NoteSeq()
    done_once = False
    for note in all_notes:
        if utils.note_to_val(note) >= 0 and not done_once:
            dev_5 -= 1
            done_once = True
        octave = "'" * (abs(dev_5) + 1) if dev_5 <= 0 else "," * dev_5
        note_str = f'{note}{duration}{octave}'
        logging.info('Constructing Note with %s.', note_str)
        note_seq.append(Note(note_str))

    return note_seq


def get_harmonised_seq(key, len_chord, *args):

    chords = helpers.get_all_chords(key)
    logging.debug('All the chords in the key are %s.', chords)
    duration = int(4/len_chord)

    Note_Seq = []
    for chord in chords:
        dev_5  = 5 - constants.root_octaves[chord.root]
        octave = "'" if not dev_5 else "," * dev_5
        note_seq = NoteSeq(' '.join([f'{chord.root}{duration}{octave}', *chord.components()[1:]]))
        Note_Seq.append(note_seq)

    return Note_Seq

