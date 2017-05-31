from enum import IntEnum, Enum


class Pitch(IntEnum):
    # Overview:
    # 1. 12 semitones exists in an octave
    # 2. Start at C
    # More details:
    # Refer to https://en.wikipedia.org/wiki/Piano_key_frequencies

    C = 0
    D_FLAT = 1
    C_SHARP = 1
    D = 2
    E_FLAT = 3
    D_SHARP = 3
    E = 4
    F_FLAT = 4
    F = 5
    E_SHARP = 5
    G_FLAT = 6
    F_SHARP = 6
    G = 7
    A_FLAT = 8
    G_SHARP = 8
    A = 9
    B_FLAT = 10
    A_SHARP = 10
    B = 11
    B_SHARP = 0


class Accidental(Enum):
    # Overview:
    # Accidentals are referenced only during rendering, pitch should reflect
    # the true tone of that note
    NAT = "n"
    SHARP = "#"
    DB_SHARP = "##"
    FLAT = "b"
    DB_FLAT = "bb"

