###
### K'iche' verbs
###

### morpheme and morphophonemic characters
# M: negative imperative prefix
# A: epenthetic a after k-
## ERG
# N: 1 s erg
# W: cons before vowel in 2 erg
# R: 3 s erg
# Q: 1 p erg
# K: 3 p erg
## MOV
# E: e', b'e': movement GO
## POST-ROOT/STEM
# v: reduplicated vowel
# T: reduplicated consonant
# L: active->stative positional
# ^, $ vowels before -taq and -n
## CATEGORIZERS
# O: categorizer for vtr, cmp, incmp
# @: categorizer for vtr imp, directional
# *: categorizer (ik) for intransitive non-imverative/directional

-> start

### TAM
start -> tam      [x:]      [tam=[+cmp,-imv,-prh,-prf,-stv,-fut],m=[TAM=x]]
# more constraints on k: incompletive or intransitive imperative except 3s and 2 pol
start -> tam      <kA:>     [tam=[-cmp,-prf,-imv,-prh,-stv],m=[TAM=k]];[tam=[+imv,-cmp,-prh,-prf,-stv,-fut],er=[-xpl],ab=[+p2,-frm],m=[TAM=k]];[tam=[+imv,-prh,-prf,-cmp,-stv,-fut],er=[-xpl],ab=[-frm,+plr],m=[TAM=k]]
start -> tam      [ch:]     [tam=[+imv,-prf,-cmp,-prh,-stv,-fut],m=[TAM=ch]]
start -> tam      [M:]      [tam=[+prh,-imv,-prf,-cmp,-stv,-fut],m=[TAM=m]]
start -> tam      [j:]      [tam=[+imv,-prh,-prf,-cmp,-stv,-fut],mov=[+xpl],m=[TAM=j]]
## handle the cases where there's no prefix
# perfect or stative
start -> tam      [:]       [tam=[+prf,-imv,-prh,-cmp,-stv,-fut],m=[TAM='0']] ; [tam=[-prf,-imv,-prh,-cmp,+stv,-fut],m=[TAM='0']]
# also various imperatives where the prefix is sometimes dropped?
# start -> tam    [:]       [tam=[+imv],er=[+p1,-p2,+plr],m=[TAM='0']]

### ABS
tam -> abs      <in:>     [ab=[+p1,-p2,-plr],m=[ABS=in]]
tam -> abs      <at:>     [ab=[-p1,+p2,-plr,-frm],m=[ABS=at]]
# Include both -oj- and -uj- variants
tam -> abs2p    [u:;o:]   [ab=[+p1,-p2,+plr],m=[ABS=oj]]
abs2p -> abs    [j:]
tam -> abs      <ix:>     [ab=[-p1,+p2,+plr,-frm],m=[ABS=ix]]
tam -> abs      [E:]      [ab=[-p1,-p2,+plr],m=[ABS="e"]]
# No explicit abs if 3p sing or 2p polite (which can't occur with 3p erg)
tam -> abs      [:]       [ab=[-p1,-p2,-plr],m=[ABS='0']] ; [ab=[-p1,+p2,+frm],er=[+p1,+xpl],m=[ABS='0']] ; [ab=[-p1,+p2,+frm],er=[-xpl],m=[ABS='0']]

### MOV
abs -> mov      [:]        [mov=[-xpl],m=[MOV=None]]
# differs only following e' (3p abs); otherwise e'
abs -> mov      <b'e:>     [mov=[+xpl,+go],m=[MOV="b'e"]]
abs -> mov      <ul:>      [mov=[+xpl,-go],m=[MOV=ul]]

### ERG
# No overt erg if intransitive or if erg is 2p polite
mov -> erg      [:]       [er=[-xpl],m=[ERG=None]] ; [er=[-p1,+p2,+frm,+xpl],ab=[-p2],m=[ERG='0']]
mov -> erg      [N:]      [er=[+p1,-p2,-plr,+xpl],ab=[-p1],m=[ERG=nu]]
mov -> erg      <aW:>     [er=[-p1,+p2,-plr,-frm,+xpl],ab=[-p2],m=[ERG=a]]
# Can't occur with polite abs
mov -> erg      [R:]      [er=[-p1,-p2,-plr,+xpl],ab=[-frm],m=[ERG=u]]
mov -> erg      [Q:]      [er=[+p1,-p2,+plr,+xpl],ab=[-p1],m=[ERG=qa]]
mov -> erg      <iW:>     [er=[-p1,+p2,+plr,-frm,+xpl],ab=[-p2],m=[ERG=i]]
# Can't occur with polite abs
mov -> erg      [K:]      [er=[-p1,-p2,+plr,+xpl],ab=[-frm],m=[ERG=ki]]

