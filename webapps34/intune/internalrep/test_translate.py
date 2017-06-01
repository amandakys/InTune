import unittest

from hamcrest import *

from intune.internalrep.ir import RegNote, RestNote, Segment, IRScore
from intune.internalrep.jsoncodec.irscore_codec import *
from intune.internalrep.jsoncodec.note_codec import *
from intune.internalrep.jsoncodec.seg_codec import *


class IRTranslateTestCase(unittest.TestCase):
    def test_encode_pitch(self):
        pitch = Pitch.C
        expected = "C"
        encoded_pitch = encode_pitch(pitch)
        self.assertEqual(encoded_pitch, expected)

    def test_encode_duration(self):
        duration = 4
        expected = "q"
        encoded_duration = encode_duration(duration)
        self.assertEqual(encoded_duration, expected)

    def test_encode_reg_note(self):
        note = RegNote.default_construct()
        encoded_note = encode_reg_note(note)
        expected = {DURATION: "w",
                    KEYS: ["C"]}
        self.assertTrue(isinstance(encoded_note, dict))
        assert_that(encoded_note, has_entries(expected))

    def test_encode_rest_note(self):
        note = RestNote(4)
        encoded_note = encode_rest_note(note)
        expected = {DURATION: "qr",
                    KEYS: [DEF_REST_POS]}
        self.assertTrue(isinstance(encoded_note, dict))
        assert_that(encoded_note, has_entries(expected))

    def test_encode_segment(self):
        expected = {CLEF: "treble",
                    NOTES: [
                        {DURATION: "q", KEYS: ["C"]},
                        {DURATION: "q", KEYS: ["D"]},
                        {DURATION: "q", KEYS: ["E"]},
                        {DURATION: "q", KEYS: ["F"]}
                    ]}

        segment = Segment.default_construct()
        segment.add_note(0, RegNote(4, Pitch.C, 4))
        segment.add_note(1, RegNote(4, Pitch.D, 4))
        segment.add_note(2, RegNote(4, Pitch.E, 4))
        segment.add_note(3, RegNote(4, Pitch.F, 4))

        encoded_seg = encode_seg(segment)
        self.assertTrue(isinstance(encoded_seg, dict))
        assert_that(encoded_seg, has_entries(expected))

    def test_encode_score(self):
        expected = [{
            CLEF: "treble",
            NOTES: [
                {DURATION: "w",
                 KEYS: ["F"]}
            ]
        }]

        score = IRScore.default_construct()
        score.segments[0].append_note(RegNote(1, Pitch.F, 4))

        encoded = encode_score(score)
        self.assertTrue(isinstance(encoded, list))

        assert_that(len(encoded), len(expected),
                    "Difference in encoded list length")
        for i in range(len(expected)):
            with self.subTest(i=i):
                assert_that(encoded[i], has_entries(expected[i]))


if __name__ == '__main__':
    unittest.main()
