-> start

# No conjunction or preposition
start -> neg   [:]     [cn1=nil,pp=nil,-rel,-sub]

## CONJUNCTIONS (+sub is redundant)
# start -> neg    >>cn1<<

## PREPOSITIONS (+sub is redundant)
# start -> rel1  >>prep<<
# Relative with no preposition
start -> rel   [:]      [pp=nil,+sub,+rel]

## RELATIVE PREFIX (+sub is redundant)
# No relative prefix; could still be +rel if imperf
rel -> neg     [:]     [tm=imf,pp=nil,cn1=nil,+rel,+sub]
rel -> neg    <ye:>   [tm=prf,+rel,pp=nil,+sub]

## NEGATIVE PREFIX
neg -> neg_s      [e:]    [+neg,tm=prf];[+neg,tm=imf,+sub];[+neg,tm=j_i]
neg_s -> sbjp     [l:]    [tm=prf]
neg_s -> sbjp     [:]     [tm=imf];[tm=j_i]
# Non-subordinate imperfective negative
neg -> neg_si     [I:]    [+neg,tm=imf,-sub]
neg_si -> stem    <t_:>   [sb=[-p1,+p2]];[sb=[-p1,-p2,-plr,+fem]]
neg_si -> neg_si1 [l:]    [sb=[+p1]];[sb=[-p1,-p2,-plr,-fem]];[sb=[-p1,-p2,+plr]]
neg_si1 -> stem   <ew*_:> [sb=[+p1]]
neg_si1 -> stem   <*e:>   [sb=[-p1,-p2]]
# Affirmative
neg ->  sbjp      [:]     [-neg]

## SUBJECT PREFIX
# Prefix only for imperfective and jussive
sbjp -> stem      [:]    [tm=prf];[tm=ger];[tm=j_i,sb=[+p2],-neg]
sbjp -> sbjp*     [:]    [tm=imf];[tm=j_i,sb=[-p2]];[tm=j_i,+neg]
# When nothing precedes the subject prefix
sbjp* -> sbjp1    [:]    [-sub,-neg]
# Another prefix precedes the subject prefix
sbjp* -> sbjp1    [:]    [+sub];[+neg]
# Consonant
sbjp1 -> sbjp2    [l:]   [tm=j_i,sb=[+p1]];[tm=imf,-sub,+neg,sb=[+p1]];[tm=imf,sb=[+p1],cn1=l];[tm=imf,sb=[+p1],cn1=b];[tm=imf,sb=[+p1],cn1=t]
# y- also possible for 1p jussive (not given here)
sbjp1 -> sbjp2   <*y:>   [tm=imf,sb=[+p1,-p2]]; [sb=[-p1,-p2,+plr],-imprs]; [sb=[-p1,-p2,-plr,-fem],-imprs]; [sb=[-p1,-p2],+imprs]
# Unless at the beginning of the word there is no 1s prefix, except in jussive
sbjp1 -> stem     [:]    [tm=imf,sb=[+p1,-plr],ob=[-p1]]
# Treat t- and n- specially because they can be geminated in Amharic                   
sbjp1 -> sbjp_t   [t:]   [sb=[+p2,-p1],ob=[-p2]];[sb=[-plr,-p1,-p2,+fem]]
sbjp_t -> sbjp2   [:]
# Vowel                   
sbjp2 -> stem     [e:]   [tm=j_i]
sbjp2 -> stem     [:]    [tm=imf]

## STEM
# stem -> stem0     [:+]
##stem -> sbjs     <sebr:s> [tm=imf,vc=smp,as=smp]
##stem -> sbjs    <seber:s> [tm=prf,vc=smp,as=smp]
##stem -> sbjs     <bela:b> [tm=imf,vc=smp,as=smp]
stem -> sbjs      >>v_stem<<
# stem1 -> sbjs     [:+]                   