### ROOT
# because of possible derivational suffixes, these don't constrain transitivity
erg -> rz_vi      +vi+    [-pst]
erg -> rz_pos     +pos+   [+pst]
# transitive roots can't take causative suffix
erg -> rz_vtr     +vtr+   [-pst,der=[-cas]]
erg -> rz_vtd     +vtd+   [-pst,der=[-cas]]

### POSITIONAL ROOTS
# use the STATIVE form for imperative and perfect
rz_pos -> rz_vi      [L:]    [tam=[+imv]] ; [tam=[+prf]] ; [tam=[+stv]]
# use the ACTIVE form for other TAM
rz_pos -> rz_vi      <i':>   [tam=[-imv,-prf,-stv]]

### CAUSATIVE / TRANSITIVIZERS
## causative transitivizes intransitive root; voice can still be suffixed
# other allomorphs (-sa, -tisa) handled separately
rz_vi -> rz_vtd      <isa:>     [der=[+cas],m=[DER1=sa]]
# transitivizer for positionals
rz_pos -> rz_vtd     <vB:>      [der=[+cas],m=[DER1="b'a'"]]

### FREQUENTATIVE (VTR+VC1a'), IMMEDIATIVE (VT + (V)la')
# ! not clear what derivational affixes can co-occur
# ! or what has priority for the categorizer
# assume freq and imm exclude other derivational suffixes, including intransitivers
rz_vtr -> word_end  <vTa':>     [der=[+frq,-imm],m=[DER1=DUP,DER2=None]]
rz_vtr -> word_end  <vla':>     [der=[+imm,-frq],m=[DER1="la'",DER2=None]]
rz_vtd -> word_end  <la':>      [der=[+imm,-frq],m=[DER1="la'",DER2=None]]

### VOICE / INTRANSITIVIZERS
## create intransitive stems; no more derivation possible
## exclude imm and frq
## Mondloch's Voice 2: passive 1
rz_vtr -> bs_vi      [:]        [der=[+pas,-aps,-imm,-frq],er=[-xpl],m=[DER2=x]]  # actually lengthens the root vowel
rz_vtd -> bs_vi      [x:]       [der=[+pas,-aps,-imm,-frq],er=[-xpl],m=[DER2=x]]
## Mondloch's Voice 3: passive 2; special initial vowel rules
rz_vtr -> bs_vi      <^taj:>    [der=[+pas,-aps,-imm,-frq],er=[-xpl],m=[DER2=taj]]
rz_vtd -> bs_vi      <taj:>     [der=[+pas,-aps,-imm,-frq],er=[-xpl],m=[DER2=taj]]
rz_vtd -> bs_vi      <tal:>     [tam=[+stv],der=[+pas,-aps,-imm,-frq],er=[-xpl],m=[DER2=tal]]
# Mondloch's Voice 4 and 5 (VTD)
rz_vtd -> bs_vi      [n:]       [der=[+aps,-pas,-imm,-frq],er=[-xpl],m=[DER2=n]]
# Mondloch's Voice 4 (VTR); special initial vowel rules; what to call it though, middle??
rz_vtr -> bs_vi      <$n:>      [der=[+aps,-pas,-imm,-frq],er=[-xpl],m=[DER2=n]]
# Mondloch's Voice 5: antipassive; same initial vowel as active (voice 1)??
rz_vtr -> bs_vi      <Ow:>      [der=[+aps,-pas,-imm,-frq],er=[-xpl],m=[DER2=w]]

### NO INTRANSITIVE DERIVATIONAL AFFIXES
rz_vi -> bs_vi      [:]         [der=[-cas,-imm,-frq,-pas,-aps],er=[-xpl],m=[DER1=None,DER2=None]]
### NO TRANSITIVE DERIVATIONAL/VOICE AFFIXES
rz_vtr -> bs_vtr    [:]         [der=[-cas,-imm,-frq,-pas,-aps],er=[+xpl],m=[DER1=None,DER2=None]]
rz_vtd -> bs_vtd    [:]         [der=[-imm,-frq,-pas,-aps],er=[+xpl],m=[DER2=None]]

### CATEGORIZERS

## intransitive categorizers (do we need er=[-xpl] given the state?)
# this is usually ik, but changes following positional and -b'a' roots (at least)
bs_vi -> word_end     [*:]      [tam=[-prf,-imv],ab=[-frm],mov=[-xpl],+trm,m=[CAT=ik]]
# intransitive perfect; sometimes the i is not there?
bs_vi -> word_end     <inaq:>   [tam=[+prf],m=[CAT=naq]]
# Mondloch has -a when imperative -trm
bs_vi -> word_end     <oq:>     [tam=[+imv,-stv],m=[CAT=oq]] ; [mov=[+xpl],m=[CAT=oq]]
# No -ik if verb is non-terminal or 2p formal or future (-oq is always present?)
bs_vi -> word_end     [:]       [tam=[-prf,-imv],mov=[-xpl],ab=[-frm],-trm] ; [tam=[-prf,-imv],ab=[-p1,+p2,+frm],mov=[-xpl]] ; [tam=[+fut],mov=[-xpl]]

