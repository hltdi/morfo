###
### Morfotaxis de verbos españoles
###

-> start

start -> mood    [:]     [pos=v,+fin,tm=prs|fut|prt|sbp|sbi|ipf|cnd|ipv];[pos=v,-fin,tm=ger|inf|prc]

# irregular participles
mood -> pps    +irr_part+

mood -> prepron  [:]     [pos=v]

# prefixes which begin some irregular verbs
prepron           +prefix+
prepron -> stem   [:]

stem -> stem_e  +verbs_e+
stem -> stem_a  +verbs_a+
stem -> stem_i  +verbs_i+
# these specify different destination states;
# separate states are needed for particular verbs so that prefix.lex can refer to them
stem              +vb_irr+
stem -> caer      [:]
caer              +caer+
stem -> decir     [:]
decir             +decir+
stem -> ducir     [:]
ducir             +ducir+
stem -> oír       [:]
oír               +oir+
stem -> poner     [:]
poner             +poner+
stem -> tener     [:]
tener             +tener+
stem -> traer     [:]
traer             +traer+
stem -> venir     [:]
venir             +venir+
stem -> ver       [:]
ver               +ver+

# Presente 2,3,1p; imperativo familiar; infinitivo; imperfecto;
# participio; gerundio (no futuro, pretérito, subjuntivo, presente 1s)
stem_a -> stem_a1      [:]     [tm=prs|ipv|inf|ipf|ger|prc]
stem_e -> stem_e1      [:]     [tm=prs|ipv|inf|ipf|ger|prc]
stem_i -> stem_i1      [:]     [tm=prs|ipv|inf|ipf|ger|prc]

# Subjuntivo presente, presente 1s ##, imperativo formal
stem_a -> a_sub_prs1   [:]     [tm=prs|sbp]
stem_e -> e_sub_prs1   [:]     [tm=prs|sbp]
stem_i -> e_sub_prs1   [:]     [tm=prs|sbp]

# Imperativo
# tú, -VOS
stem_a1 -> end [a:]    [tm=ipv,p=2,n=0,-VOS,+ipv]
stem_e1 -> end [e:]    [tm=ipv,p=2,n=0,-VOS,+ipv]
stem_i1 -> end [e:]    [tm=ipv,p=2,n=0,-VOS,+ipv]
# vos
stem_a1 -> end  [á:]    [tm=ipv,p=2,n=0,+ipv]
stem_e1 -> end  [é:]    [tm=ipv,p=2,n=0,+ipv]
stem_i1 -> end  [í:]    [tm=ipv,p=2,n=0,+ipv]
# vosotros
#stem_a1 -> end  <ad:>    [tm=ipv,sj=[-1,+2,+p],-AL,+ipv]
#stem_e1 -> end  <ed:>    [tm=ipv,sj=[-1,+2,+p],-AL,+ipv]
#stem_i1 -> end  <id:>    [tm=ipv,sj=[-1,+2,+p],-AL,+ipv]

# Presente
# 1s
a_sub_prs1 -> person    [o:]    [tm=prs,p=1,n=0]
e_sub_prs1 -> person    [o:]    [tm=prs,p=1,n=0]
# 2s vos, presente
stem_a1 -> end    <ás:>     [tm=prs,p=2,n=0]
stem_e1 -> end    <és:>     [tm=prs,p=2,n=0]
stem_i1 -> end    <ís:>     [tm=prs,p=2,n=0]
# 2p vosotros, presente
#stem_a1 -> end    <áis:>     [tm=prs,sj=[-1,+2,+p],-AL]
#stem_e1 -> end    <éis:>     [tm=prs,sj=[-1,+2,+p],-AL]
#stem_i1 -> end    <ís:>     [tm=prs,sj=[-1,+2,+p],-AL]
# otras
stem_a1 -> prs    [a:]     [tm=prs]
stem_e1 -> prs    [e:]     [tm=prs]
# becomes e when not stressed
stem_i1 -> prs    [I:]     [tm=prs]
prs -> person    [:]       [n=1,p=1|3] ; [n=0,p=3] ; [p=2,n=0,-VOS]

# Futuro
stem_a -> fut    <ar':>   [tm=fut|cnd]
stem_e -> fut    <er':>   [tm=fut|cnd]
stem_i -> fut    <ir':>   [tm=fut|cnd]
# yo, nosotros, vosotros
fut -> person    [e:]     [p=1,tm=fut]  # ;[sj=[+2,+p],tm=fut]
fut -> person    [a:]     [p=2|3,n=0,tm=fut];[p=3,n=1,tm=fut]

# Condicional
fut -> person    <ía:>    [tm=cnd]

