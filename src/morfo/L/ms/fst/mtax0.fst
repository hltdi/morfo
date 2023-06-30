###
### Malay morphotactics
### 0-3 prefixes, 0-2 suffixes possible
###

### morpheme and morphophonemic characters
# R
# N

-> start

### prefixes

start -> pre1      [:]
start -> pre1      <ke:ke->
start -> pre1      <se:se->
start -> pre1      <di:di->
start -> pre1      <pe:pe->
# Ambiguous: peR -> pe | peR
start -> pre1      <peR:pe->
start -> pre1      <peR:peR->
start -> pre1      <beR:beR->
start -> pre1      <teR:teR->
start -> pre1      <meN:meN->
start -> pre1      <peN:peN->
start -> pre1      <juru:juru->

pre1 -> pre2      [:]
pre1 -> pre2      <ke:ke->
pre1 -> pre2      <se:se->
pre1 -> pre2      <di:di->
pre1 -> pre2      <pe:pe->
# Ambiguous: peR -> pe | peR
pre1 -> pre2      <peR:pe->
pre1 -> pre2      <peR:peR->
pre1 -> pre2      <beR:beR->
pre1 -> pre2      <teR:teR->
pre1 -> pre2      <meN:meN->
pre1 -> pre2      <peN:peN->
pre1 -> pre2      <juru:juru->

pre2 -> root      [:]
pre2 -> root      <ke:ke->
pre2 -> root      <se:se->
pre2 -> root      <di:di->
pre2 -> root      <pe:pe->
# Ambiguous: peR -> pe | peR
pre2 -> root      <peR:pe->
pre2 -> root      <peR:peR->
root -> root0  +tv_root_free+        
root -> root0  +tv_root_bound+       
pre2 -> root      <beR:beR->
pre2 -> root      <teR:teR->
pre2 -> root      <meN:meN->
pre2 -> root      <peN:peN->
pre2 -> root      <juru:juru->

# irregular <ajar>

start -> suf1 <belajar+:ber-ajar>       
start -> suf1 <mempelajar+:meN-peR-ajar>  
start -> suf1 <dipelajar+:di-pe-ajar>     
start -> suf1 <pelajar+:pe-ajar>     

### root
#root -> root0  >>root<<
root -> syll    >>syll<<
syll -> syll    >>syll<<
syll -> suf1    [+:]
#root0 -> suf1  [+:]

### suffixes

suf1 -> suf2    [:] 
suf1 -> suf2   <i:-i>
suf1 -> suf2  <an:-an>
suf1 -> suf2  <kan:-kan>

suf2 -> part     [:] 
suf2 -> part    <i:-i>
suf2 -> part   <an:-an>
suf2 -> part   <kan:-kan>

## Suffixed "particles"
part -> end      [:]
part -> end    <nya:-nya>
part -> end    <lah:-lah>
part -> end    <kah:-kah>
part -> end    <mu:-mu>
part -> end    <ku:-ku>

end ->
