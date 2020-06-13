import re
import math
import pynbs
import struct
import os
import argparse

def getFloat(f):
    return struct.pack('<f',f)

def getInt(n):
    return struct.pack('<i',n)

def getShort(n):
    return struct.pack('<h',n)


def getByte(b):
    return bytes([b])

def convert(file):
    with open(os.path.basename(file)[0:-4]+".mcs", 'wb') as f:
        insts = []
        notes = []
        nbs = pynbs.read(file)
        print(nbs.header.tempo)

        multiplier = 20 / nbs.header.tempo

        # Magic
        f.write(bytes('MCSQ', encoding='utf-8'))
        # Version
        f.write(getShort(1))
        # Tempo Multiplier
        f.write(getFloat(multiplier))
        # Number of notes
        f.write(getInt(len(nbs.notes)))

        length = 0
        for i in range(len(nbs.notes)):
            note = nbs.notes[i]
            try:
                length = note.tick - nbs.notes[i-1].tick
            except:
                length = 1
            if length < 0:
                length = 0
            f.write(getShort(length))                       # Note tick
            # Note instrument
            f.write(getByte(note.instrument))
            f.write(getByte(note.key+21))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str,
                        help='File')
    args = parser.parse_args()

    convert(args.file)