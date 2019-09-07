# u_V -> úV when accented, uV otherwise
# i_V -> íV when accented, iV otherwise
# e_V -> éV when accented, eV otherwise

-> start

start -> start   [X;V-i,u,e;Q]

## accented
start -> A      [í:i;ú:u;é:e]     # accent the i or u
A -> A_         [:_]          # delete the _
# unaccented vowel must follow; it's the last vowel
A_ -> A_V       [V0]
# ... followed by s, n, or nothing
A_V -> end      [s;n;:]

## unaccented
start -> iu     [i;u;e]       # don't accent the i, u or e
iu -> iu_       [:_]          # delete the _
# ' or accented vowel
iu_ -> start    [';V1]
# unaccented vowel, could be final
iu_ -> iu_V     [V0]

# accent final vowel following _ (probably only i, maybe e)
iu_ -> iu_acc   [í:i;é:e;á:a;ú:u]
# final consonant following accented vowel (reír)
iu_acc -> iu_accC [X]
# and one more vowel (creído)
iu_accC -> iu_accCV [V4]
# and possibly a final n or s (reúnen/s)
iu_accCV -> end   [n;s]

# another vowel could follow
iu_V -> start   [';V1]
iu_V -> iu_VC   [X]
iu_VC -> iu_VC  [X]
# some other vowel or '
iu_VC -> start  [V;']

# other occurrences of i and u
iu -> start     [X;V;Q-_]

start ->
end ->
iu ->
iu_V ->
iu_VC ->
iu_accC ->
iu_accCV ->