import re
import math
import pynbs
import struct
import os
import argparse
import mido
import gzip


def getFloat(f):
    return struct.unpack('<f', f)


def getInt(n):
    return struct.unpack('<i', n)


def getShort(n):
    return struct.unpack('<h', n)


def getByte(b):
    return bytes([b])


programs = [0, 32, 24, 73, 11, 11, 13, 112, 112, 0, 29, 80, 105, 2, 0, 0]
offset = [0, -24, 0, 0, 0, -12, 12, 24, 36, 0, 0, 0, 0, 0, 0, 0]


def getChannel(inst):
    if inst < 2:
        return inst
    elif inst == 2 or inst == 3 or inst == 4:
        return 9
    else:
        return inst-3


def convert(string):
    if(string.endswith('.mcz')):
        f = gzip.open(string)
    else:
        f = open(string, 'rb')
    f.seek(4)
    version = getShort(f.read(2))[0]
    tempo = getFloat(f.read(4))[0]
    length = getInt(f.read(4))[0]
    mid = mido.MidiFile()
    tracks = []
    deltas=[]
    for i in range(16):
        track = mido.MidiTrack()
        track.append(mido.Message('program_change',
                                  program=programs[i], channel=i))
        tracks.append(track)
        mid.tracks.append(track)
        deltas.append(0)
    tracks[0].append(mido.MetaMessage('set_tempo', tempo=int(200000*tempo)))
    notes = []
    for i in range(length):
        delta = getShort(f.read(2))[0]
        inst = f.read(1)[0]
        pitch = f.read(1)[0]
        ch = getChannel(inst)
        if delta > 0:
            for j in range(16):
                deltas[j] += delta
            for j in range(0, len(notes)):
                element = notes[j]
                ch2 = getChannel(element[0])
                print(deltas)
                if j == 0:
                    tracks[0].append(mido.Message('note_off', note=element[1]+offset[element[0]],
                                                  velocity=0, time=deltas[ch2]*120, channel=ch2))
                else:
                    tracks[0].append(mido.Message('note_off', note=element[1]+offset[element[0]],
                                                  velocity=0, time=0, channel=ch2))
            notes.clear()
        deltas[ch] = 0
        if not (inst >= 2 and inst <= 4):
            tracks[0].append(mido.Message('note_on', note=pitch+offset[inst],
                                          velocity=100, time=0, channel=ch))
            notes.append([inst, pitch])
        elif inst == 2:
            note = 36
            if pitch > 66:
                note=37
            tracks[0].append(mido.Message('note_on', note=note,
                                          velocity=100, time=0, channel=9))
            notes.append([inst, note])
        elif inst == 3:
            note = 38
            if pitch > 66:
                note=42
            tracks[0].append(mido.Message('note_on', note=note,
                                          velocity=100, time=0, channel=9))
            notes.append([inst, note])
        elif inst == 4:
            tracks[0].append(mido.Message('note_on', note=39,
                                          velocity=100, time=0, channel=9))
            notes.append([inst, 39])

    print(version, tempo, length)
    mid.save('test.mid')
    f.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('string', type=str,
                        help='String')
    args = parser.parse_args()

    convert(args.string)
