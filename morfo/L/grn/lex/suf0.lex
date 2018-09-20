### PATTERNS
## previous accented or nasal vowel (constrain length?)
pat: pre_acc ([áéíóúý])(\w*?)$
pat: pre_nasv ([ãẽĩõũỹ])(\w*?)$
## previous unaccented (constrain length?)
pat: pre_unacc ([^áéíóúý]*?)([aeiouy])$
pat: last_acc ([áéíóúý])$
pat: last_nasv ([ãẽĩõũỹ])i??$
## accented but on last vowel
pat: acc_notlast [áéíóúý]\w*?[aeiouy]$
pat: final_e (\w*?)([eéẽ])$
pat: anything (\w*?)$

#### FEATURE STRUCTURES
# anything
gram: any []
# non-negative
gram: nonneg [-neg]
# negative
gram: neg [+neg]
# no pregrad suffix
gram: nopregrd [pregrd=None]
# imperative or optative
gram: impopt [mod=imp];[mod=opt]
# Person/number specific forms
gram: 1s [sj=[+1,-2,-p]]
gram: 2s [sj=[-1,+2,-p]]
gram: 3  [sj=[-1,-2]]
gram: 1pe [sj=[+1,-2,+p]]
gram: 1pi [sj=[+1,+2,+p]]
gram: 2p [sj=[-1,+2,+p]]

#### FUNCTIONS
## Accent last
func: accent_last n=2, acc=2
## Deaccent all
func: deaccent n=1, deacc=1
## Insert * (deaccent character)
func: ins_deacc n=1, ins='*'
## Insert * after e
func: ins_deacc_e n=2, ins='*'

#### SUFFIXES

#### VERBS
pos: v

### ONE ONLY

## Ára
# pretonic
#suf: va +va
#  pat=last_acc; change=deaccent; gram=any
#  pat=last_nasv; gram=any
#  pat=acc_notlast; gram=any
#suf: mi +mi1
#  # mi1: atonic, past
#  pat=last_acc; change=deaccent; gram=any
#  pat=last_nasv; gram=any
#  pat=acc_notlast; gram=any
#  # mi2: tonic, softening
#  pat=anything; change=ins_deacc; gram=impopt; aff=+mi2
#suf: ke +ke
#  pat=last_acc; change=deaccent; gram=impopt
#  pat=last_nasv; gram=impopt
#  pat=acc_notlast; gram=impopt
#suf: na +na
#  pat=last_acc; change=deaccent; gram=impopt
#  pat=last_nasv; gram=impopt
#  pat=acc_notlast; gram=impopt
# jussive py
suf: py +py1
  pat=last_acc; change=deaccent; gram=impopt
  pat=last_nasv; gram=impopt
  pat=acc_notlast; gram=impopt
#suf: ne +ne
#  pat=last_acc; change=deaccent; gram=any
#  pat=last_nasv; gram=any
#  pat=acc_notlast; gram=any
#suf: tei +tei
#  pat=last_acc; change=deaccent; gram=any
#  pat=last_nasv; gram=any
#  pat=acc_notlast; gram=any
suf: kuri +kuri
  pat=last_acc; change=deaccent; gram=any
  pat=last_nasv; gram=any
  pat=acc_notlast; gram=any
# tonic cancelling previous (ipu'atãva)
#suf: va'ekue +va'ekue
#  pat=anything; change=ins_deacc; gram=any
#suf: va'erã +va'erã
#  pat=anything; change=ins_deacc; gram=any
#suf: kuévo +kuévo
#  pat=anything; change=ins_deacc; gram=any
#suf: pota +Pota
#  pat=anything; change=ins_deacc; gram=any
#suf: mbota +Pota
#  pat=anything; change=ins_deacc; gram=any
#suf: 'arã +'arã
#  pat=anything; change=ins_deacc; gram=any
#suf: 'akue +'akue
#  pat=anything; change=ins_deacc; gram=any
suf: rãngue +rãngue
  pat=anything; change=ins_deacc; gram=any
suf: raka'e +raka'e
  pat=anything; change=ins_deacc; gram=any
suf: ra'e +ra'e
  pat=anything; change=ins_deacc; gram=any