## transitive categorizers
# VTR
# completive, incompletive, negative imperative; no movement ;; either terminal or not 2p formal
bs_vtr -> word_end        [O:]      [tam=[-prf,-imv],ab=[-frm],er=[-frm,+xpl],mov=[-xpl],+trm,m=[CAT=o]]
# imperative, movement
bs_vtr -> word_end        [@:]      [tam=[+imv],er=[+xpl],m=[CAT=a]] ; [tam=[-prf],er=[+xpl],mov=[+xpl],m=[CAT=a]]
bs_vtr -> word_end        <om:>     [tam=[+prf],er=[+xpl],m=[CAT=om]]
# drop the suffix unless prf; fut or 2p formal (erg or abs) and not +mov or +imv
bs_vtr -> word_end        [:]       [tam=[-prf],ab=[-frm],er=[+xpl,-frm],-trm]; [tam=[+fut],mov=[-xpl]]; [tam=[-imv],mov=[-xpl],ab=[+frm]]; [tam=[-imv],mov=[-xpl],er=[+xpl,+frm]]
# VTD
# for phonetic case, need to worry about vowel redup for V'VVj
bs_vtd -> word_end        [j:]      [tam=[-prf],er=[+xpl],m=[CAT=j]]
bs_vtd -> word_end        [m:]      [tam=[+prf],er=[+xpl],m=[CAT=om]]

### FUTURE CLITIC
word_end -> fut           < na:>    [tam=[+fut],m=[FUT="na"]]
word_end -> fut           [:]       [tam=[-fut],m=[FUT=None]]

# no polite 2p clitic
fut -> end                [:]       [ab=[-frm],er=[-frm],m=[FORM=None]]

### POLITE 2p CLIITCS
fut -> end               < la:>     [ab=[-p1,+p2,-plr,+frm],m=[FORM=la]] ; [er=[-p1,+p2,-plr,+frm,+xpl],m=[FORM=la]]
fut -> end               < alaq:>   [ab=[-p1,+p2,+plr,+frm],m=[FORM=alaq]] ; [er=[-p1,+p2,+plr,+frm,+xpl],m=[FORM=alaq]]

end ->

### Irregular verbs

## k'oj: be
erg -> k'oj1       [k']
k'oj1 -> k'oj2     [o]              [der=[-cas,-imm,-frq,-pas,-aps],er=[-xpl],+pst,m=[DER1=None,DER2=None]]
# imperative, perfect stem`(k'ol instead of k'ojol)
k'oj2 -> bs_vi     [l:j]            [tam=[+imv,-cmp,-prf,-prh,-stv,-fut]] ; [tam=[-imv,-cmp,+prf,-prh,-stv,-fut]]

## b'e: go, only one of the variants ('e, e' not included)
erg -> b'e1   [b]
b'e1 -> b'e2  [e]
b'e2 -> rz_vi [n:]

## eta'ma
# special stative form

## ajawa: want, a in voice 1 (underived forms)
erg -> ajawa1      [a:]
ajawa1 -> ajawa2   [:j]
ajawa2 -> ajawa3   [:a]
ajawa3 -> ajawa4   [:w]
ajawa4 -> bs_vtd   [:a]             [-pst]

## tay: hear, ask
# voice 1
erg -> tay1        [t]
tay1 -> tay2       [o:a]
tay2 -> word_end   [:y]             [der=[-cas,-imm,-frq,-pas,-aps],+trm,er=[+xpl],-pst]
tay1 -> tay2a      [a]
tay2a -> word_end  [:y]             [der=[-cas,-imm,-frq,-pas,-aps],-trm,er=[+xpl],-pst]
# voice 5
tay2 -> bs_vi      [w:y]            [der=[+aps,-pas],er=[-xpl],-pst,m=[DER2=w]]
# voice 3
tay2a -> tay3a     [:y]
tay3a -> bs_vi     <taj:>           [der=[+pas,-aps],er=[-xpl],-pst,m=[DER2=taj]]
# voice 2 non-final: ta

## cha': say
# no -ik when final
erg -> cha'1       [ch]
cha'1 -> cha'2     [a]
cha'2 -> word_end  [']              [der=[-cas,-imm,-frq,-pas,-aps],+trm,tam=[-prf,-imv],er=[-xpl]]
