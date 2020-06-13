import re
import math
import pynbs
import struct
import os
import argparse

import mido

import instruments_map
import drum_set

index = [
    'note.harp',
    'note.bass',
    'note.bd',
    'note.snare',
    'note.hat',
    'note.guitar',
    'note.flute',
    'note.bell',
    'note.chime',
    'note.xylophone',
    'note.iron_xylophone',
    'note.cowbell',
    'note.didgeridoo',
    'note.bit',
    'note.banjo',
    'note.pling'
]


def getFloat(f):
    return struct.pack('<f', f)


def getInt(n):
    return struct.pack('<i', n)


def getShort(n):
    b = []
    for i in range(2):
        b.append((n >> (i << 3)) & 0xff)
    return bytes(b)


def getByte(b):
    return bytes([b])


def convert(file):
    with open(os.path.basename(file)[0:-4]+".mcs", 'wb') as f:
        insts = []
        notes = []

        insts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        mid = mido.MidiFile(file)
        for i, track in enumerate(mid.tracks):
            time = 0
            for j, msg in enumerate(track):
                time += msg.time
                print(j, msg)
                if msg.type == "program_change":
                    insts[msg.channel] = msg.program
                elif msg.type == "note_on" and msg.velocity != 0:
                    notes.append({
                        'time': time,
                        'instrument': index.index(instruments_map.inst_map[insts[msg.channel]][0]),
                        'key': msg.note
                    })

        notes.sort(key=lambda note: note.get('time'))

        multiplier = 10 / mid.ticks_per_beat

        # Magic
        f.write(bytes('MCSQ', encoding='utf-8'))
        # Version
        f.write(getShort(0))
        # Tempo Multiplier
        f.write(getFloat(multiplier))
        # Number of notes
        f.write(getInt(len(notes)))

        length = 0
        for i in range(len(notes)):
            note = notes[i]
            try:
                length = notes[i+1]['time'] - note['time']
            except:
                length = 1000

            f.write(getShort(length))                       # Note tick
            # Note instrument
            f.write(getByte(note['instrument']))
            f.write(getByte(note['key']))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str,
                        help='File')
    args = parser.parse_args()

    convert(args.file)
