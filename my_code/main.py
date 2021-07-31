import sys
sys.path.append('/home/tushar/music_programming/repos/pyknon/')

from pyknon.genmidi import Midi

import helpers
import constants

def main():

    all_chords = helpers.get_all_chords()
    all_note_seqs = helpers.chords_to_noteseq(all_chords)

    midi = Midi(1, tempo=60, instrument=[40])
    midi.seq_chords(all_note_seqs, track=0)

    midi.write("Track_1_Em.mid")

if __name__ == '__main__':
    main()
