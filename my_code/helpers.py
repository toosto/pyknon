import logging

from pychord import utils, Chord


def get_tonic_type(key):
    return key[:-3], key[-3:]

def get_all_notes(key):

    tonic, type_key = get_tonic_type(key)
    logging.debug('Tonic: %s, type of key: %s', tonic, type_key)

    tonic_c_offset = utils.note_to_val(tonic)

    intervals = {
        'maj': (0, 2, 4, 5, 7, 9, 11),
        'min': (0, 2, 3, 5, 7, 8, 10)
    }

    all_notes = tuple(utils.val_to_note(tonic_c_offset + _, tonic) for _ in intervals[type_key])

    return all_notes


def get_all_chords(key):

    tonic, type_key = get_tonic_type(key)
    logging.debug('Tonic: %s, type of key: %s', tonic, type_key)

    qualities = {
        'maj': ('maj', 'min', 'min', 'maj', 'maj', 'min', 'dim'),
        'min': ('min', 'dim', 'maj', 'min', 'min', 'maj', 'maj')
    }

    chords = tuple(Chord.from_note_index(note=_+1, quality=qualities[type_key][_], scale=key) for _ in range(0, 7))

    return chords
