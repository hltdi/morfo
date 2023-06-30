# M -> m, X -> ng (inmediatamente) después de nasal "real"
# P -> mb después de cualquier nasal

-> start

start -> start  [.-@M]

start -> M      [@M]
M -> M          [@M;@v;!;%;*]
M -> start      [m:M;ng:X;.-@v,@M,M,X,!,%]
# optionally one non-nasal syllable can intervene
M -> M1         [@x;@G]
M1 -> M2        [@x;@G;!;%;*]
M2 -> M3        [!;%;*]
M2 -> start     [m:M;ng:X]
M3 -> start     [m:M;ng:X]

# P can only happen once and always before M and X?
#start -> G      [@G]
#G -> G          [.-P,@M]
#G -> M          [@M]
#G -> start      [mb:P]

start ->
M ->
#G ->

