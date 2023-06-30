# realization of vowel before -taj(ik) following VTR: ^
# assume vowel is previous vowel, though this will not always be true

-> start

start -> start [C;V;P;S-^; ]

start -> C     [C-',n]
C -> start     [v:^]

start -> n     [';n]
n -> n^        [:^]
n^ -> start    [C]

start ->
