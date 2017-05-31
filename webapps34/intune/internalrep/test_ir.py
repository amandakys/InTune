import unittest

from intune.internalrep.ir import RegNote, RestNote, Composition, Segment
from intune.internalrep.irdefs import Pitch, Accidental


class RegNoteBasicTestCase(unittest.TestCase):

    def setUp(self):
        # Default Note: C4-1
        self.note = RegNote.defaultconstruct()

    def test_defaultconstructor(self):
        # Attribute Checks
        self.assertEqual(self.note.duration, RegNote.DEFAULT_DURATION,
                         "Default note duration should be " +
                         str(RegNote.DEFAULT_DURATION) +
                         " but got " +
                         str(self.note.duration))
        self.assertEqual(self.note.pitch, Pitch.C,
                         "Default note pitch should be " +
                         str(RegNote.DEFAULT_PITCH) +
                         " but got " +
                         self.note.pitch.name)
        self.assertEqual(self.note.octave, RegNote.DEFAULT_OCTAVE,
                         "Default note octave should be " +
                         str(RegNote.DEFAULT_OCTAVE) +
                         " but got " +
                         str(self.note.octave))

    def test_octavelowerbound(self):
        note = RegNote(1, Pitch.C, RegNote.MIN_OCTAVE)
        note.modoctave(-1)
        self.assertTrue(note.octave >= RegNote.MIN_OCTAVE)

    def test_octaveupperbound(self):
        note = RegNote(1, Pitch.C, RegNote.MAX_OCTAVE)
        note.modoctave(1)
        self.assertTrue(note.octave <= RegNote.MAX_OCTAVE)

    def test_setoctave(self):
        test = 2
        self.note.setoctave(test)
        self.assertEqual(self.note.octave, test)

    def test_setpitch(self):
        test = Pitch.D
        self.note.setpitch(test)
        self.assertEqual(self.note.pitch, test)

    def test_setaccidental(self):
        test = Accidental.FLAT
        self.note.setaccidental(test)
        self.assertEqual(self.note.accidental, test)

    def test_delnote(self):
        initduration = self.note.duration
        note = self.note.delnote()
        self.assertTrue(isinstance(note, RestNote))
        self.assertEqual(note.duration, initduration)


class RegNoteAdvTestCase(unittest.TestCase):
    pass


class SegmentBasicTestCase(unittest.TestCase):

    def setUp(self):
        self.composition = Composition.defaultconstruct()

    def test_addsegment(self):
        segment = Segment()
        self.composition.addsegment(segment)
        self.assertTrue(segment in self.composition.segments)

    def test_delsegment(self):
        # All composition has at least one segment
        seg0 = self.composition.segments[0]
        seg1 = Segment()
        seg2 = Segment()
        seg3 = Segment()
        seglist = [seg1, seg2, seg3]
        test = [seg0, seg1, seg3]
        self.composition.segments += seglist
        self.composition.delsegment(2)
        self.assertTrue(all(x in self.composition.segments for x in test))


class SegmentNotesTestCase(SegmentBasicTestCase):

    def setUp(self):
        self.composition = Composition.defaultconstruct()
        note = RegNote.defaultconstruct()
        segments = self.composition.segments
        segments[0].addnote(0, note)

    def test_addnotetoseg0(self):
        note = RegNote.defaultconstruct()
        note.setpitch(Pitch.D)
        self.composition.segments[0].addnote(1, note)
        self.assertTrue(note in self.composition.segments[0].notes)

    def test_changenote(self):
        segment = self.composition.segments[0]
        note = segment.notes[0]
        test = Pitch.F
        note.setpitch(test)
        pitch = segment.notes[0].pitch
        self.assertTrue(note in self.composition.segments[0].notes)
        self.assertEqual(pitch, test)


if __name__ == '__main__':
    unittest.main()
