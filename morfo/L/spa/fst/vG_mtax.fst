###
### Morfotaxis de verbos españoles
###
### +- AL = América Latina (sin o con vosotros, vos)

-> start

# irregular participles
start -> pps    +irr_part+

start -> prepron  [:]     [pos=v]
### old version with pre-clitics
## start -> prepron >cl_pre<
## if no pre-clitics, either tenseless or continuous participle (possible post-clitics)
## or not clitics at all
##        [tam=[-tmp]] ; [tam=[+ger]] 
###

# prefixes which begin some irregular verbs
prepron           +prefix+
prepron -> stem   [:]

stem -> stem_e  +verbs_e+
stem -> stem_a  +verbs_a+
stem -> stem_i  +verbs_i+
# these specify different destination states
stem              +vb_irr+
stem -> caer      [:]
caer              +caer+
stem -> decir     [:]
decir             +decir+
stem -> ducir     [:]
ducir             +ducir+
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
# tú
stem_a1 -> end [a:]    [tm=ipv,sj=[-1,+2,-p],-VOS]
stem_e1 -> end [e:]    [tm=ipv,sj=[-1,+2,-p],-VOS]
stem_i1 -> end [e:]    [tm=ipv,sj=[-1,+2,-p],-VOS]
# vos
stem_a1 -> end  [á:]    [tm=ipv,sj=[-1,+2,-p],+VOS]
stem_e1 -> end  [é:]    [tm=ipv,sj=[-1,+2,-p],+VOS]
stem_i1 -> end  [í:]    [tm=ipv,sj=[-1,+2,-p],+VOS]
# vosotros
stem_a1 -> end  <ad:>    [tm=ipv,sj=[-1,+2,+p],-AL]
stem_e1 -> end  <ed:>    [tm=ipv,sj=[-1,+2,+p],-AL]
stem_i1 -> end  <id:>    [tm=ipv,sj=[-1,+2,+p],-AL]

# Presente
# 1s
a_sub_prs1 -> person    [o:]    [tm=prs,sj=[+1,-2,-p]]
e_sub_prs1 -> person    [o:]    [tm=prs,sj=[+1,-2,-p]]
# 2s vos, presente
stem_a1 -> end    <ás:>     [tm=prs,sj=[-1,+2,-p],+VOS]
stem_e1 -> end    <és:>     [tm=prs,sj=[-1,+2,-p],+VOS]
stem_i1 -> end    <ís:>     [tm=prs,sj=[-1,+2,-p],+VOS]
# 2p vosotros, presente
stem_a1 -> end    <áis:>     [tm=prs,sj=[-1,+2,+p],-AL]
stem_e1 -> end    <éis:>     [tm=prs,sj=[-1,+2,+p],-AL]
stem_i1 -> end    <ís:>     [tm=prs,sj=[-1,+2,+p],-AL]
# otras
stem_a1 -> prs    [a:]     [tm=prs]
stem_e1 -> prs    [e:]     [tm=prs]
# becomes e when not stressed
stem_i1 -> prs    [I:]     [tm=prs]
prs -> person    [:]       [sj=[-2,+p]] ; [sj=[-1,-2,-p]] ; [sj=[-1,+2,-p],-VOS]

# Futuro
stem_a -> fut    <ar':>   [tm=fut|cnd]
stem_e -> fut    <er':>   [tm=fut|cnd]
stem_i -> fut    <ir':>   [tm=fut|cnd]
# yo, nosotros, vosotros
fut -> person    [e:]     [sj=[+1],tm=fut];[sj=[+2,+p],tm=fut,-AL]
fut -> person    [a:]     [sj=[-1,-p],tm=fut];[sj=[-1,-2,+p],tm=fut]

# Condicional
fut -> person    <ía:>    [tm=cnd]

## Subjuntivo presente
# ar
a_sub_prs1 -> person [e:]   [sj=[-p],tm=sbp];[sj=[-2,+p],tm=sbp]
# vosotros
a_sub_prs1 -> end   <éis:>  [tm=sbp,sj=[-1,+2,+p],-AL]
# er,ir
e_sub_prs1 -> person [a:]   [sj=[-p],tm=sbp];[sj=[-2,+p],tm=sbp]
# vosotros
e_sub_prs1 -> end   <áis:>  [tm=sbp,sj=[-1,+2,+p],-AL]