# Person/number specific forms
suf: 'aína +hína
  pat=anything; change=ins_deacc; gram=1s
suf: reína +hína
  pat=anything; change=ins_deacc; gram=2s
suf: hína +hína
  pat=anything; change=ins_deacc; gram=3
suf: ñaína +ñaína
  pat=anything; change=ins_deacc; gram=1pi
suf: roína +roína
  pat=anything; change=ins_deacc; gram=1pe
suf: peína +peína
  pat=anything; change=ins_deacc; gram=2p
suf: 'aikóni +hikóni
  pat=anything; change=ins_deacc; gram=1s
suf: reikóni +hikóni
  pat=anything; change=ins_deacc; gram=2s
suf: hikóni +hikóni
  pat=anything; change=ins_deacc; gram=3
suf: ñaikóni +hikóni
  pat=anything; change=ins_deacc; gram=1pi
suf: roikóni +hikóni
  pat=anything; change=ins_deacc; gram=1pe
suf: peikóni +hikóni
  pat=anything; change=ins_deacc; gram=2p

## Ñe'ẽteko 1: nte
suf: nte +nte
  pat=last_acc; change=deaccent; gram=any
  pat=last_nasv; gram=any
  pat=acc_notlast; gram=any

## Ñe'ẽteko 2: miscellaneous aspect
#suf: jevy +jevy
#  pat=anything; change=ins_deacc; gram=any
#suf: jey +jevy
#  pat=anything; change=ins_deacc; gram=any
#suf: 'ypy +'ypy
#  pat=anything; change=ins_deacc; gram=any
#suf: ma +ma
#  pat=last_acc; change=deaccent; gram=any
#  pat=last_nasv; gram=any
#  pat=acc_notlast; gram=any
suf: vo +vo
  pat=last_acc; change=deaccent; gram=any
  pat=last_nasv; gram=any
  pat=acc_notlast; gram=any
suf: voi +voi
  pat=last_acc; change=deaccent; gram=any
  pat=last_nasv; gram=any
  pat=acc_notlast; gram=any
suf: vove +vove
  pat=last_acc; change=deaccent; gram=any
  pat=last_nasv; gram=any
  pat=acc_notlast; gram=any

## Ñe'ẽteko 3: more miscellaneous aspect
# Pretonic
# rare?
#suf: 'anga +'anga
#  pat=last_acc; change=deaccent; gram=any
#  pat=last_nasv; gram=any
#  pat=acc_notlast; gram=any
# rare?
suf: mba'e +mba'e
  pat=last_acc; change=deaccent; gram=any
  pat=last_nasv; gram=any
  pat=acc_notlast; gram=any
# also -ramõ?
suf: ramo +ramo
  pat=last_acc; change=deaccent; gram=any
  pat=last_nasv; gram=any
  pat=acc_notlast; gram=any
# same as ramo??
suf: rõ +rõ
  pat=last_acc; change=deaccent; gram=any
  pat=last_nasv; gram=any
  pat=acc_notlast; gram=any
suf:  vaicha +vaicha
  pat=last_acc; change=deaccent; gram=any
  pat=last_nasv; gram=any
  pat=acc_notlast; gram=any
suf:  nga'u +nga'u
  pat=last_acc; change=deaccent; gram=any
  pat=last_nasv; gram=any
  pat=acc_notlast; gram=any
suf: rupi +rupi
  pat=last_acc; change=deaccent; gram=any
  pat=last_nasv; gram=any
  pat=acc_notlast; gram=any
suf: sapy'a +sapy'a
  pat=last_acc; change=deaccent; gram=any
  pat=last_nasv; gram=any
  pat=acc_notlast; gram=any
#suf: jepi +jepi
#  pat=last_acc; change=deaccent; gram=any
#  pat=last_nasv; gram=any
#  pat=acc_notlast; gram=any
suf: ndaje +ndaje
  pat=last_acc; change=deaccent; gram=any
  pat=last_nasv; gram=any
  pat=acc_notlast; gram=any
# alternate
suf: je +ndaje
  pat=last_acc; change=deaccent; gram=any
  pat=last_nasv; gram=any
  pat=acc_notlast; gram=any
