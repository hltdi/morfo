# A syllable can consist of an onset consonant (or nothing), a vowel, and a
# coda consonant (or nothing)
#
# Ignore capital letters

-> start

start -> c.   [X;:]
c. -> cv.     [V]
cv. -> end    [x;:]

end ->