# Imperfecto
stem_a1 -> person <'aba:>  [tm=ipf]
stem_e1 -> person <ía:>    [tm=ipf]
stem_i1 -> person <ía:>    [tm=ipf]

# Pretérito

# Orthographic changes may precede 1s é
# yo
stem_a -> end    [é:]     [tm=prt,sj=[+1,-p]]
# 3s
stem_a -> end    [ó:]     [tm=prt,sj=[-1,-2,-p]]
# tú, plur
stem_a -> prt2   [a:]     [tm=prt,sj=[+2,-p]] ; [tm=prt,sj=[+p]]
# subj
stem_a -> prt2   <'a:>    [tm=sbi]

stem_e -> ie_prt [:]      [tm=prt|sbi]
stem_i -> ie_prt [:]      [tm=prt|sbi]

ie_prt -> end     [í:]    [sj=[+1,-p],tm=prt]
ie_prt -> end     <ió:>   [sj=[-1,-2,-p],tm=prt]
# tú, vosotros, nosotros
ie_prt -> prt2    [i:]    [sj=[+2],tm=prt] ; [sj=[+1,-2,+p],tm=prt]
ie_prt -> prt2    <i'e:>  [sj=[-1,-2,+p]] ; [tm=sbi]

irr_prt -> end    [e:]    [sj=[+1,-p],tm=prt]
irr_prt -> end    [o:]    [sj=[-1,-2,-p],tm=prt]
# tú, vosotros, nosotros
irr_prt -> prt2   [i:]    [sj=[+2],tm=prt] ; [sj=[+1,-2,+p],tm=prt]
# 3p
irr_prt -> prt2   <i'e:>  [sj=[-1,-2,+p],tm=prt] ; [tm=sbi]

# Special person endings for preterite
prt2 -> end      <ste:>   [tm=prt,sj=[-1,+2,-p]]
# vosotros
prt2 -> end      <steis:> [tm=prt,sj=[-1,+2,+p],-AL]
prt2 -> end      <mos:>   [tm=prt,sj=[+1,-2,+p]]
prt2 -> end      <ron:>   [tm=prt,sj=[-1,-2,+p]]

# Subjuntivo imperfecto
prt2 -> person    <ra:>    [tm=sbi]
# prt2 -> person    <se:>    [tm=sbi]

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
stem_e1 -> ppr  <i'endo:>
stem_i1 -> ppr  <i'endo:>
ppr -> end  [:]      [tm=ger]

# Participio
stem_a1 -> pps       <ad:>
stem_e1 -> pps       <id:>
stem_i1 -> pps       <id:>
pps -> adjsuff      [:]    [pos=v,tm=prc]

# Person endings for most tenses/moods
# Don't consider hables, pongas, etc. to be imperative
person -> end      [s:]    [sj=[-1,+2,-p]]
# vosotros
person -> end      <is:>   [sj=[-1,+2,+p],-AL]
# nosotros
person -> end      <mos:>  [sj=[+1,-2,+p]]
# 3 pers plur non-imperative
person -> end      [n:]    [sj=[-1,-2,+p]]
# 2 pers (3 gram) plur imperative
# person -> end [n:]    [sj=[-1,-2,+p],tm=sbp];[sj=[-1,+2,+p],tm=sbp,+VOS]
# sing non-imperative; 1st or 3rd person
person -> end      [:]     [sj=[-p,-2]]
# 2 pers sing polite (3 gram) imperative
# person -> end [:]     [sj=[-1,-2,-p],tm=sbp]
# ;[tm=sbp,tam=[+sub,+tmp,-ger,-part,-inf,-ipv],sj=[+2,+p],-AL];[tm=sbp,tam=[+sub,+tmp,-ger,-part,-inf,-ipv],sj=[+2,+p],-AL]
## Object suffixes for imperative, pres part, and infinitive
#postpron -> end   >cl_post<

# Adjective suffixes for past part

adjsuff -> end     [o:]    [g=m,n=s]
adjsuff -> end     [a:]    [g=f,n=s]
adjsuff -> end     <os:>   [g=m,n=p]
adjsuff -> end     <as:>   [g=f,n=p]

end ->