suf: niko +niko
  pat=last_acc; change=deaccent; gram=any
  pat=last_nasv; gram=any
  pat=acc_notlast; gram=any
# alternate
suf: ningo +niko
  pat=last_acc; change=deaccent; gram=any
  pat=last_nasv; gram=any
  pat=acc_notlast; gram=any
suf: ngo +ngo
  pat=last_acc; change=deaccent; gram=any
  pat=last_nasv; gram=any
  pat=acc_notlast; gram=any
suf: ko +ko
  pat=last_acc; change=deaccent; gram=any
  pat=last_nasv; gram=any
  pat=acc_notlast; gram=any
suf: nipo +nipo
  pat=last_acc; change=deaccent; gram=any
  pat=last_nasv; gram=any
  pat=acc_notlast; gram=any
# alternate
suf: po +nipo
  pat=last_acc; change=deaccent; gram=any
  pat=last_nasv; gram=any
  pat=acc_notlast; gram=any
# alternate
suf: pipo +nipo
  pat=last_acc; change=deaccent; gram=any
  pat=last_nasv; gram=any
  pat=acc_notlast; gram=any
# Tonic
suf: guare +guare
  pat=anything; change=ins_deacc; gram=any
# apparently also atonic
suf: mante +mante
  pat=anything; change=ins_deacc; gram=any
  pat=last_acc; change=deaccent; gram=any
  pat=last_nasv; gram=any
  pat=acc_notlast; gram=any
#suf: gua'u +gua'u
#  pat=anything; change=ins_deacc; gram=any
# apparently also atonic
suf: katu +katu
  pat=anything; change=ins_deacc; gram=any
  pat=last_acc; change=deaccent; gram=any
  pat=last_nasv; gram=any
  pat=acc_notlast; gram=any

## Ñe'ẽteko 4: relativity
suf: ha +ha
  pat=anything; change=ins_deacc; gram=any
suf: hague +hague
  pat=anything; change=ins_deacc; gram=any
suf: haguã +haguã
  pat=anything; change=ins_deacc; gram=any
# alternate spelling
suf: haĝua +haguã
  pat=anything; change=ins_deacc; gram=any

## Interrogative
suf: pa +pa
  pat=last_acc; change=deaccent; gram=any
  pat=last_nasv; gram=any
  pat=acc_notlast; gram=any
suf: piko +piko  
  pat=last_acc; change=deaccent; gram=any
  pat=last_nasv; gram=any
  pat=acc_notlast; gram=any

### Nominalization, adjectivization
#suf: py +py2

### TWO OR MORE
## Ára +

## ma+
#suf: maha +ma+ha
#  # Both accented ...
#  pat=anything; change=ins_deacc; gram=any
#  # and pre-accented
#  pat=last_acc; change=deaccent; gram=any
#  pat=last_nasv; gram=any
#  pat=acc_notlast; gram=any
#suf: makatu +ma+katu
#  pat=last_acc; change=deaccent; gram=any
#  pat=last_nasv; gram=any
#  pat=acc_notlast; gram=any
#suf: mandi +ma+ndi
#  pat=last_acc; change=deaccent; gram=any
#  pat=last_nasv; gram=any
#  pat=acc_notlast; gram=any
#suf: mara'e +ma+ra'e
#  pat=last_acc; change=deaccent; gram=any
#  pat=last_nasv; gram=any
#  pat=acc_notlast; gram=any
#suf: maramo +ma+ramo
#  pat=last_acc; change=deaccent; gram=any
#  pat=last_nasv; gram=any
#  pat=acc_notlast; gram=any
#suf: mava'ekue +ma+va'ekue
#  pat=anything; change=ins_deacc; gram=any
#suf: mava'erã +ma+va'erã
#  pat=anything; change=ins_deacc; gram=any
#suf: mava'erãha +ma+va'erã+ha
#  pat=anything; change=ins_deacc; gram=any
#suf: mavoi +ma+voi
#  pat=last_acc; change=deaccent; gram=any
#  pat=last_nasv; gram=any
#  pat=acc_notlast; gram=any
#suf: mavoíkuri +ma+voi+kuri
#  pat=anything; change=ins_deacc; gram=any
#suf: mavoíra'e +ma+voi+ra'e
#  pat=anything; change=ins_deacc; gram=any
#suf: mavoínte +ma+voi+nte
#  pat=anything; change=ins_deacc; gram=any
#suf: ma'aína +ma+hína
#  pat=anything; change=ins_deacc; gram=1s
#suf: mareína +ma+hína
#  pat=anything; change=ins_deacc; gram=2s
#suf: mahína +ma+hína
#  pat=anything; change=ins_deacc; gram=3
#suf: mañaína +ma+hína
#  pat=anything; change=ins_deacc; gram=1pi
#suf: maroína +ma+hína
#  pat=anything; change=ins_deacc; gram=1pe
#suf: mapeína +ma+hína
#  pat=anything; change=ins_deacc; gram=2p

