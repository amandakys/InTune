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

duration_encoding = {
    1: "w",
    2: "h",
    3: "hd",
    4: "q",
    8: "8",
    16: "16"
}


class NoteEncoder:
    # Keywords
    DURATION = 'duration'
    KEYS = 'keys'

    # Constants
    DEF_REST_POS = "b/4"

    @staticmethod
    def encode_pitch(pitch):
        """
        Encodes IR Pitch format to VexFlow JSON format
        :param pitch:
        :type pitch: Pitch
        :return:
        :rtype: str
        """
        return pitch_encoding[pitch]

    @staticmethod
    def encode_duration(duration):
        """
        Encodes IR Duration format to VexFlow JSON format
        :param duration:
        :type duration: int
        :return:
        :rtype: str
        """
        return duration_encoding[duration]

    @staticmethod
    def encode_reg_note(note):
        """
        Translates a single REGULAR note
        :param note:
        :type note: RegNote
        :return: encoded form of a regular note
        :rtype: dict
        """
        return {NoteEncoder.DURATION: NoteEncoder.encode_duration(note.duration),
                NoteEncoder.KEYS: [NoteEncoder.encode_pitch(note.pitch)]}

    @staticmethod
    def encode_rest_note(note):
        """
        Translates a single REST note
        :param note:
        :type note: RestNote
        :return: encoded form of a rest note
        :rtype: dict
        """
        encoded = NoteEncoder.encode_duration(note.duration)
        return {NoteEncoder.DURATION: (encoded + "r"),
                NoteEncoder.KEYS: [NoteEncoder.DEF_REST_POS]}

    @staticmethod
    def encode_note(note):
        """
        Polymorphic encoding of a note
        :param n:
        :type n: Note
        :return:
        :rtype: dict
        """
        return note.accept_encoder(NoteEncoder)


class SegEncoder:
    # Keywords
    CLEF = 'clef'
    NOTES = 'notes'

    @staticmethod
    def encode_seg(segment):
        """
        Translates a single segment
        :param segment:
        :type segment: Segment
        :return: encoded form of a segment
        :rtype: dict
        """
        encoded_notes = []
        for n in segment.notes:
            enc_note = NoteEncoder.encode_note(n)
            encoded_notes.append(enc_note)

        return {SegEncoder.CLEF: segment.clef,
                SegEncoder.NOTES: encoded_notes}

