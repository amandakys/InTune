# Abstract Class
class Note:
    # TODO: Abstract class / Interface
    pass


class RestNote:
    # TODO: Implements Note
    pass


class RegNote:
    # TODO: Implements Note
    pass


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

    def changetimesig(self, newtimesig):
        self.timeSig = newtimesig

    def addnote(self, index, note):
        self.notes.insert(index, note)

    def delnote(self, index):
        self.notes.remove(index)
        # Rest placeholder
        self.notes.insert(index, RestNote())

