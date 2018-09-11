# realization of imperative and movement suffixes for VTR

-> start

start -> start [C;V;P;*; ]

start -> u     [u]
u -> uC        [C]
uC -> VCV      [u:@]
VCV -> start   [':]

start -> o     [o]
o -> oC        [C]
oC -> VCV      [o:@]
VCV -> start   [':]

start -> a     [a;e;i]
a -> aC        [C]
aC -> VCV      [a:@]
VCV -> start   [':]

start ->
