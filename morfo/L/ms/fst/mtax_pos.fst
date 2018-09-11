###
### Malay nouns, verbs, adjectives
###

### morpheme and morphophonemic characters
# R
# N

-> start

# Nouns

## peN- and pe(R)-
start -> agtpat0    [:]       [pos=n, suf=0];[pos=n, suf=an]
# Relax this constraint
agtpat0 -> agtpat1  [:]       #   [rcat=v];[rcat=a]
agtpat1 -> root     <peN:>    [pre=peN]
agtpat1 -> pe0      <pe:>     [pre=pe]
# per- and pe- are variants of the same prefix
pe0 -> root        [R:;:]        
## juru-
start -> root   <juru:>       [pos=n, pre=juru,suf=0,rcat=n]

# Verbs and adjectives

## ber-
# with or without -an / -kan; any limitation on roots?
start -> ber1   [:]        [suf=an];[suf=kan];[suf=0]
# ber0 -> ber1    [:]        [rcat=v];[rcat=n];[rcat=p]
ber1 -> root   <beR:>      [pos=v, pre=ber]
## keber-
# this is really ke- + ber-, so does it obey the constraits for ber- or ke-?
start -> keber <kebeR:>    [pos=v, pre=keber]

## meN-
# with or without -i / -kan
start -> root   <meN:>     [pos=v, pre=meN,suf=0];[pos=v, pre=meN,suf=i];[pos=v, pre=meN,suf=kan]
# with or without -i / -kan; without suffix must have verb root?
## mempeR
# this is really meN- + per-
# with or without -i / -kan
start -> root <mempeR:>    [pos=v, pre=memper,suf=0];[pos=v, pre=memper,suf=i];[pos=v, pre=memper,suf=kan]
## menge
# this is really meN- + ke-
# with or without -i / -kan
start -> root <menge:>    [pos=v, pre=menge,suf=0];[pos=v, pre=menge,suf=i];[pos=v, pre=menge,suf=kan]

## di-
# shouldn't di- -0 only work with verb roots?
start -> root   <di:>      [pos=v, pre=di,suf=0];[pos=v, pre=di,suf=i];[pos=v, pre=di,suf=kan]
## dike-
# this is really di- + ke-
start -> root   <dike:>    [pos=v, pre=dike,suf=0];[pos=v, pre=dike,suf=i];[pos=v, pre=dike,suf=kan]
## dipeR-
# this is really di- + peR-
# -i / -kan / -0
start -> root  <dipeR:>    [pos=v, pre=diper,suf=0];[pos=v, pre=diper,suf=kan];[pos=v, pre=diper,suf=i]

## teR-
# no suffix possible; root can be verb, adj, or adv; POS can be verb or adj
start -> ter0   [:]        [pre=ter,suf=0,rcat=v];[pre=ter,suf=0,rcat=a];[pre=ter,suf=0,rcat=adv]
ter0 -> root   <teR:>      [pos=v];[pos=a]

# Various POS

## ke-
start -> ke0    [:]         [pre=ke]
# Not so clear what the constraints are for ke-; POS can be n,v,a; suffix can be -0,-an,-kan; root can be anything?
ke -> root      <ke:>       [suf=an];[suf=kan];[suf=0]
## must have -an for verbs and adjectives? root constraints not clear
## start -> root   <ke:>         [pos=v, pre=ke,suf=an];[pos=a, pre=ke,suf=an,rcat=n]; [pos=n, pre=ke,suf=an,rcat=n]
## uncommon but nouns can have ke- and no suffix
## start -> root   <ke:>         [pos=n, pre=ke,suf=0,rcat=v]
## se-
# not clear what the restrictions are on POS for se- or what root categories are
start -> root   <se:>         [pre=se,suf=0]

# irregular <ajar>

start -> suffix <belajar+:ajar>       [pos=v, pre=ber,suf=0,rcat=v,+free];[pos=v, pre=ber,suf=an,rcat=v,+free];[pos=v, pre=ber,suf=kan,rcat=v,+free]
start -> suffix <mempelajar+:ajar>    [pos=v, pre=memper,suf=0,rcat=v,+free];[pos=v, pre=memper,suf=i,rcat=v,+free];[pos=v, pre=memper,suf=kan,rcat=v,+free]
start -> suffix <dipelajar+:ajar>     [pos=v, pre=diper,suf=0,rcat=v,+free];[pos=v, pre=diper,suf=kan,rcat=v,+free];[pos=v, pre=diper,suf=i,rcat=v,+free]
start -> suffix <pelajar+:ajar>       [pos=n, pre=pe,suf=an,rcat=v,+free];[pos=n, pre=pe,suf=0,rcat=v,+free]

## No prefix

start -> no_pre_v  [:]                [pos=v, pre=0]
# verb root is whole verb (+free root), or suffix is -kan or -i
no_pre_v -> root   [:]                [pos=v, rcat=v,suf=0,+free];[pos=v, rcat=v,suf=kan];[pos=v, rcat=v,suf=i]
# no prefix with noun or adj root: must have suffix (i or kan)
no_pre_v -> root   [:]                [pos=v, rcat=n,suf=kan];[pos=v, rcat=n,suf=i];[pos=v, rcat=a,suf=kan];[pos=v, rcat=a,suf=i]
start -> root      [:]                [pos=n, pre=0,suf=0,rcat=n,+free];[pos=n, pre=0,suf=an];[pos=a, pre=0,rcat=a,suf=0,+free]

### root

root -> root0  +siv_root_free+       [rcat=a,+free]
root -> root0  +siv_root_bound+      [rcat=a,-free]
root -> root0  +n_root_free+         [rcat=n,+free]
root -> root0  +n_root_bound+        [rcat=n,-free]
root -> root0  +tv_root_free+        [rcat=v,rtrans=t,+free]
root -> root0  +tv_root_bound+       [rcat=v,rtrans=t,-free]
root -> root0  +iv_root_bound+       [rcat=v,rtrans=i,-free]
root -> root0  +iv_dyn_root_bound+   [rcat=v,rtrans=id,-free]
root -> root0  +iv_dyn_root_free+    [rcat=v,rtrans=id,+free]
root -> root0  +prep+                [rcat=p,+free]
# This list needs to be extended
root -> root0  +adv+                 [rcat=adv,+free]
root0 -> suffix  [+:]

### suffixes

## -i
# -i always seems to produce a verb but appears on different root cats; occurs with meN-, memper-, di- and 0-
suffix -> end    [i:]               [pos=v, suf=i]
## -an
# -an and -kan seem to occur with almost all prefixes and no prefix
suffix -> end   <an:>               [suf=an]
## -kan
suffix -> end  <kan:>               [suf=kan]

# no suffix
suffix -> end    [:]                [suf=0]

end ->