## Subjuntivo presente
# ar
a_sub_prs1 -> person [e:]   [n=0,tm=sbp];[p=1|3,n=1,tm=sbp]
# vosotros
#a_sub_prs1 -> end   <éis:>  [tm=sbp,sj=[-1,+2,+p],-AL]
# er,ir
e_sub_prs1 -> person [a:]   [n=0,tm=sbp];[n=1,p=1|3,tm=sbp]
# vosotros
#e_sub_prs1 -> end   <áis:>  [tm=sbp,sj=[-1,+2,+p],-AL]

# Imperfecto
stem_a1 -> person <'aba:>  [tm=ipf]
stem_e1 -> person <ía:>    [tm=ipf]
stem_i1 -> person <ía:>    [tm=ipf]

# Pretérito

# Orthographic changes may precede 1s é
# yo
stem_a -> end    [é:]     [tm=prt,p=1,n=0]
# 3s
stem_a -> end    [ó:]     [tm=prt,n=0,p=3]
# tú, plur
stem_a -> prt2   [a:]     [tm=prt,p=2,n=0] ; [tm=prt,n=1]
# subj
stem_a -> prt2   <'a:>    [tm=sbi]

stem_e -> ie_prt [:]      [tm=prt|sbi]
stem_i -> ie_prt [:]      [tm=prt|sbi]

ie_prt -> end     [í:]    [p=1,n=0,tm=prt]
ie_prt -> end     <ió:>   [p=3,n=0,tm=prt]
# tú, vos, vosotros, nosotros
ie_prt -> prt2    [i:]    [p=2,n=0,tm=prt] ; [p=1,n=1,tm=prt]
ie_prt -> prt2    <i'e:>  [p=3,n=1] ; [tm=sbi]

irr_prt -> end    [e:]    [p=1,n=0,tm=prt]
irr_prt -> end    [o:]    [p=3,n=0,tm=prt]
# tú, vos, vosotros, nosotros
irr_prt -> prt2   [i:]    [p=2,n=0,tm=prt] ; [p=1,n=1,tm=prt]
# 3p
irr_prt -> prt2   <i'e:>  [p=3,n=1,tm=prt] ; [tm=sbi]

# Special person endings for preterite
prt2 -> end      <ste:>   [tm=prt,p=2,n=0]
# vosotros
#prt2 -> end      <steis:> [tm=prt,sj=[-1,+2,+p],-AL]
prt2 -> end      <mos:>   [tm=prt,p=1,n=1]
prt2 -> end      <ron:>   [tm=prt,p=3,n=1]

# Subjuntivo imperfecto
prt2 -> person    <ra:>    [tm=sbi]
prt2 -> person    <se:>    [tm=sbi]

# Infinitivo
stem_a1 -> inf    <ar:>
# Realize the special vowel I as i when there is another vowel other than i,
#   as e otherwise
# Convert U to O (when no vowel follows)
# and IE to ! or E
stem_e1 -> inf    <er:>
stem_i1 -> inf    <ir:>
inf -> end  [:]     [tm=inf]

# Gerundio
stem_a1 -> ppr  <ando:> 
stem_e1 -> ppr  <iendo:>
stem_i1 -> ppr  <iendo:>
ppr -> end  [:]      [tm=ger]

# Participio
stem_a1 -> pps       <ad:>
stem_e1 -> pps       <id:>
stem_i1 -> pps       <id:>
pps -> adjsuff      [:]    [pos=v,tm=prc]

# Person endings for most tenses/moods
# Don't consider hables, pongas, etc. to be imperative
person -> end      [s:]    [p=2,n=0]
# vosotros
#person -> end      <is:>   [sj=[-1,+2,+p],-AL]
# nosotros
person -> end      <mos:>  [p=1,n=1]
# 3 pers plur non-imperative
person -> end      [n:]    [p=3,n=1]
# 2 pers (3 gram) plur imperative
# person -> end [n:]    [p=3,n=1,tm=sbp];[sj=[-1,+2,+p],tm=sbp]
# sing non-imperative; 1st or 3rd person
person -> end      [:]     [p=1|3,n=0]
# 2 pers sing polite (3 gram) imperative
# person -> end [:]     [p=3,n=0,tm=sbp]
## Object suffixes for imperative, pres part, and infinitive
#postpron -> end   >cl_post<

# Adjective suffixes for past part

adjsuff -> end     [o:]    [g=m,n=0]
adjsuff -> end     [a:]    [g=f,n=0]
adjsuff -> end     <os:>   [g=m,n=1]
adjsuff -> end     <as:>   [g=f,n=1]

end ->
