from enum import IntEnum, Enum


class Pitch(IntEnum):
    # Overview:
    # 1. 12 semitones exists in an octave
    # 2. Start at C
    # More details:
    # Refer to https://en.wikipedia.org/wiki/Piano_key_frequencies

    C = 0
    DFLAT = 1
    CSHARP = 1
    D = 2
    EFLAT = 3
    DSHARP = 3
    E = 4
    FFLAT = 4
    F = 5
    ESHARP = 5
    GFLAT = 6
    FSHARP = 6
    G = 7
    AFLAT = 8
    GSHARP = 8
    A = 9
    BFLAT = 10
    ASHARP = 10
    B = 11
    BSHARP = 0


class Accidental(Enum):
    # Overview:
    # Accidentals are referenced only during rendering, pitch should reflect
    # the true tone of that note
    NAT = "n"
    SHARP = "#"
    DSHARP = "##"
    FLAT = "b"
    DFLAT = "bb"

