## Delete ! before or after accented vowels and right after a nasal vowel.

-> start

start -> start    [.-@V,@Z,!]

# acc: at least one accented vowel
start -> acc      [@V]

# del: at least one ! has been deleted
# there must be an accented vowel: @V
start -> del      [:!]
# following deleted !,
# there must be at least one more segment, not accented, but possibly nasal
del -> delX       [.-@V]
delX -> del       [:!]
delX -> delX      [.-@V,!]
delX -> acc       [@V]
del -> acc        [@V]
# further ! must be deleted
acc -> accdel     [:!]
# must be at least one more segment after deleted !
accdel -> acc     [.-!]
acc -> acc        [.-!]

# ret: at least one ! has been retained
# there can be no accented vowel: @V
start -> ret      [!]
ret -> ret        [.-@V]

start -> nas      [@Z]
# Delete ! if it comes right after a nasal vowel
nas -> accdel     [:!]
# otherwise go back to start
nas -> start      [.-!]

start ->
acc ->
ret ->
nas ->