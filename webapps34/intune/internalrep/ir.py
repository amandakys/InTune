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

    def delnote(self):
        pass


class RestNote(Note):

    def __init__(self, duration):
        Note.__init__(self, duration)


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
        self.octave = RegNote.__boundoctave(octave)
        self.accidental = Accidental.NAT

    @classmethod
    def defaultconstruct(cls):
        return cls(RegNote.DEFAULT_DURATION,
                   RegNote.DEFAULT_PITCH,
                   RegNote.DEFAULT_OCTAVE)

    @staticmethod
    def __boundoctave(octave):
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

    def modoctave(self, diff):
        """

        :param diff:
        :type diff: int
        """
        octave = self.octave + diff
        self.octave = RegNote.__boundoctave(octave)

    def setpitch(self, pitch):
        """
        Sets the new pitch explicitly
        :param pitch: New pitch
        :type pitch: Pitch
        """
        self.pitch = pitch

    def setoctave(self, octave):
        """
        Sets the new octave explicitly
        :param octave: New octave
        :type octave: int
        """
        self.octave = RegNote.__boundoctave(octave)

    def setaccidental(self, accidental):
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

    def delnote(self):
        return RestNote(self.duration)


# || Segment Class Overview ||
# Class Attribute:
# 1. segCount (number of segments)
# Instance Attributes:
# 1. keySig (key signature)
# 2. timeSig (time signature)
# 3. notes (list of notes)
class Segment:
    segCount = 0

    def __init__(self):
        self.keySig = "C"
        self.timeSig = (4, 4)
        self.notes = []

        Segment.segCount += 1

    @classmethod
    def defaultconstruct(cls):
        return cls()

    # Segment functions #

    def changekey(self, newkey):
        self.keySig = newkey
        # TODO: modulate all notes wrt new key
        return self

    def changetimesig(self, newtimesig):
        self.timeSig = newtimesig
        return self

    def addnote(self, index, note):
        self.notes.insert(index, note)
        return self

    def delnote(self, index):
        """
        Replaces note to be deleted at index with a rest of the same duration
        :param index: Note index to be deleted
        :type index: int
        :return: self with placeholder inserted
        :rtype: Segment
        """
        note = self.notes[index]
        placeholder = note.delnote()
        self.notes.remove(index)
        # Rest placeholder
        self.notes.insert(index, placeholder)
        return self


class Composition:
    DEFAULT_TILE = "Untitled"
    DEFAULT_COMPOSER = "Unknown"
    DEFAULT_ARRANGER = "Unknown"

    def __init__(self, title, composer, arranger):
        self.segments = [Segment()]

    @classmethod
    def defaultconstruct(cls):
        """
        Default Constructor
        :return: Composition object with default values
        :rtype: Composition
        """
        return cls(Composition.DEFAULT_TILE,
                   Composition.DEFAULT_COMPOSER,
                   Composition.DEFAULT_ARRANGER)

    def addsegment(self, segment):
        self.segments.append(segment)

    def delsegment(self, index):
        del self.segments[index]

