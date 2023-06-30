# realization of vowel before -n(ik) following VTR: $
# below ba.fst and Vtaj

-> start

start -> start [C;V;P;L;O;@;*; ]

start -> u     [u]
u -> uC        [C]
uC -> start    [u:$]

start -> a     [a]
a -> aC        [C]
aC -> start    [a:$]

start -> o     [i;e;o]
o -> oC        [C]
oC -> start    [o:$]

start ->

