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
    notes = []
    for i in range(16):
        track = mido.MidiTrack()
        track.append(mido.Message('program_change',
                                  program=programs[i], channel=i))
        tracks.append(track)
        mid.tracks.append(track)
        notes.append([])
    tracks[0].append(mido.MetaMessage('set_tempo', tempo=int(200000*tempo)))
    tick = 0
    for i in range(length):
        delta = getShort(f.read(2))[0]
        inst = f.read(1)[0]
        pitch = f.read(1)[0]
        ch = getChannel(inst)
        tick += delta
        notes[ch].append({'note': pitch, 'inst': inst, 'tick': tick})

    for i in range(len(notes)):
        e1 = notes[i]
        tempnote = []
        timedelta = 0
        playing = False
        delay = 0
        for j in range(len(e1)):
            e2 = e1[j]
            if j == 0:
                delta = e2['tick']
            else:
                delta = e2['tick'] - e1[j-1]['tick']
            if delta > 0:
                for k in range(len(tempnote)):
                    element = tempnote[k]
                    ch2 = getChannel(element[0])
                    if delta > 4:
                        t = 480
                        delay = t
                        playing = False
                    else:
                        t=delta*120
                    if k == 0:
                        tracks[ch2].append(mido.Message('note_off', note=element[1]+offset[element[0]],
                                                        velocity=0, time=t, channel=ch2))
                    else:
                        tracks[ch2].append(mido.Message('note_off', note=element[1]+offset[element[0]],
                                                        velocity=0, time=0, channel=ch2))
                tempnote.clear()

            ch = getChannel(e2['inst'])

            if not playing:
                timedelta = delta * 120 - delay
                print(delta,timedelta)
                playing = True
            else:
                timedelta = 0

            if not (e2['inst'] >= 2 and e2['inst'] <= 4):
                tracks[ch].append(mido.Message('note_on', note=e2['note']+offset[e2['inst']],
                                               velocity=100, time=timedelta, channel=ch))
                tempnote.append([e2['inst'], e2['note']])
            elif e2['inst'] == 2:
                note = 36
                if e2['note'] > 66:
                    note = 37
                tracks[ch].append(mido.Message('note_on', note=note,
                                               velocity=100, time=timedelta, channel=ch))
                tempnote.append([e2['inst'], note])
            elif e2['inst'] == 3:
                note = 38
                if e2['note'] > 66:
                    note = 42
                tracks[ch].append(mido.Message('note_on', note=note,
                                               velocity=100, time=timedelta, channel=ch))
                tempnote.append([e2['inst'], note])
            elif e2['inst'] == 4:
                tracks[ch].append(mido.Message('note_on', note=39,
                                               velocity=100, time=timedelta, channel=ch))
                tempnote.append([e2['inst'], 39])


    print(version, tempo, length)
    mid.save('test2.mid')
    f.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('string', type=str,
                        help='String')
    args = parser.parse_args()

    convert(args.string)
