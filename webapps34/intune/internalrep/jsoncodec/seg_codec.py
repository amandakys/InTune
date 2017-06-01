# Keywords
from intune.internalrep.jsoncodec.note_codec import encode_note

CLEF = 'clef'
NOTES = 'notes'


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
