from intune.internalrep.irdefs import Accidental, Pitch


class Note:
    # TODO: Refactor to ABC class

    def __init__(self, duration):
        """
        Standard constructor for all notes
        :param duration: Length of note to be played
        :type duration: int
        """
        self.duration = duration

    def modulate(self, semitones, keysig):
        pass

    def del_note(self):
        pass

    def accept_encoder(self, encoder):
        pass


class RestNote(Note):

    def __init__(self, duration):
        Note.__init__(self, duration)

    def accept_encoder(self, encoder):
        """
        :param encoder:
        :type encoder: NoteEncoder
        :return:
        :rtype: dict
        """
        return encoder.encode_rest_note(self)


class RegNote(Note):
    SEMITONES = 12
    MIN_PITCH = 0
    MAX_PITCH = 11
    MIN_OCTAVE = 0
    MAX_OCTAVE = 8
    DEFAULT_DURATION = 1
    DEFAULT_PITCH = Pitch.C
    DEFAULT_OCTAVE = 4

    def __init__(self, duration, pitch, octave):
        """
        Constructor
        :param duration: Length of note
        :type duration: int
        :param pitch: Semitone starting at C
        :type pitch: Pitch
        :param octave: Value of octave (0 to 8 incl)
        :type octave: int
        """
        Note.__init__(self, duration)
        self.pitch = pitch
        self.octave = RegNote.__bound_octave(octave)
        self.accidental = Accidental.NAT

    @classmethod
    def default_construct(cls):
        return cls(RegNote.DEFAULT_DURATION,
                   RegNote.DEFAULT_PITCH,
                   RegNote.DEFAULT_OCTAVE)

    @staticmethod
    def __bound_octave(octave):
        """

        :param octave:
        :type octave: int
        :return:
        :rtype: int
        """
        if octave < RegNote.MIN_OCTAVE:
            octave = RegNote.MIN_OCTAVE
        elif octave > RegNote.MAX_OCTAVE:
            octave = RegNote.MAX_OCTAVE

        return octave

    def mod_octave(self, diff):
        """

        :param diff:
        :type diff: int
        """
        octave = self.octave + diff
        self.octave = RegNote.__bound_octave(octave)

    def set_pitch(self, pitch):
        """
        Sets the new pitch explicitly
        :param pitch: New pitch
        :type pitch: Pitch
        """
        self.pitch = pitch

    def set_octave(self, octave):
        """
        Sets the new octave explicitly
        :param octave: New octave
        :type octave: int
        """
        self.octave = RegNote.__bound_octave(octave)

    def set_accidental(self, accidental):
        """
        Sets accidental explicitly
        :param accidental: New accidental
        :type accidental: Accidental
        """
        self.accidental = accidental

    def modulate(self, semitones, keysig):
        """
        Changes the note by the number of semitones given
        :param keysig: key signature used by this note
        :param semitones: int (+/-) number of semitones to change
        :return: self
        """

        # pitch = self.pitch
        # cand = pitch.value + semitones
        # # Max pitch reached
        # if cand > RegNote.MAX_PITCH:
        #     if self.octave.value >= Octave.MAX:
        #         self.pitch = Pitch.B
        #     else:
        #         octavechange = int(semitones / RegNote.SEMITONES)
        #         self.octave.mod(octavechange)
        #
        #     pitchchange = semitones % RegNote.SEMITONES
        #
        # else:
        #     self.pitch = Pitch(cand)

        # TODO: Do actual modulation
        return self

    def del_note(self):
        return RestNote(self.duration)

    def accept_encoder(self, encoder):
        """
        :param encoder:
        :type encoder: NoteEncoder
        :return:
        :rtype: dict
        """
        return encoder.encode_reg_note(self)


# || Segment Class Overview ||
# Class Attribute:
# 1. segCount (number of segments)
# Instance Attributes:
# 1. keySig (key signature)
# 2. timeSig (time signature)
# 3. notes (list of notes)
class Segment:
    # Constants
    DEF_CLEF = "treble"
    DEF_KEYSIG = "C"
    DEF_TIMESIG = (4, 4)

    # Internal counter
    segCount = 0

    def __init__(self, clef, key_sig, time_sig):
        self.clef = clef
        self.keySig = key_sig
        self.timeSig = time_sig
        self.notes = []
        Segment.segCount += 1

    @classmethod
    def default_construct(cls):
        return cls(Segment.DEF_CLEF,
                   Segment.DEF_KEYSIG,
                   Segment.DEF_TIMESIG)

    # Segment functions #

    def change_key(self, newkey):
        self.keySig = newkey
        # TODO: modulate all notes wrt new key
        return self

    def change_timesig(self, new_timesig):
        self.timeSig = new_timesig
        return self

    def append_note(self, note):
        self.notes.append(note)
        return self

    def add_note(self, index, note):
        self.notes.insert(index, note)
        return self

    def de_note(self, index):
        """
        Replaces note to be deleted at index with a rest of the same duration
        :param index: Note index to be deleted
        :type index: int
        :return: self with placeholder inserted
        :rtype: Segment
        """
        note = self.notes[index]
        placeholder = note.del_note()
        self.notes.remove(index)
        # Rest placeholder
        self.notes.insert(index, placeholder)
        return self


class IRScore:
    DEFAULT_TILE = "Untitled"
    DEFAULT_COMPOSER = "Unknown"
    DEFAULT_ARRANGER = "Unknown"

    def __init__(self, title, composer, arranger):
        self.segments = [Segment.default_construct()]

    @classmethod
    def default_construct(cls):
        """
        Default Constructor
        :return: Composition object with default values
        :rtype: IRScore
        """
        return cls(IRScore.DEFAULT_TILE,
                   IRScore.DEFAULT_COMPOSER,
                   IRScore.DEFAULT_ARRANGER)

    def add_seg(self, segment):
        self.segments.append(segment)

    def del_seg(self, index):
        del self.segments[index]

