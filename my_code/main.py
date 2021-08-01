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
    'chords': sequences.get_chords_seq
}

def main(mode, key, len_each, len_track):

    f_name = f"Track_{mode}_{key}"

    # Initialize logging.
    logging.basicConfig(level=logging.INFO, filename=f_name+'.log')

    # 60 bpm single track Midi
    midi = Midi(number_tracks=1, tempo=60, instrument=40, channel=0)

    full_seq = _MODE_FUNC[mode](key=key)

    if mode == 'chords':
        midi.seq_chords(full_seq, track=0)
    else:
        midi.seq_notes(full_seq, track=0)

    midi.write(filename=f_name+'.mid')


if __name__ == '__main__':

    if not (len(sys.argv) == 5 and \
            sys.argv[1] in _MODE_FUNC.keys() and \
            re.match(r'[A-G](#|b)?(maj|min)$', sys.argv[2]) and \
            all(_.isnumeric() for _ in sys.argv[3:])):

        raise SyntaxError('Invalid command line!')
    raise Exception('Stop')

    main(*argv[1:])
