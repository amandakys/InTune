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

    def test_encode_reg_note(self):
        note = RegNote.default_construct()
        encoded_note = IREncoder.encode_reg_note(note)
        expected = {IREncoder.DURATION: 1,
                    IREncoder.KEYS: ["C"]}
        self.assertTrue(isinstance(encoded_note, dict))
        assert_that(encoded_note, has_entries(expected))

    def test_encode_rest_note(self):
        note = RestNote(1)
        encoded_note = IREncoder.encode_rest_note(note)
        self.assertTrue(isinstance(encoded_note, dict))
        self.assertEqual(encoded_note[IREncoder.DURATION], 1)
        self.assertEqual(encoded_note[IREncoder.KEYS], [])

if __name__ == '__main__':
    unittest.main()
