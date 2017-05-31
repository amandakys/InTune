import unittest

from hamcrest import *

from intune.internalrep.ir import RegNote, RestNote
from intune.internalrep.irdefs import Pitch
from intune.internalrep.translate import IREncoder


class IRTranslateTestCase(unittest.TestCase):

    def test_encode_pitch(self):
        pitch = Pitch.C
        expected = "C"
        encoded_pitch = IREncoder.encode_pitch(pitch)
        self.assertEqual(encoded_pitch, expected)

    def test_encode_duration(self):
        duration = 4
        expected = "q"
        encoded_duration = IREncoder.encode_duration(duration)
        self.assertEqual(encoded_duration, expected)

    def test_encode_reg_note(self):
        note = RegNote.default_construct()
        encoded_note = IREncoder.encode_reg_note(note)
        expected = {IREncoder.DURATION: 1,
                    IREncoder.KEYS: ["C"]}
        self.assertTrue(isinstance(encoded_note, dict))
        assert_that(encoded_note, has_entries(expected))

    def test_encode_rest_note(self):
        note = RestNote(4)
        encoded_note = IREncoder.encode_rest_note(note)
        expected = {IREncoder.DURATION: "qr",
                    IREncoder.KEYS: [IREncoder.DEF_REST_POS]}
        self.assertTrue(isinstance(encoded_note, dict))
        assert_that(encoded_note, has_entries(expected))


if __name__ == '__main__':
    unittest.main()
