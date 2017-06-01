from intune.internalrep.ir import IRScore, RegNote
from intune.internalrep.irdefs import Pitch
from intune.internalrep.translate import \
    SegEncoder, NoteEncoder

# simple_ir
simple_ir = IRScore.default_construct()
simple_ir.segments[0].append_note(RegNote.default_construct())

simple_encoded = [
    {SegEncoder.CLEF: "treble",
     SegEncoder.NOTES: [
         {NoteEncoder.DURATION: "w", NoteEncoder.KEYS: ["C"]}
     ]}
]

# sample_ir1
sample_ir1 = IRScore.default_construct()
sample_segments = simple_ir.segments[0]
sample_segments.append_note(RegNote(4, Pitch.C, 4))