## mi1+  past
#suf: míma +mi1+ma
#  pat=anything; change=ins_deacc; gram=any
# only occurs with romba'apo+
#suf: mímante +mi1+mante
#  pat=anything; change=ins_deacc; gram=any
#suf: míta +mi1+ta
#  # past + future?
#  pat=anything; change=ins_deacc; gram=any
#suf: mítava +mi1+ta+va
#  pat=anything; change=ins_deacc; gram=any
#suf: miva'ekue +mi1+va'ekue
#  # in both patterns??; past + past ??
#  pat=last_acc; change=deaccent; gram=any
#  pat=last_nasv; gram=any
#  pat=acc_notlast; gram=any
#  pat=anything; change=ins_deacc; gram=any
#suf: miva'erã +mi1+va'erã
#  # in both patterns??; past + future ??
#  pat=last_acc; change=deaccent; gram=any
#  pat=last_nasv; gram=any
#  pat=acc_notlast; gram=any
#  pat=anything; change=ins_deacc; gram=any
#suf: miva'erãmo'ã +mi1+va'erã+mo'ã
#  pat=anything; change=ins_deacc; gram=any
#suf: miva'erãre +mi1+va'erã+re
#  pat=anything; change=ins_deacc; gram=any
#suf: miva'erãnte +mi1+va'erã+nte
#  pat=anything; change=ins_deacc; gram=any
#suf: mivoi +mi1+voi
#  pat=anything; change=ins_deacc; gram=any
#suf: mivoínte +mi1+voi+nte
#  pat=anything; change=ins_deacc; gram=any
## minte/mínte... mimante... (probably others)
#suf: minte +mi1+nte
#  pat=anything; change=ins_deacc; gram=any
#suf: mínte +mi1+nte
#  pat=anything; change=ins_deacc; gram=any
#suf: mínteko +mi1+nte+ko
#  pat=anything; change=ins_deacc; gram=any
#suf: minteva'erã +mi1+nte+va'erã
#  pat=anything; change=ins_deacc; gram=any
#suf: minte'akue +mi1+nte+'akue
#  pat=anything; change=ins_deacc; gram=any
#suf: mintevoi +mi1+nte+voi
#  pat=anything; change=ins_deacc; gram=any
#suf: mimante +mi1+mante
#  pat=anything; change=ins_deacc; gram=any
#suf: mimanteva'erã +mi1+mante+va'erã
#  pat=anything; change=ins_deacc; gram=any
## miha ... (ha followed by any postposition?)
#suf: miha +mi1+ha
#  pat=anything; change=ins_deacc; gram=any
#suf: miháicha +mi1+ha+icha
#  pat=anything; change=ins_deacc; gram=any
#suf: miháichante +mi1+ha+icha+nte
#  pat=anything; change=ins_deacc; gram=any
#suf: miháichamante +mi1+ha+icha+mante
#  pat=anything; change=ins_deacc; gram=any
#suf: mihápe +mi1+ha+pe
#  pat=anything; change=ins_deacc; gram=any
#suf: mihápente +mi1+ha+pe+nte
#  pat=anything; change=ins_deacc; gram=any
#suf: miháre +mi1+ha+re
#  pat=anything; change=ins_deacc; gram=any
#suf: mihárupi +mi1+ha+rupi
#  pat=anything; change=ins_deacc; gram=any
#suf: míva +mi1+va
#  pat=anything; change=ins_deacc; gram=any
#suf: mívape +mi1+va+pe
#  pat=anything; change=ins_deacc; gram=any
#suf: mívare +mi1+va+re
#  pat=anything; change=ins_deacc; gram=any
#suf: mívo +mi1+vo
#  pat=anything; change=ins_deacc; gram=any
#suf: míngo +mi1+ngo
#  pat=anything; change=ins_deacc; gram=any
#suf: míniko +mi1+niko
#  pat=anything; change=ins_deacc; gram=any
#suf: míningo +mi1+ningo
#  pat=anything; change=ins_deacc; gram=any
#suf: míramo +mi1+ramo
#  pat=anything; change=ins_deacc; gram=any
#suf: mírõ +mi1+rõ
#  pat=anything; change=ins_deacc; gram=any
#suf: mírente +mi1+re+nte
#  pat=anything; change=ins_deacc; gram=any
#suf: mírentevoi +mi1+re+nte+voi
#  pat=anything; change=ins_deacc; gram=any
#suf: mi'akue +mi1+'akue
#  pat=anything; change=ins_deacc; gram=any
#suf: mi'arã +mi1+'arã
#  pat=anything; change=ins_deacc; gram=any
#suf: mihague +mi1+hague
#  pat=anything; change=ins_deacc; gram=any
#suf: miraka'e +mi1+raka'e
#  pat=anything; change=ins_deacc; gram=any

