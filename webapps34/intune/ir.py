from intune.irdefs import Accidental


class Note:
    # TODO: Refactor to ABC class

    def __init__(self, duration):
        self.duration = duration

    def modulate(self, semitones, keysig):
        pass


class RestNote(Note):

    def __init__(self, duration):
        Note.__init__(self, duration)


class RegNote(Note):

    def __init__(self, duration, pitch, octave):
        Note.__init__(self, duration)
        self.pitch = pitch
        self.octave = octave
        self.accidental = Accidental.NONE

    def modulate(self, semitones, keysig):
        """
        Changes the note by the number of semitones given
        :param keysig: key signature used by this note
        :param semitones: int (+/-) number of semitones to change
        :return: self
        """

        # TODO: Do actual modulation
        return self


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
        self.notes.remove(index)
        # Rest placeholder
        self.notes.insert(index, RestNote())
        return self

