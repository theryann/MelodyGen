from midiutil import MIDIFile
from enum import Enum


#
# GUIDE
#
# - verschiedene Instrumente/Spuren bekommen je eigene 'channel' (tracks sind irrelevant)
# - die duration beschreibt die Notenlänge in beats. 1 beat ist eine Viertelnote (also idR. 4 beats pro Takt)
# - time ist der Startzeitpunkt in beats seit 0
# - pitch in Halbtonschritten. 60 ist middle C
# - track sollte immer 0 sein. ka was das genau bedeutet

class Chord(Enum):
    C = 0
    Csharp = 1
    D = 2
    Dsharp = 3
    E = 4
    F = 5
    Fsharp = 6
    G = 7
    Gsharp = 8
    A = 9
    Asharp = 10
    B = 11

class Mode(Enum):
    Major = 0
    Minor = 0
    Dim = 0
    Major7 = 0
    Min7 = 0

class customMIDIFile(MIDIFile):
    def __init__(self) -> None:
        super().__init__(1)

    def addChord(self, root: Chord, mode: Mode):
        pass

mf = customMIDIFile()

print(mf)

mf.addTempo(
    track=0,
    time=0,
    tempo=130
)

mf.addNote(track=0, channel=0, time=0, pitch=60, duration=2, volume=64)
mf.addNote(track=0, channel=0, time=0, pitch=64, duration=2, volume=64)
mf.addNote(track=0, channel=0, time=0, pitch=67, duration=2, volume=64)
mf.addNote(track=0, channel=0, time=4, pitch=60, duration=2, volume=64)
# mf.addNote(track=0, channel=1, time=0, pitch=60, duration=1, volume=100)


with open('test.mid', 'wb') as out_file:
    mf.writeFile(out_file)