### SUBJECT SUFFIXES AND OBJECT INFIXES
sbjs -> sbjs_i    [:]    [tm=imf];[tm=j_i]
sbjs -> sbjs_p    [:]    [tm=prf]
## IMPERFECTIVE, JUSSIVE/IMPERATIVE
# 2/3 plural
# u is deleted preceding -b- unless it follows two consonants
sbjs_i -> obj     <0u:>  [sb=[-p1,+plr],ob=[+expl,+b],-imprs]
sbjs_i -> obj     [u:]   [sb=[-p1,+plr],ob=[-expl],-imprs] ; [sb=[-p1,+plr],ob=[+expl,-b],-imprs]
# 2sf
sbjs_i -> sbjs_ii [8:]   [sb=[+p2,-p1,+fem,-plr]]
# 1pp and impers
sbjs_i -> obj     <ne:>  [sb=[+p1,-p2,+plr]]
sbjs_i -> negs_aux [I:]  [+imprs,sb=[-p1,-p2],ob=[-expl]]
# No suffix
sbjs_i -> sbjs_i0 [:]    [sb=[+p2,-p1,-plr,-fem]];[sb=[+p1,-p2,-plr]];[sb=[-p1,-p2,-plr],-imprs]
# We apparently need to know how the stem ends
sbjs_i0 -> obj    [6:]  [ob=[+expl,-prp]]
sbjs_i0 -> obj    [:]    [ob=[-expl]];[ob=[+expl,+prp]]
## PERFECTIVE
# 3sm same for all languages                   
sbjs_p -> obj     [e:]   [tm=prf,sb=[-p1,-p2,-plr,-fem]]
# 1s, 2sm
# 7 realized as k after consonant, h after vowel
sbjs_p -> sbjs_pk     [7:]   [tm=prf,sb=[-plr]]
# 1s
sbjs_pk -> obj        [u:]   [sb=[+p1,-p2],ob=[-p1]]
# 2sm
sbjs_pk -> obj        [e:]   [sb=[-p1,+p2,-fem],ob=[-p2]]
# 2sf
sbjs_p -> sbjs_2sf_sa [x:]   [tm=prf,sb=[-p1,+p2,-plr,+fem],ob=[-p2]]
# No object infix before prep objects or 3sf
sbjs_2sf_sa -> obj    [:]    [ob=[-expl]];[ob=[+prp,+b,+expl]];[ob=[-p1,-p2,-plr,+fem,+expl]]
# Object infix before 1,2,3sm,3p
sbjs_2sf_sa -> obj    [I:]   [ob=[+p1,-p2,+expl,-b]];[ob=[-p1,+p2,+expl,-b]];[ob=[-p1,-p2,-plr,-fem,+expl,-b]];[ob=[+plr,+expl,-b]]
# 3sf
sbjs_p -> sbjs_3sf_s  [t:]   [tm=prf,sb=[-p1,-p2,-plr,+fem]]
# Infix for objects other than prep
sbjs_3sf_s -> obj     [e:]   [ob=[-prp,+expl]]
sbjs_3sf_s -> obj     [:]    [ob=[-expl]];[ob=[+prp,+expl]]
# 1p
sbjs_p -> obj        <ne:>   [tm=prf,sb=[+p1,+plr]]
# 2p: depends on preceding segment and whether b- follows
# -mmu, -kum(u), -m
sbjs_p -> obj         [2:]  [tm=prf,sb=[+p2,-p1,+plr]]
# 3p
sbjs_p -> obj         [u:]   [tm=prf,sb=[-p1,-p2,+plr],ob=[+expl,-b],-imprs];[tm=prf,sb=[-p1,-p2,+plr],ob=[-expl]]
# delete the u before detrimental -b unless two consonsants would come together
sbjs_p -> obj        <0u:>   [tm=prf,sb=[-p1,-p2,+plr],ob=[+expl,+b],-imprs]
# impersonal
sbjs_p -> negs_aux    [I:]   [tm=prf,+imprs,sb=[-p1,-p2],ob=[-expl]]

