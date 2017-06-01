from intune.internalrep.jsoncodec.seg_codec import encode_seg, decode_seg


def encode_score(score):
    """
    :param score:
    :type score: IRScore
    :return:
    :rtype: list
    """
    segments = score.segments
    encoded = [encode_seg(s) for s in segments]
    return encoded


def decode_score_segs(score):
    """
    :param score:
    :type score: list
    :return: List of Segments
    :rtype: list
    """
    return [decode_seg(s) for s in score]
