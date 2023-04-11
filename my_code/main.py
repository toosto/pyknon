#!/usr/bin/env python3
import sys
sys.path.append('/home/parallels/repos/pyknon')

import logging
import re

from pyknon.genmidi import Midi

import sequences

_MODE_FUNC = {
    'absolute': sequences.get_absolute_seq,
    'absolute_p': sequences.get_absolute_p_seq,
    'relative': sequences.get_relative_seq,
    'relative_p': sequences.get_relative_p_seq,
    'interval': sequences.get_interval_seq,
    'chords': sequences.get_chords_seq,
    'octave': sequences.get_octave_seq,  # Debugging
    'harmonised': sequences.get_harmonised_seq  # Debugging
}

def main(mode, key, tempo, len_each, total):

    f_path = f"/home/parallels/shared_folder/midi_tracks/Track_{mode}_{key}_{tempo}_{len_each}_{total}"

    # Initialize logging.
    # logging.basicConfig(level=logging.INFO, filename=f_path+'.log')
    logging.basicConfig(level=logging.DEBUG, filename=f_path+'.log', filemode='w', format='%(message)s')

    # 60 bpm single track Midi
    midi = Midi(number_tracks=1, tempo=tempo, instrument=26, channel=0)

    full_seq = _MODE_FUNC[mode](key, len_each, total)

    len_ = len(full_seq)
    for index, item in enumerate(full_seq):
        logging.debug(f'{(100/len_) * (index + 1)}: {item}')

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
        # E.g. python3 main.py relative_p Amin 60 4 120
        # Am pentatonic single octave, whole notes at 60 BPM

    mode = sys.argv[1]
    key = sys.argv[2]
    tempo = int(sys.argv[3])
    len_each = int(sys.argv[4])
    total = int(sys.argv[5])

    main(mode, key, tempo, len_each, total)
