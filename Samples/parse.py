import re
import math

pattern = '@s\[scores=\{song3039474755=(\d+)\}\]'


def getInt(n):
    b = []
    for i in range(4):
        b.append((n >> (i << 3)) & 0xff)
    return bytes(b)


def getShort(n):
    b = []
    for i in range(2):
        b.append((n >> (i << 3)) & 0xff)
    return bytes(b)


def getByte(b):
    return bytes([b])


with open('file.mcs', 'wb') as f:
    insts = []
    notes = []
    with open('playing.mcfunction') as f2:
        txt = f2.read()
        cmds = txt.split('\n')
        for i in cmds:
            args = i.split(' ')
            if args[0] == 'playsound':
                instrument = args[1]
                if not instrument in insts:
                    insts.append(instrument)
                tick = int(re.search(pattern, args[2]).group(1))
                pitch = float(args[7])
                notes.append({
                    'instrument': instrument,
                    'tick': tick,
                    'pitch': round(math.log(pitch, 2)*12+66)
                })

    # Magic
    f.write(bytes('MCSQ', encoding='utf-8'))
    # Version
    f.write(getShort(0))
    # Number of instruments
    f.write(getShort(len(insts)))
    for i in range(len(insts)):
        instrument = insts[i]
        # Instrument name
        f.write(bytes(instrument, encoding='utf-8'))
        # End of instrument name
        f.write(b'\x00')
    # Number of notes
    f.write(getInt(len(notes)))

    delta=0
    for note in notes:
        print(note)
        delta=note['tick']-delta
        f.write(getShort(delta))                       # Note tick
        f.write(getShort(insts.index(note['instrument'])))  # Note instrument
        f.write(getByte(note['pitch']))                     # Note pitch
