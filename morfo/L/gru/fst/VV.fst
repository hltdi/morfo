# eu -> o
# Eu -> Ew
# iu -> iw

-> start

start -> start [X;=;_;/;V-e,E,i,a]

start ->  e.u  [o:e]
e.u -> start   [:u]
start -> e     [e]
e -> start     [X;_;/;V-u]
e -> e=.C      [=]
e=.C -> start  [X;/]
# delete e before vowels on other side of boundary
start -> e.=V  [:e]
e.=V -> e=.V   [=]
# e=e, e=a, e=i, e=I, e=o
e=.V -> start  [e;a;i;I;o]

start -> E     [E]
E -> start     [w:u;X;=;_;/;V-u]

start -> i     [i]
i -> start     [w:u;X;=;_;/;V-u]

start -> a     [a]
a -> start     [X;_;/;V-i;=]
a -> a.i       [y:]
a.i -> start   [i]

start ->
i ->
e ->
E ->
a ->