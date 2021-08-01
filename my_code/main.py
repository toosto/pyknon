#!python
import sys
sys.path.append('/home/tushar/music_programming/repos/pyknon/')

import logging
import re

from pyknon.genmidi import Midi

import sequences

_MODE_FUNC = {
    'absolute': sequences.get_absolute_seq,
    'relative': sequences.get_relative_seq,
    'chords': sequences.get_chords_seq,
    'octave': sequences.get_octave_seq,
    'harmonised': sequences.get_harmonised_seq
}

def main(mode, key, tempo, len_each, total):

    f_path = f"/home/tushar/shared_folder/Midi_tracks/Track_{mode}_{key}_{tempo}_{len_each}_{total}"

    # Initialize logging.
    # logging.basicConfig(level=logging.INFO, filename=f_path+'.log')
    logging.basicConfig(level=logging.DEBUG, filename=f_path+'.log')

    # 60 bpm single track Midi
    midi = Midi(number_tracks=1, tempo=tempo, instrument=40, channel=0)

    full_seq = _MODE_FUNC[mode](key, len_each, total)
    logging.debug('Full sequence created is:\n%s', full_seq)

    if mode in ('chords', 'harmonised'):
        midi.seq_chords(full_seq, track=0)
    else:
        midi.seq_notes(full_seq, track=0)

    midi.write(filename=f_path+'.mid')


if __name__ == '__main__':

    if not (len(sys.argv) == 6 and \
            sys.argv[1] in _MODE_FUNC.keys() and \
            re.match(r'[A-G](#|b)?(maj|min)$', sys.argv[2]) and \
            all(_.isnumeric() for _ in sys.argv[3:])) and \
            int(sys.argv[4]) in {1, 2, 4}:

        raise SyntaxError('Invalid command line!')
    raise Exception('Stop')

    main(*argv[1:])
