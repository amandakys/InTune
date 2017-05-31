# Translates IR into Python Dictionary in VewFlow JSON Format
from intune.internalrep.ir import RegNote
from intune.internalrep.irdefs import Pitch

# Pitch Encoding Dictionary
# Does NOT support accidental for now
pitch_encoding = {
    Pitch.C: "C",
    Pitch.D: "D",
    Pitch.E: "E",
    Pitch.F: "F",
    Pitch.G: "G",
    Pitch.A: "A",
    Pitch.B: "B",
}


class IREncoder:
    # Keywords
    DURATION = 'duration'
    KEYS = 'keys'

    @staticmethod
    def encode_pitch(pitch):
        """
        Encodes IR Pitch format to VexFlow JSON format
        :param pitch:
        :type pitch: Pitch
        :return:
        :rtype: Pitch
        """
        return pitch_encoding[pitch]

    @staticmethod
    def encode_reg_note(note):
        """
        Translates a single REGULAR note
        :param note:
        :type note: RegNote
        :return: encoded form of a regular note
        :rtype: dict
        """
        return {IREncoder.DURATION: note.duration,
                IREncoder.KEYS: [IREncoder.encode_pitch(note.pitch)]}

    @staticmethod
    def encode_rest_note(note):
        """
        Translates a single REST note
        :param note:
        :type note: RestNote
        :return: encoded form of a rest note
        :rtype: dict
        """
        return {IREncoder.DURATION: note.duration,
                IREncoder.KEYS: []}

    @staticmethod
    def encode_segment(segment):
        """
        Translates a single segment
        :param segment:
        :type segment: Segment
        :return:
        :rtype:
        """
        pass
