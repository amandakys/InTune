from enum import IntEnum, Enum, auto


class Pitch(IntEnum):
    # Overview:
    # 1. 12 semitones exists in an octave
    # 2. Start at C
    # More details:
    # Refer to https://en.wikipedia.org/wiki/Piano_key_frequencies
    C = 1
    CSHARP = 2
    DFLAT = 2
    D = 3
    DSHARP = 4
    EFLAT = 4
    E = 5
    FFLAT = 5
    ESHARP = 6
    F = 6
    FSHARP = 7
    GFLAT = 7
    G = 8
    GSHARP = 9
    AFLAT = 9
    A = 10
    ASHARP = 11
    BFLAT = 11
    B = 12
    BSHARP = 1


class Octave:
    MIN_VALUE = 0
    MAX_VALUE = 8

    def __init__(self, value):
        """
        Bounds octave to MIN_VALUE and MAX_VALUE
        :param value: Octave value (0 to 8 incl)
        :type value: int
        """
        if value < Octave.MIN_VALUE:
            self.value = Octave.MIN_VALUE
        elif value > Octave.MAX_VALUE:
            self.value = Octave.MAX_VALUE
        else:
            self.value = value

    def inc(self):
        if self.value < Octave.MAX_VALUE:
            self.value += 1

    def dec(self):
        if self.value > Octave.MIN_VALUE:
            self.value -= 1


class Accidental(Enum):
    # Overview:
    # Accidentals are referenced only during rendering, pitch should reflect
    # the true tone of that note
    NONE = auto()
    SHARP = auto()
    DSHARP = auto()
    FLAT = auto()
    DFLAT = auto()