### OBJECT SUFFIXES
obj -> negs_aux    [:]     [ob=[-expl]]
# Prepositional
## b-
obj -> obj_b_sa0       [b:]   [ob=[+prp,+b,+expl]]
# -bu following u (-ku, -u, -kumu), -bI otherwise
obj_b_sa0 -> negs_aux  <Et:>  [ob=[-p1,-p2,-plr,+fem]]
obj_b_sa0 -> obj_b_sa0* [:]   [ob=[+plr]]; [ob=[+p1,-plr]]; [ob=[+p2,-plr]]; [ob=[-p1,-p2,-plr,-fem]]                       
obj_b_sa0* -> obj_s_bu  [u:]  [sb=[-p1,+plr]];[tm=prf,sb=[+p1,-p2,-plr]]
obj_b_sa0* -> obj_s_b   [:]   [sb=[+p1,+plr]];[tm=imf,sb=[-plr]];[tm=j_i,sb=[-plr]];[tm=prf,sb=[-p1,-plr]]
obj_s_b -> negs_aux    [i:]   [ob=[-p1,-p2,-plr,-fem]]
obj_s_b -> negs_aux   <im_u:> [ob=[-p1,-p2,+plr]]
obj_s_b -> negs_aux    <IN:>  [ob=[+p1,-p2,-plr]]
obj_s_b -> negs_aux    <Ine:> [ob=[+p1,-p2,+plr]]
obj_s_b -> negs_aux    <Ihe:> [ob=[-p1,+p2,-plr,-fem]]
obj_s_b -> negs_aux    <Ix:>  [ob=[-p1,+p2,-plr,+fem]]
obj_s_b -> negs_aux   <Im_u:> [ob=[-p1,+p2,+plr]]
obj_s_bu -> negs_aux   [y:]   [ob=[-p1,-p2,-plr,-fem]]
obj_s_bu -> negs_aux  <ymu:>  [ob=[-p1,-p2,+plr]]
obj_s_bu -> negs_aux   [N:]   [ob=[+p1,-p2,-plr]]
obj_s_bu -> negs_aux   <ne:>  [ob=[+p1,-p2,+plr]]
obj_s_bu -> negs_aux   <he:>  [ob=[-p1,+p2,-plr,-fem]]
obj_s_bu -> negs_aux   [x:]   [ob=[-p1,+p2,-plr,+fem]]
obj_s_bu -> negs_aux  <m_u:>  [ob=[-p1,+p2,+plr]]
## l-
obj -> negs_aux       <N_:>   [ob=[+p1,-p2,-plr,+prp,+l,+expl]]
obj -> negs_aux       <n_e:>  [ob=[+p1,-p2,+plr,+prp,+l,+expl]]
obj -> negs_aux       <nke:>  [ob=[-p1,+p2,-plr,-fem,+prp,+l,+expl]]
obj -> negs_aux       <nx:>   [ob=[-p1,+p2,-plr,+fem,+prp,+l,+expl]]
obj -> negs_aux       <n_i:>  [ob=[-p1,-p2,-plr,-fem,+prp,+l,+expl]]
obj -> negs_aux      <n_Et:>  [ob=[-p1,-p2,-plr,+fem,+prp,+l,+expl]]
obj -> negs_aux       <nkum:> [ob=[-p1,+p2,+plr,+prp,+l,+expl]]
obj -> negs_aux     <n_im_u:> [ob=[-p1,-p2,+plr,+prp,+l,+expl]]
# Non-prepositional
obj -> obj_sa          [:]    [ob=[-prp,+expl]]
# Pronouns
obj_sa -> negs_aux     [N:]   [ob=[+p1,-p2,-plr]]
obj_sa -> negs_aux    <7e:>  [ob=[-p1,+p2,-plr,-fem]]
obj_sa -> negs_aux     [x:]   [ob=[-p1,+p2,-plr,+fem]]
# w, ew, t
obj_sa -> negs_aux     [y:]   [ob=[-p1,-p2,-plr,-fem]]  # ,-prp]]
obj_sa -> negs_aux    <Et:>   [ob=[-p1,-p2,-plr,+fem]]
obj_sa -> negs_aux    <ne:>   [ob=[+p1,-p2,+plr]]
# Never -kum (except after b-)
obj_sa -> negs_aux   <m_u:>   [ob=[-p1,+p2,+plr]]
# Never -immu (except after n- and b-)
obj_sa -> negs_aux   <ymu:>   [ob=[-p1,-p2,+plr]]

## NEGATIVE SUFFIX: required if verb is independent or AUXILIARY VERB
# AUX
negs_aux -> aux1   [a:]        [tm=imf,-neg,ax=al];[tm=prf,-neg,ax=al]
aux1 -> cn2       <hu:>       [sb=[+p1,-p2,-plr]]
aux1 -> cn2       <ha:>       [sb=[-p1,+p2,-plr,-fem]]
aux1 -> cn2       [x:]        [sb=[-p1,+p2,-plr,+fem]]
aux1 -> cn2       [t:]        [sb=[-p1,-p2,-plr,+fem]]
aux1 -> cn2       <m_u:>      [sb=[-p1,+p2,+plr]]
aux1 -> cn2       [n:]        [sb=[-p1,-p2,-plr,-fem]];[sb=[+p1,-p2,+plr]];[sb=[-p1,-p2,+plr]];[sb=[-p1,-p2],+imprs]
# NEGATIVE
# No negs_aux: juss_imp
negs_aux -> cn2  [:]          [tm=j_i];[tm=prf,ax=nil];[tm=imf,ax=nil]

## CONJUNCTIVE SUFFIXES
##cn2 -> end  [n:]         [cn2=n]
##cn2 -> end  [s:]         [cn2=s]
cn2 -> end  [:]          [cn2=nil]

end ->