## mi2+  softened
#suf: míke +mi2+ke
#  pat=anything; change=ins_deacc; gram=impopt
#suf: míkena +mi2+ke+na
#  pat=anything; change=ins_deacc; gram=impopt
#suf: mína +mi2+na
#  pat=anything; change=ins_deacc; gram=impopt
#suf: mívante +mi2+va+nte
#  pat=anything; change=ins_deacc; gram=impopt
#suf: mívanteko +mi2+va+nte+ko
#  pat=anything; change=ins_deacc; gram=impopt

## 'akue+
#suf: 'akuéko +'akue+ko
 # pat=anything; change=ins_deacc; gram=any
#suf: 'akuénte +'akue+nte
#  pat=anything; change=ins_deacc; gram=any
#suf: 'akuévo +'akue+vo
#  pat=anything; change=ins_deacc; gram=any
#suf: 'akuévoi +'akue+voi
#  pat=anything; change=ins_deacc; gram=any

## 'arã+
#suf: 'arãha +'arã+ha
#  pat=anything; change=ins_deacc; gram=any

## ha+
#hájepi
#háme/hápe...
#háre
#hárentema
#háicha(ma|nte|mante)
#haichaite
#haichami
#haichamínte
#hágui
#hárupi
#hápy
#hávoi, ?havoi
#hahína, etc.
#?haitépe

## va+
# and other postpositions (+icha ...)
#suf: vare +va+re
#  pat=last_acc; change=deaccent; gram=any
#  pat=last_nasv; gram=any
#  pat=acc_notlast; gram=any
#suf: vamante +va+mante
#  pat=last_acc; change=deaccent; gram=any
#  pat=last_nasv; gram=any
#  pat=acc_notlast; gram=any
#suf: vaha +va+ha
#  pat=last_acc; change=deaccent; gram=any
#  pat=last_nasv; gram=any
#  pat=acc_notlast; gram=any
#suf: varã +va+rã
#  pat=anything; change=ins_deacc; gram=any
#suf: vavoi +va+voi
#  pat=anything; change=ins_deacc; gram=any
#suf: vavoínte +va+voi+nte
#  pat=anything; change=ins_deacc; gram=any
#suf: vajepi +va+jepi
#  pat=last_acc; change=deaccent; gram=any
#  pat=last_nasv; gram=any
#  pat=acc_notlast; gram=any
#suf: va'aína +va+hína
#  pat=anything; change=ins_deacc; gram=1s
#suf: vareína +va+hína
#  pat=anything; change=ins_deacc; gram=2s
#suf: vahína +va+hína
#  pat=anything; change=ins_deacc; gram=3
#suf: vañaína +va+hína
#  pat=anything; change=ins_deacc; gram=1pi
#suf: varoína +va+hína
#  pat=anything; change=ins_deacc; gram=1pe
#suf: vapeína +va+hína
#  pat=anything; change=ins_deacc; gram=2p
## and other persons?
#suf: vahikóni +va+hikóni
#  pat=anything; change=ins_deacc; gram=3

