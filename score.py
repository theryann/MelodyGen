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
    Major  = ' '
    Minor  = 'm'
    Dim    = 'dim'
    Major7 = 'maj7'
    Min7   = '7'
    Five   = '5'

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

class Note:
    note_names = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']

    def __init__(
            self,
            pitch: int = 0,
            duration: int = 1,
            start_time: int = 0
        ) -> None:

        self.pitch: int = pitch
        self.duration: int = duration
        self.start_time: int = start_time

    def __eq__(self, other: object) -> bool:
        ''' check wether pitch and duration are equal '''
        if not isinstance(other, Note):
            raise TypeError(f"'=' is not supported between Types 'Note' and '{type(other).__name__}'.")

        return (
            self.pitch == other.pitch and
            self.duration == other.duration
        )

    def __add__(self, other: object) -> bool:
        if not isinstance(other, int):
            raise TypeError(f"'+' is not supported between Types 'Note' and '{type(other).__name__}'. Only 'Note' + 'int'.")

        self.pitch += other
        self.checkPitchInRange()
        return self

    def __sub__(self, other: object) -> bool:
        if not isinstance(other, int):
            raise TypeError(f"'-' is not supported between Types 'Note' and '{type(other).__name__}'. Only 'Note' - 'int'.")

        self.pitch -= other
        self.checkPitchInRange()
        return self

    def __repr__(self) -> str:
        return f'{Note.note_names[self.pitch % 12]}{self.pitch // 12}'

    def checkPitchInRange(self) -> None:
        ''' check if pitch is still in midi bounds after addition '''
        if not 0 <= self.pitch <= 127:
            raise ValueError(f'Note pitch should be in [0..127]. It is {self.pitch}.')

    def is_same_note_as(self, other) -> bool:
        if not isinstance(other, Note):
            raise TypeError(f"check for same note can not happen between 'Note' and '{type(other).__name__}'. Only 'Note' and 'Note'.")
        return self.pitch % 12 == other.pitch % 12

class Chord:
    def __init__(
            self,
            root_pitch: int,
            mode: Mode = Mode.Major,
            duration: int = 1,
            start_time: int = 0
        ) -> None:
        self.note_list: list[Note] = []
        self.root_pitch = root_pitch
        self.mode = mode
        self.start_time: int = start_time
        self.duration: int = duration
        self.set_chord_notes()

    def set_chord_notes(self) -> None:
        ''' fill the notes in the chord note list on init '''
        # add tonica
        self.note_list.append( Note(pitch = self.root_pitch, duration=self.duration, start_time=self.start_time) )

        if self.mode == Mode.Dim:
            self.note_list.append( Note(pitch = self.root_pitch + 3, duration=self.duration, start_time=self.start_time) )
            self.note_list.append( Note(pitch = self.root_pitch + 6, duration=self.duration, start_time=self.start_time) )
            return

        # add dominant (V)
        self.note_list.append( Note(pitch = self.root_pitch + 7, duration=self.duration, start_time=self.start_time) )

        if self.mode == Mode.Five:
            return

        if self.mode in (Mode.Major, Mode.Min7, Mode.Major7):
            self.note_list.append( Note(pitch = self.root_pitch + 4, duration=self.duration, start_time=self.start_time) )
            if self.mode == Mode.Major:
                return
            if self.mode == Mode.Min7:
                self.note_list.append( Note(pitch = self.root_pitch + 10, duration=self.duration, start_time=self.start_time) )
            else:
                self.note_list.append( Note(pitch = self.root_pitch + 11, duration=self.duration, start_time=self.start_time) )

        elif self.mode == Mode.Minor:
            self.note_list.append( Note(pitch = self.root_pitch + 3, duration=self.duration, start_time=self.start_time) )


        self.note_list.sort(key=lambda n: n.pitch)

    def __repr__(self) -> str:
        return f'{Note.note_names[self.root_pitch % 12]}{self.mode.value} ({", ".join([str(n) for n in self.note_list])})'



c = Chord(66, Mode.Min7)
print(c)


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