import re
import math
import pynbs
import struct
import os
import argparse

_map = 'a_b[cd~e;f1gh2i3jk4l5m6no7p8qr9s0t"uv,w.xy?z'


def getFloat(f):
    return struct.pack('<f', f)


def getInt(n):
    return struct.pack('<i', n)


def getShort(n):
    return struct.pack('<h', n)


def getByte(b):
    return bytes([b])


def convert(string):
    with open("out.mcs", 'wb') as f:
        notes = []
        ticking = True
        tick = 0
        for i in string:
            if i == '(':
                ticking = False
            elif i == ')':
                ticking = True
            else:
                try:
                    notes.append({
                        'time': tick,
                        'instrument': 0,
                        'key': _map.index(i.lower())+48
                    })
                except:
                    pass
            if ticking:
                tick += 1

        notes.sort(key=lambda note: note.get('time'))

        multiplier = 5

        # Magic
        f.write(bytes('MCSQ', encoding='utf-8'))
        # Version
        f.write(getShort(1))
        # Tempo Multiplier
        f.write(getFloat(multiplier))
        # Number of notes
        f.write(getInt(len(notes)))

        length = 0
        for i in range(len(notes)):
            note = notes[i]
            try:
                length = note['time'] - notes[i-1]['time']
            except:
                length = 1
            
            if length < 0:
                length = 0

            f.write(getShort(length))                       # Note tick
            # Note instrument
            f.write(getByte(note['instrument']))
            f.write(getByte(note['key']))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('string', type=str,
                        help='String')
    args = parser.parse_args()

    convert(args.string)
