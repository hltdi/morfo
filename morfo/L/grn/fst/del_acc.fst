## Before *, deaccent accented characters and delete !.
##  Make this optional in analysis. Generation: G%
## After *, keep ! and accented characters
## Delete all *s in the process.

-> start

## Delete * if there's nothing to deaccent
# A%
# start -> start   [.-*]
# G%
start -> start   [.-!,*,@V]
# Delete *
start -> start      [:*]

## what to with accented characters and !

# deaccent and delete ! if a * appears later
start -> deacc   [a:á;e:é;i:í;o:ó;u:ú;y:ý;:!]
deacc -> deacc   [a:á;e:é;i:í;o:ó;u:ú;y:ý;:!]
deacc -> deacc   [.-@V,!,*]
# Must be followed by *, which is deleted
# (What if it's not final?)
deacc -> end     [:*]
end -> end       [.]
## Following only true if suf.lex file is used
## ~ may be followed by * at the end of a word; both are deleted
#deacc -> deacc1  [:~]
#deacc1 -> end    [:*]

## Keep ! and accented characters (only when no * follows in gen)
#G%
start -> nodeacc   [á;é;í;ó;ú;ý;!]
#G%
# ... if no * appears later
nodeacc -> nodeacc  [.-*]

start ->
#G%
nodeacc ->
end ->

