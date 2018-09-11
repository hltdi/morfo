# M -> m, X -> ng (inmediatamente) después de nasal "real"
# P -> mb después de cualquier nasal

-> start

start -> start  [.-@M]

start -> M      [@M]
M -> M          [@M;@v;!;%;*]
M -> start      [m:M;ng:X;.-@v,@M,M,X,!,%]

# P can only happen once and always before M and X?
#start -> G      [@G]
#G -> G          [.-P,@M]
#G -> M          [@M]
#G -> start      [mb:P]

start ->
M ->
#G ->

