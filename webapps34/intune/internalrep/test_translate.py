import unittest

from hamcrest import *

from intune.internalrep.ir import RegNote, RestNote, Segment, Note
from intune.internalrep.irdefs import Pitch
from intune.internalrep.translate import NoteEncoder, SegEncoder


class IRTranslateTestCase(unittest.TestCase):

    def test_encode_pitch(self):
        pitch = Pitch.C
        expected = "C"
        encoded_pitch = NoteEncoder.encode_pitch(pitch)
        self.assertEqual(encoded_pitch, expected)

    def test_encode_duration(self):
        duration = 4
        expected = "q"
        encoded_duration = NoteEncoder.encode_duration(duration)
        self.assertEqual(encoded_duration, expected)

    def test_encode_reg_note(self):
        note = RegNote.default_construct()
        encoded_note = NoteEncoder.encode_reg_note(note)
        expected = {NoteEncoder.DURATION: "w",
                    NoteEncoder.KEYS: ["C"]}
        self.assertTrue(isinstance(encoded_note, dict))
        assert_that(encoded_note, has_entries(expected))

    def test_encode_rest_note(self):
        note = RestNote(4)
        encoded_note = NoteEncoder.encode_rest_note(note)
        expected = {NoteEncoder.DURATION: "qr",
                    NoteEncoder.KEYS: [NoteEncoder.DEF_REST_POS]}
        self.assertTrue(isinstance(encoded_note, dict))
        assert_that(encoded_note, has_entries(expected))

    def test_encode_segment(self):
        expected = {SegEncoder.CLEF: "treble",
                    SegEncoder.NOTES: [
                        {NoteEncoder.DURATION: "q",
                         NoteEncoder.KEYS: ["C"]},
                        {NoteEncoder.DURATION: "q",
                         NoteEncoder.KEYS: ["D"]},
                        {NoteEncoder.DURATION: "q",
                         NoteEncoder.KEYS: ["E"]},
                        {NoteEncoder.DURATION: "q",
                         NoteEncoder.KEYS: ["F"]}
                    ]
                    }

        segment = Segment.default_construct()
        segment.add_note(0, RegNote(4, Pitch.C, 4))
        segment.add_note(1, RegNote(4, Pitch.D, 4))
        segment.add_note(2, RegNote(4, Pitch.E, 4))
        segment.add_note(3, RegNote(4, Pitch.F, 4))

        encoded_seg = SegEncoder.encode_seg(segment)
        self.assertTrue(isinstance(encoded_seg, dict))
        assert_that(encoded_seg, has_entries(expected))


if __name__ == '__main__':
    unittest.main()
