from midiutil import MIDIFile
from enum import Enum
from random import randint

#
# GUIDE
#
# - verschiedene Instrumente/Spuren bekommen je eigene 'channel' (tracks sind irrelevant)
# - die duration beschreibt die Notenlänge in beats. 1 beat ist eine Viertelnote (also idR. 4 beats pro Takt)
# - time ist der Startzeitpunkt in beats seit 0
# - pitch in Halbtonschritten. 60 ist middle C
# - track sollte immer 0 sein. ka was das genau bedeutet

class Root(Enum):
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
    Minor = 1
    Dim = 2
    Major7 = 3
    Min7 = 4

class SectionRole(Enum):
    Intro = 0
    Verse = 1
    PreChorus = 2
    Chorus = 3
    PostChorus = 4
    Bridge = 5

class Instrument(Enum):
    Chords = 0
    Vocals = 1
    Piano  = 2
    Guitar = 3
    Bass   = 4

class Section:
    def __init__(
            self,
            section_role: SectionRole,
            start_time: int,
            bars: int = 4
        ) -> None:

        self.section_role: SectionRole = section_role
        self.start_time: int = start_time
        self.bars: int = bars

    def __len__(self) -> int:
        ''' returns this sections length in bars '''
        return self.bars



class Score:
    # static variables so all sections know which instruments and pitches they can use.
    # They don't HAVE to use every instrument though, depending of the section role (intro, chorus, ...)
    available_instruments: list[Instrument] = []
    available_notes: list[int] = []

    def __init__(self) -> None:
        self.section_list: list[Section]
        self.key: tuple[int, int]

    def setKey(
            self,
            root: Root = None,
            mode: Mode = None
        ) -> None:
        ''' sets the key for the score and generates a list of all pitches that lie within the key '''

        if root is None or mode is None:
            # random root note and random major minor choice. Other modes maybe in the future
            self.key = ( randint(0, 11), randint(0, 1) )
        else:
            self.key = (root, mode)

        # create allowed pitches
        scale_notes: set[int]

        if mode == Mode.Major:
            scale_notes = { 0, 2, 4, 5, 7, 9, 11 }
        elif mode == Mode.Minor:
            scale_notes = { 0, 2, 3, 5, 7, 8, 10 }

        scale_notes = { (root.value + s) % 12 for s in scale_notes }

        Score.available_notes = [ n for n in range(0, 128) if n % 12 in scale_notes  ]

    def generateSections() -> None:
        ...


    def append(self, section: Section) -> None:
        self.section_list.append(section)

    def saveMidi() -> None:
        ...



score = Score()
score.setKey(Root.D, Mode.Minor)
print(score.available_notes)



# mf.addTempo(
#     track=0,
#     time=0,
#     tempo=130
# )

# mf.addNote(track=0, channel=0, time=0, pitch=60, duration=2, volume=64)
# mf.addNote(track=0, channel=0, time=0, pitch=64, duration=2, volume=64)
# mf.addNote(track=0, channel=0, time=0, pitch=67, duration=2, volume=64)
# mf.addNote(track=0, channel=0, time=4, pitch=60, duration=2, volume=64)
# # mf.addNote(track=0, channel=1, time=0, pitch=60, duration=1, volume=100)


# with open('test.mid', 'wb') as out_file:
#     mf.writeFile(out_file)