## ne+
#suf: nera'e +ne+ra'e
#  pat=last_acc; change=deaccent; gram=any
#  pat=last_nasv; gram=any
#  pat=acc_notlast; gram=any

## ngo+
suf: ngora'e +ngo+ra'e
  pat=last_acc; change=deaccent; gram=any
  pat=last_nasv; gram=any
  pat=acc_notlast; gram=any

## pa+ (interrogative)
suf: para'e +pa+ra'e
  pat=last_acc; change=deaccent; gram=any
  pat=last_nasv; gram=any
  pat=acc_notlast; gram=any

## nte+
suf: nteramo +nte+ramo
  pat=last_acc; change=deaccent; gram=any
  pat=last_nasv; gram=any
  pat=acc_notlast; gram=any
suf: nteva'ekue +nte+va'ekue
  pat=last_acc; change=deaccent; gram=any
  pat=last_nasv; gram=any
  pat=acc_notlast; gram=any
suf: nteva'erã +nte+va'erã
  pat=last_acc; change=deaccent; gram=any
  pat=last_nasv; gram=any
  pat=acc_notlast; gram=any
suf: ntevoi +nte+voi
  pat=last_acc; change=deaccent; gram=any
  pat=last_nasv; gram=any
  pat=acc_notlast; gram=any
suf: ntevoiva'ekue +nte+voi+va'ekue
  pat=last_acc; change=deaccent; gram=any
  pat=last_nasv; gram=any
  pat=acc_notlast; gram=any
suf: ntevoi'akue +nte+voi+'akue
  pat=last_acc; change=deaccent; gram=any
  pat=last_nasv; gram=any
  pat=acc_notlast; gram=any
suf: nteramo'aína +nte+ramo+hína
  pat=anything; change=ins_deacc; gram=1s
suf: nteramoreína +nte+ramo+hína
  pat=anything; change=ins_deacc; gram=2s
suf: nteramohína +nte+ramo+hína
  pat=anything; change=ins_deacc; gram=3
suf: nteramoñaína +nte+ramo+hína
  pat=anything; change=ins_deacc; gram=1pi
suf: nteramoroína +nte+ramo+hína
  pat=anything; change=ins_deacc; gram=1pe
suf: nteramopeína +nte+ramo+hína
  pat=anything; change=ins_deacc; gram=2p
suf: ntemavoi +nte+ma+voi
  pat=anything; change=ins_deacc; gram=any
suf: ntemava'erãha +nte+ma+va'erã+ha
  # or accented, or both?
  pat=last_acc; change=deaccent; gram=any
  pat=last_nasv; gram=any
  pat=acc_notlast; gram=any

## mante+
suf: mante+'arã +mante+'arã
  pat=anything; change=ins_deacc; gram=any
suf: mante+va'erã +mante+va'erã
  pat=anything; change=ins_deacc; gram=any

## niko+
# what about other persons ('aína, etc.)?
suf: nikohína +niko+hína
  pat=anything; change=ins_deacc; gram=3
suf: nikohínakuri +niko+hína+kuri
  pat=anything; change=ins_deacc; gram=3

## ramõ, rõ
suf: ramoguare +ramo+guare
  # both patterns
  pat=anything; change=ins_deacc; gram=any
  pat=last_acc; change=deaccent; gram=any
  pat=last_nasv; gram=any
  pat=acc_notlast; gram=any
suf: rõguare +ramo+guare
  # both patterns
  pat=anything; change=ins_deacc; gram=any
  pat=last_acc; change=deaccent; gram=any
  pat=last_nasv; gram=any
  pat=acc_notlast; gram=any
suf: ramoguáicha +ramo+gua+icha
  pat=anything; change=ins_deacc; gram=any
suf: rõguáicha +ramo+gua+icha
  pat=anything; change=ins_deacc; gram=any
suf: ramomante +ramo+mante
  pat=last_acc; change=deaccent; gram=any
  pat=last_nasv; gram=any
  pat=acc_notlast; gram=any
