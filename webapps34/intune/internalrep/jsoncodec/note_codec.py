# Pitch Encoding Dictionary
# Does NOT support accidental for now
from intune.internalrep.irdefs import Pitch

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

# Keywords
DURATION = 'duration'
KEYS = 'keys'

# Constants
DEF_REST_POS = "b/4"


def encode_note(note):
    """
    Polymorphic encoding of a note
    :param note:
    :type note: Note
    :return:
    :rtype: dict
    """
    return note.accept_encoder(__name__)


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
            KEYS: [DEF_REST_POS]}


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
def decode_pitch(pitch_json):
    pass


def decode_duration(duration_json):
    pass


def decode_note(note_json):
    pass
