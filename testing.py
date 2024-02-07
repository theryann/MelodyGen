from score import Chord, Note, Score, Mode, Root



def test_chords():
    # chord construction

    # major
    c = Chord(60, Mode.Major)
    assert c.root_pitch == 60
    assert c.mode == Mode.Major
    assert len(c.note_list) > 0
    assert str(c) == 'C  (C5, E5, G5)'

    # dim
    c = Chord(60, Mode.Dim)
    assert str(c) == 'Cdim (C5, D#5, F#5)'
    for n in c.iter_notes():
        assert isinstance(n, Note)

    # maj7
    c = Chord(62, Mode.Major7)
    # check if chordnotes are sorted by pitch
    assert str(c) == 'Dmaj7 (D5, F#5, A5, C#6)'

    # verify note ordering in chords for all modes
    for mode in Mode:
        f = Chord(65, mode)
        nl = list(f.iter_notes())
        assert all( [nl[i].pitch <= nl[i+1].pitch for i in range(len(nl)-1)] )


    # note shifting in chords
    s = Score()
    s.setKey(Root.A, Mode.Minor)
    c = Chord(60, Mode.Major)
    assert c.allowed_in_scale()
    for n in c.iter_notes():
        n.shift_by_scale_steps(2)
    e = Chord(64, Mode.Minor)

def test_notes():
    c = Note(60)
    g = Note(67)

    # check math oparators
    assert c != g
    assert c == Note(60)
    assert c != Note(60, duration=2)
    assert c + 7 == g
    assert Note(67) - 7 == Note(60)
    assert str(g) == 'G5'
    assert Note(60).is_same_note_as( Note(0) )

    # in scales
    s = Score().setKey(Root.C, Mode.Major)
    assert Note(0).shift_by_scale_steps(5) == Note(9)

    # test for value error on wrong notes
    try:
        Note(200).checkPitchInRange()
    except ValueError:
        pass
    try:
        Note(-2).checkPitchInRange()
    except ValueError:
        pass


if __name__ == '__main__':
    print('chord generation')
    test_chords()
    print('note opartions')
    test_notes()