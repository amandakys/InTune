# Encoding segments from a score
# A score has additional attributes - title, composer, etc. -
# which are not part of the notation rendering
from intune.internalrep.jsoncodec.seg_codec import encode_seg, decode_seg


def encode_score_segs(score_segs):
    """
    :param score_segs:
    :type score_segs: IRScore
    :return:
    :rtype: list
    """
    segments = score_segs.segments
    encoded = [encode_seg(s) for s in segments]
    return encoded


def decode_score_segs(score_segs):
    """
    :param score_segs:
    :type score_segs: list
    :return: List of Segments
    :rtype: list
    """
    return [decode_seg(s) for s in score_segs]
