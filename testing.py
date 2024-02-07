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
    nl = list(c.iter_notes())
    assert all( [nl[i].pitch <= nl[i+1].pitch for i in range(len(nl)-1)] )
    assert str(c) == 'Dmaj7 (D5, F#5, A5, C#6)'

    # note shifting in chords
    s = Score()
    s.setKey(Root.A, Mode.Minor)
    c = Chord(60, Mode.Major)
    assert c.allowed_in_scale()
    for n in c.iter_notes():
        n.shift_by_scale_steps(2)
    e = Chord(64, Mode.Minor)
    assert c == e







if __name__ == '__main__':
    print('chord generation')
    test_chords()