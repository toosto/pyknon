#!/usr/bin/env python3
import sys
sys.path.append('/home/parallels/repos/pyknon')

import logging
import re
import time

from pyknon.genmidi import Midi

import sequences

_MODE_FUNC = {
    'absolute': (sequences.get_absolute_seq, 2),
    'absolute_p': (sequences.get_absolute_p_seq, 2),
    'relative': (sequences.get_relative_seq, 2),
    'relative_p': (sequences.get_relative_p_seq, 2),
    'interval': (sequences.get_interval_seq, 2),
    'chords': (sequences.get_chords_seq, 48),
    'octave': (sequences.get_octave_seq, 2),  # Debugging
    'harmonised': (sequences.get_harmonised_seq, 48)  # Debugging
}

def main(mode, key, tempo, len_each, total):

    random_str = str(time.time()).split('.')[1]

    f_path = f"/home/parallels/shared_folder/midi_tracks/Track_{mode}_{key}_{tempo}_{len_each}_{total}_{random_str}"

    # Initialize logging.
    logging.basicConfig(level=logging.DEBUG, filename=f_path+'.log', filemode='w', format='%(message)s')

    func, instrument = _MODE_FUNC[mode]
    # 60 bpm single track Midi
    midi = Midi(number_tracks=1, tempo=tempo, instrument=instrument, channel=0)  # String ensemble 1

    full_seq = func(key, len_each, total)

    len_ = len(full_seq)
    for index, item in enumerate(full_seq):
        logging.info(item)

    if mode in ('chords', 'harmonised'):
        midi.seq_chords(full_seq, track=0)
    else:
        midi.seq_notes(full_seq, track=0)

    midi.write(filename=f_path+'.mid')


if __name__ == '__main__':

    if not (len(sys.argv) == 6 and \
            sys.argv[1] in _MODE_FUNC.keys() and \
            re.match(r'[A-G](#|b)?(maj|min)$', sys.argv[2]) and \
            all(_.isnumeric() for _ in sys.argv[3:]) and \
            int(sys.argv[4]) in {1, 2, 4}):

        raise SyntaxError('Invalid command line!')
        # E.g. python3 main.py relative_p Amin 120 4 60
        # Am pentatonic single octave, 60 whole notes at 120 BPM

    mode = sys.argv[1]
    key = sys.argv[2]
    tempo = int(sys.argv[3])
    len_each = int(sys.argv[4])
    total = int(sys.argv[5])

    main(mode, key, tempo, len_each, total)
