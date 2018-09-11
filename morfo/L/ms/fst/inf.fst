-> start

start -> start  [X;V;R;N;+]

start -> L      [:L]
start -> M      [:M]
start -> R      [:$]

L -> LC         [X]
M -> MC         [X]
R -> RC         [X]

LC -> start     <el:>
MC -> start     <em:>
RC -> start     <er:>

start ->
