# realization of 1s erg: nu, w, in, inw

-> start

start -> mid   [C;V;M;A;E]

mid -> mid     [C;V;A;E; ]

# before consonant
.C -> mid      [C]
# before vowel
.V -> mid      [V]

# only nuC at beginning of word
start -> n.u1  [n:N]
n.u1 -> .C     [u:]
.C -> mid      [C]
# only wV at beginning of word
start -> .V    [w:N]

# wV or inwV in mid-word
mid -> .V      [w:N]
mid -> i.n     [i:N]
i.n -> in      [n:]
in -> .V       [w:]

# inC in mid-word, unless it follows l, in which case nu is also possible
i.n -> .C      [n:]
mid -> l       [l]
l -> ln        [n:N]
ln -> .C       [u:]

mid ->

