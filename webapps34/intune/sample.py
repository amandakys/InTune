from intune.internalrep.ir import IRScore, RegNote
from intune.internalrep.irdefs import Pitch
from intune.internalrep.jsoncodec.note_codec import DURATION, KEYS
from intune.internalrep.jsoncodec.seg_codec import CLEF, NOTES

# simple_ir
# | C--- |
simple_ir = IRScore.default_construct()
simple_ir.segments[0].append_note(RegNote.default_construct())

simple_encoded = [
    {CLEF: "treble",
     NOTES: [
         {DURATION: "w", KEYS: ["C"]}
     ]}
]

# sample_ir1
# | C D F E |
sample_ir1 = IRScore.default_construct()
sample_segments = simple_ir.segments[0]
sample_segments \
    .append_note(RegNote(4, Pitch.C, 4)) \
    .append_note(RegNote(4, Pitch.D, 4)) \
    .append_note(RegNote(4, Pitch.F, 4)) \
    .append_note(RegNote(4, Pitch.E, 4))

sample_encoded = [
    {CLEF: "treble",
     NOTES: [
         {DURATION: "q", KEYS: ["C"]},
         {DURATION: "q", KEYS: ["D"]},
         {DURATION: "q", KEYS: ["F"]},
         {DURATION: "q", KEYS: ["E"]},
     ]}
]