suf: rõmante +ramo+mante
  pat=last_acc; change=deaccent; gram=any
  pat=last_nasv; gram=any
  pat=acc_notlast; gram=any
suf: ramo'aína +ramo+hína
  pat=anything; change=ins_deacc; gram=1s
suf: ramoreína +ramo+hína
  pat=anything; change=ins_deacc; gram=2s
suf: ramohína +ramo+hína
  pat=anything; change=ins_deacc; gram=3
suf: ramoñaína +ramo+hína
  pat=anything; change=ins_deacc; gram=1pi
suf: ramoroína +ramo+hína
  pat=anything; change=ins_deacc; gram=1pe
suf: ramopeína +ramo+hína
  pat=anything; change=ins_deacc; gram=2p
suf: rõ'aína +ramo+hína
  pat=anything; change=ins_deacc; gram=1s
suf: rõreína +ramo+hína
  pat=anything; change=ins_deacc; gram=2s
suf: rõhína +ramo+hína
  pat=anything; change=ins_deacc; gram=3
suf: rõñaína +ramo+hína
  pat=anything; change=ins_deacc; gram=1pi
suf: rõroína +ramo+hína
  pat=anything; change=ins_deacc; gram=1pe
suf: rõpeína +ramo+hína
  pat=anything; change=ins_deacc; gram=2p
# also +ramoitéva (always separate word?); also rõ+?
#suf: ramoite +ramo+ite
#  pat=anything; change=ins_deacc; gram=any
#suf: ramoiterei +ramo+iterei
#  pat=anything; change=ins_deacc; gram=any
#suf: ramove +ramo+ve
#  pat=anything; change=ins_deacc; gram=any
#suf: ramovéva +ramo+ve+va
#  pat=anything; change=ins_deacc; gram=any
#suf: ramoveva'ekue +ramo+ve+va'ekue
#  pat=anything; change=ins_deacc; gram=any
#suf: ramóme +ramo+pe
#  pat=anything; change=ins_deacc; gram=any
#suf: ramómeraka'e +ramo+pe+raka'e
#  pat=anything; change=ins_deacc; gram=any
#suf: ramóva +ramo+va
#  pat=anything; change=ins_deacc; gram=any
## and other postpositions
#suf: ramóvape +ramo+va+pe
#  pat=anything; change=ins_deacc; gram=any
#suf: ramóvo +ramo+vo
#  pat=anything; change=ins_deacc; gram=any
#suf: ramova'erã +ramo+va'erã
#  pat=anything; change=ins_deacc; gram=any

#### NOUNS
pos: n

### ONE ONLY

## Ñe'ẽteko
suf: nte
  pat=last_acc; change=deaccent; gram=any; aff=+nte
  pat=last_nasv; gram=any; aff=+nte
  pat=acc_notlast; gram=any; aff=+nte
suf: vo
  pat=last_acc; change=deaccent; gram=any; aff=+vo
  pat=last_nasv; gram=any; aff=+vo
  pat=acc_notlast; gram=any; aff=+vo
suf: voi
  pat=last_acc; change=deaccent; gram=any; aff=+voi
  pat=last_nasv; gram=any; aff=+voi
  pat=acc_notlast; gram=any; aff=+voi
suf: ramo
  pat=last_acc; change=deaccent; gram=any; aff=+ramo
  pat=last_nasv; gram=any; aff=+ramo
  pat=acc_notlast; gram=any; aff=+ramo
suf: rõ
  pat=last_acc; change=deaccent; gram=any; aff=+rõ
  pat=last_nasv; gram=any; aff=+rõ
  pat=acc_notlast; gram=any; aff=+rõ
suf: ko
  pat=last_acc; change=deaccent; gram=any; aff=+ko
  pat=last_nasv; gram=any; aff=+ko
  pat=acc_notlast; gram=any; aff=+ko

## Interrogative
suf: pa
  pat=last_acc; change=deaccent; gram=any; aff=+pa
  pat=last_nasv; gram=any; aff=+pa
  pat=acc_notlast; gram=any; aff=+pa
suf: piko
  pat=last_acc; change=deaccent; gram=any; aff=+piko
  pat=last_nasv; gram=any; aff=+piko
  pat=acc_notlast; gram=any; aff=+piko

### TWO OR MORE
