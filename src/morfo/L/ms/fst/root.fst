###
### A root consists of 1-3 syllables.
### Each syllable consists of
### (C)V(c), where
### c: {l, r, m, n, ng, p, t, k, s, h}

-> start

start -> c1.      [X0]
start -> cv1.     [V0]    # no syll1 onset
c1. -> cv1.       [V]
cv1. -> cvc1.     [x]

cv1. -> c2.       [X;:]   # no syll1 coda
cvc1. -> c2.      [X]
c2. -> cv2.       [V]
cv2. -> cvc2.     [x]

cv2. -> c3.       [X;:]   # no syll2 coda
cvc2. -> c3.      [X]
c3. -> cv3.       [V]
cv3. -> end       [x;:]

end ->
cv1. ->
cvc1. ->
cv2. ->
cvc2. ->
cv3. ->