# Keywords
from intune.internalrep.ir import Segment
from intune.internalrep.jsoncodec.note_codec import encode_note, decode_note

# Keywords
CLEF = 'clef'
NOTES = 'notes'

# Defaults
DEF_KEYSIG = "C"
DEF_TIMESIG = (4, 4)


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
        enc_note = encode_note(n)
        encoded_notes.append(enc_note)

    return {CLEF: segment.clef,
            NOTES: encoded_notes}


def decode_seg(segment):
    clef = segment[CLEF]
    notes = segment[NOTES]
    dec_notes = [decode_note(n) for n in notes]

    decoded = Segment(clef, DEF_KEYSIG, DEF_TIMESIG)
    decoded.notes = dec_notes

    return decoded

