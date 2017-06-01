# Does NOT support accidental for now
from intune.internalrep.ir import RegNote, RestNote
from intune.internalrep.irdefs import Pitch, Accidental

# Constants
DEF_PITCH = "b/4"
DEF_OCTAVE = 4
DEF_ACCIDENTAL = Accidental.NAT

# Keywords
DURATION = 'duration'
KEYS = 'keys'

# -- Encoder --- #
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


def encode_note(note):
    """
    Polymorphic encoding of a note
    :param note:
    :type note: Note
    :return:
    :rtype: dict
    """
    return note.accept_codec(__name__)


def encode_rest_note(note):
    """
    Translates a single REST note
    :param note:
    :type note: RestNote
    :return: encoded form of a rest note
    :rtype: dict
    """
    encoded = encode_duration(note.duration)
    return {DURATION: (encoded + "r"),
            KEYS: [DEF_PITCH]}


def encode_reg_note(note):
    """
    Translates a single REGULAR note
    :param note:
    :type note: RegNote
    :return: encoded form of a regular note
    :rtype: dict
    """
    return {DURATION: encode_duration(note.duration),
            KEYS: [encode_pitch(note.pitch)]}


def encode_duration(duration):
    """
    Encodes IR Duration format to VexFlow JSON format
    :param duration:
    :type duration: int
    :return:
    :rtype: str
    """
    return duration_encoding[duration]


def encode_pitch(pitch):
    """
    Encodes IR Pitch format to VexFlow JSON format
    :param pitch:
    :type pitch: Pitch
    :return:
    :rtype: str
    """
    return pitch_encoding[pitch]


# --- Decoder --- #
pitch_decoding = {
    "C": Pitch.C,
    "D": Pitch.D,
    "E": Pitch.E,
    "F": Pitch.F,
    "G": Pitch.G,
    "A": Pitch.A,
    "B": Pitch.B,
}

duration_decoding = {
    "w": 1,
    "wr": 1,
    "h": 2,
    "hr": 2,
    "hd": 3,
    "hdr": 3,
    "q": 4,
    "qr": 4,
    "1": 1,
    "2": 2,
    "4": 4,
    "8": 8,
    "16": 16
}


def decode_pitch(pitch):
    """
    :param pitch:
    :type pitch: str
    :return:
    :rtype: Pitch
    """
    return pitch_decoding[pitch]


def decode_duration(duration):
    """
    :param duration:
    :type duration: str
    :return:
    :rtype: int
    """
    return duration_decoding[duration]


def decode_reg_note(note):
    """
    :param note:
    :type note: dict
    :return:
    :rtype: RegNote
    """
    duration = decode_duration(note[DURATION])
    chord = note[KEYS]
    # Assume only single notes
    pitches = [decode_pitch(p) for p in chord]
    if len(pitches) > 0:
        pitch = pitches[0]
    else:
        # Default Pitch
        pitch = DEF_PITCH

    return RegNote(duration, pitch, DEF_OCTAVE)


def decode_rest_note(note):
    """
    :param note:
    :type note: dict
    :return:
    :rtype: RestNote
    """
    duration = decode_duration(note[DURATION])
    return RestNote(duration)


def decode_note(note):
    """
    :param note:
    :type note: dict
    :return:
    :rtype: Note
    """
    if 'r' in note[DURATION]:
        # Rest Note
        return decode_rest_note(note)
    else:
        return decode_reg_note(note)

