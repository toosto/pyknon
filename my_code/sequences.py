import math
import random
import logging
import re

from pyknon.music import Note, NoteSeq
from pychord import utils

import helpers, constants, range_map


def get_absolute_seq(key, len_note, total):

    all_notes = helpers.get_all_notes(key)
    logging.debug('all the notes in the key are %s.', all_notes)
    seq_notes = random.choices(all_notes, k=total)

    duration = int(4/len_note)

    note_seq = NoteSeq()
    for note in seq_notes:
        dev_5 = 5 - random.choice((4, 5))
        octave = "'" * (abs(dev_5) + 1) if dev_5 <= 0 else "," * dev_5
        note_seq.append(Note(f'{note}{duration}{octave}'))

    return note_seq


def get_absolute_p_seq(key, len_note, total):

    all_notes = helpers.get_all_notes(key, pentatonic=True)
    logging.debug('all the notes in the key are %s.', all_notes)
    seq_notes = random.choices(all_notes, k=total)

    duration = int(4/len_note)

    note_seq = NoteSeq()
    for note in seq_notes:
        dev_5 = 5 - random.choice((4, 5))
        octave = "'" * (abs(dev_5) + 1) if dev_5 <= 0 else "," * dev_5
        note_seq.append(Note(f'{note}{duration}{octave}'))

    return note_seq


def get_relative_seq(key, len_note, total):

    all_notes = helpers.get_all_notes(key)
    logging.debug('all the notes in the key are %s.', all_notes)
    seq_notes = random.choices(all_notes, k=total)

    duration = int(4/len_note)
    # dev_5 = 5 - random.choice((4, 5))  # Can do 4,5,6 to get a higher octave.
    dev_5 = 0  # Middle octave always!
    octave = "'" * (abs(dev_5) + 1) if dev_5 <= 0 else "," * dev_5

    note_seq = NoteSeq()
    for note in seq_notes:
        note_seq.append(Note(f'{note}{duration}{octave}'))

    return note_seq


def get_relative_p_seq(key, len_note, total):

    duration = int(4/len_note)

    all_notes = helpers.get_all_notes(key, pentatonic=True)
    dev_5 = 5 - random.choice((4, 5))

    octave_tones = _get_octave_tones(dev_5, all_notes)
    all_notes = [Note(f'{tone[0]}{duration}{tone[1]}') for tone in octave_tones]

    note_seq = NoteSeq()
    for note in random.choices(all_notes, k=total):
        note_seq.append(note)

    return note_seq


def get_interval_seq(key, len_note, total):

    all_notes = helpers.get_all_notes(key, chromatic=True)
    logging.debug('all the notes in the key are %s.', all_notes)
    root_note = all_notes[0]
    seq_notes = [note for note in random.choices(all_notes, k=total) if note != root_note]

    duration = int(4/len_note)
    dev_5 = 5 - random.choice((4, 5))  # Can do 4,5,6 to get a higher octave.
    octave = "'" * (abs(dev_5) + 1) if dev_5 <= 0 else "," * dev_5

    note_seq = NoteSeq()
    for note in seq_notes:
        note_seq.append(Note(f'{root_note}{duration}{octave}'))
        note_seq.append(Note(f'{note}{duration}{octave}'))

    return note_seq


def get_chords_seq(key, len_chord, total):

    chords = helpers.get_all_chords(key)
    logging.debug('All the chords in the key are %s.', chords)
    seq_chords = random.choices(chords, k=total)
    higher_octave = True

    duration = int(4/len_chord)

    Note_Seq = []
    for chord in seq_chords:
        dev_5 = 5 - constants.root_octaves[chord.root] - int(higher_octave)
        octave = "'" * (abs(dev_5) + 1) if dev_5 <= 0 else "," * dev_5
        note_seq = NoteSeq(' '.join([f'{chord.root}{duration}{octave}', *chord.components()[1:]]))
        Note_Seq.append(note_seq)

    return Note_Seq


def get_octave_seq(key, len_note, *args):

    all_notes = list(helpers.get_all_notes(key))
    all_notes.append(all_notes[0])  # Completing the octave
    logging.debug('All the notes in the key are %s.', all_notes)

    duration = int(4/len_note)
    dev_5 = 5 - random.choice((3, 4, 5))

    note_seq = NoteSeq()
    prev_value = None
    for note in all_notes:
        note_val = utils.note_to_val(note)
        if prev_value is not None and note_val < prev_value:
            dev_5 -= 1
        octave = "'" * (abs(dev_5) + 1) if dev_5 <= 0 else "," * dev_5
        note_str = f'{note}{duration}{octave}'
        logging.info('Constructing Note with %s.', note_str)
        note_seq.append(Note(note_str))
        prev_value = note_val

    return note_seq


def get_harmonised_seq(key, len_chord, *args):

    chords = list(helpers.get_all_chords(key, dim=True))
    chords.append(chords[0])  # Completing the octave
    logging.debug('All the chords in the key are %s.', chords)

    duration = int(4/len_chord)
    dev_5 = 1

    Note_Seq = []
    prev_value = None
    for chord in chords:
        root_val = utils.note_to_val(chord.root)
        if prev_value is not None and root_val < prev_value:
            dev_5 -= 1
        octave = "'" * (abs(dev_5) + 1) if dev_5 <= 0 else "," * dev_5
        chord_str = ' '.join([f'{chord.root}{duration}{octave}', *chord.components()[1:]])
        logging.info('Constructing Chord with %s.', chord_str)
        note_seq = NoteSeq(chord_str)
        Note_Seq.append(note_seq)
        prev_value = root_val

    return Note_Seq


def _get_octave_tones(dev_5, all_notes):

    if dev_5 > 0:
        octave = dev_5 * ","
        ascend = True
    else:
        octave = (abs(dev_5) + 1) * "'"
        ascend = False

    tones = [(_, octave) for _ in all_notes]

    tone_indices = tuple(range_map.RANGE_MAP["".join(_)] for _ in tones)

    if ascend:
        ext_tone_index = min(tone_indices) + 12
    else:
        ext_tone_index = max(tone_indices) - 12

    for key, value in range_map.RANGE_MAP.items():
        if value == ext_tone_index:
            tones.append(re.match(r"([A-Zb#]+)('+|,+)", key).groups())

    return tones
