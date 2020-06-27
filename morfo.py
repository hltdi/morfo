#!/usr/bin/env python3

"""
This file is part of morfo, which is part of the PLoGS project.

    <http://homes.soic.indiana.edu/gasser/plogs.html>

    Copyleft 2018, 2019, 2020.
    PLoGS and Michael Gasser <gasser@indiana.edu>.

    morfo is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    morfo is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with morfo.  If not, see <http://www.gnu.org/licenses/>.

Author: Michael Gasser <gasser@indiana.edu>
""" 
import morfo

def get_lang(abbrev, segment=False, guess=True, phon=False, cache='', verbose=False):
    """Return the language with abbreviation abbrev, loading it
    if it's not already loaded."""
    return morfo.get_language(abbrev, cache=cache, phon=phon, guess=guess, load=True,
                              segment=segment, verbose=verbose)

def get_pos(abbrev, pos, phon=False, segment=False, load_morph=False,
            guess=True, verbose=False):
    """Just a handy function for working with the POS objects when re-compiling
    and debugging FSTs.
    @param abbrev: abbreviation for a language, for example, 'am'
    @type  abbrev: string
    @param pos:    part-of-speech for the FST, for example, 'v'
    @type  pos:    string
    @param phon:   whether the FST is for phonology
    @type  phon:   boolean
    @param segment: whether the FST is for segmentation
    @type  segment: boolean
    @param verbose: whether to print out various messages
    @type  verbose: boolean
    @return:       POS object for the the language and POS
    @rtype:        instance of the POSMorphology class

    """
    morfo.load_lang(abbrev, segment=segment, phon=phon, load_morph=load_morph,
                 guess=guess, verbose=verbose)
    lang = morfo.get_language(abbrev, phon=phon, segment=segment, load=load_morph,
                              load_morph=load_morph, verbose=verbose)
    if lang:
        return lang.morphology[pos]

def get_cascade(abbrev, pos, guess=False, gen=False, phon=False, segment=False, verbose=False):
    pos = get_pos(abbrev, pos, phon=phon, segment=segment, load_morph=False, verbose=verbose)
    pos.load_fst(True, guess=guess, create_fst=False,
                 phon=phon, generate=gen, invert=gen, segment=segment, verbose=verbose)
    return pos.casc

def recompile(abbrev, pos, gen=False, phon=False, segment=False, guess=False,
              backwards=False, split_index=0, verbose=True):
    """Create a new composed cascade for a given language (abbrev) and part-of-speech (pos),
    returning the morphology POS object for that POS.
    Note 1: this can take a very long time for some languages.
    Note 2: the resulting FST is not saved (written to a file). To do this, use the method
    save_fst().
    """
    pos_morph = get_pos(abbrev, pos, phon=phon, segment=segment,
                        load_morph=False, verbose=verbose)
    fst = pos_morph.load_fst(True, segment=segment, generate=gen, invert=gen, guess=guess,
                             compose_backwards=backwards, split_index=split_index,
                             phon=phon, verbose=verbose)
    if not fst and gen == True:
        print('Generation FST not found')
        # Load analysis FST>
        pos_morph.load_fst(True, verbose=True)
        # ... and invert it for generation FST
        pos_morph.load_fst(generate=True, invert=True, gen=True,
                           guess=guess, verbose=verbose)
    return pos_morph

### Simple FSTs and cascades (in test directory)

def make_casc(name):
    import os
    filename = os.path.join("morfo/L/test/cas/", name + '.cas')
    with open(filename, encoding='utf8') as infile:
        castext = infile.read()
        casc = morfo.fst.FSTCascade.parse("simple", castext,
                                          seg_units=['a', 'b', 'c', 'd', 'e', 'f'])
    fst = casc.compose(backwards=False, relabel=True)
    return fst

### Debugging functions

def get_feats(fs, feats):
    """Print values for features feats within feature structure fs."""
    values = []
    for feat in feats:
        values.append("{}={}".format(feat, fs.get(feat)))
    return ",".join(values)

def casc_anal(casc, string, start_i, end_i=0, trace=0):
    seg_units = casc.seg_units
    s = string
    if end_i:
        for index in range(start_i, end_i):
            res = casc[index].transduce(s, seg_units=seg_units, timeout=10, trace=trace)
            if not res:
                print('Analysis failed at {}'.format(index))
                return
            i = 0
            if len(res) > 1:
                print('FST {}, analyses: {}'.format(index, [a[0] for a in res]))
                x = input("Index of analysis (or quit)? ")
                if not x.isdigit():
                    return
                i = int(x)
            s = res[i][0]
            print(s)
    else:
        return casc[start_i].transduce(s, seg_units=seg_units, timeout=10)

def casc_gen(casc, string, fs, start_i, end_i=0, trace=0):
    seg_units = casc.seg_units
    s = string
    if not isinstance(fs, morfo.fst.semiring.FSSet):
        f = morfo.morfo.semiring.FSSet(fs)
    else:
        f = fs
    if end_i:
        for index in range(start_i, end_i, -1):
            res = casc[index].inverted().transduce(s, f, seg_units=seg_units,
                                                   timeout=10, trace=trace)
            if not res:
                print('Generation failed at {}'.format(index))
                return
            i = 0
            if len(res) > 1:
                print('FST {}, output: {}'.format(index, res))
                x = input("Index to select next (or quit)? ")
                if not x.isdigit():
                    return
                i = int(x)
            s = res[i][0]
            f = res[i][1]
            print(s)
    else:
        return casc[start_i].inverted().transduce(s, f, seg_units=seg_units, timeout=10)

# Analyzing Guarani word types
def anal_grn(start=0, end=45000):
    morfo.anal_word_counts("grn", "../LingData/Gn/words5.txt", ["tm", "ps", "ns", "po", "no"], write=True)

def proc_grn_feats(pos=None, feat=None):
    """Count different feature values for Guarani word tokens."""
    result = {}
    with open("../LingData/Gn/words5.txt.anl", encoding='utf8') as inf:
        for line in inf:
            item, count = line.split()
            if ';' in item:
                # Otherwise no real analysis, so ignore the line
                count = int(count)
                word, anals = item.split(';')
                anals = anals.split('|')
                nanals = len(anals)
                count1 = count / nanals
                for anal in anals:
                    root_feats = anal.split(':')
                    if len(root_feats) == 1:
                        # No features
                        continue
                    root, feats = anal.split(':')
                    if pos and '_' + pos not in root:
                        continue
                    if feats == '[]':
                        continue
                    feats = morfo.fs.FeatStruct(feats)
                    feats.freeze()
                    if feat:
                        if feat not in feats:
                            continue
                        else:
                            feats = feats[feat]
                    # Update the counts
                    if feats not in result:
                        result[feats] = 0
                    c = result[feats]
                    c = round(c + count1, 2)
                    result[feats] = c
#    result = list(result.items())
#    result.sort(key=lambda x: x[1], reverse=True)
    return result

# Splitting off Grn derived nouns

GNACC = "áéíóúýãẽĩõũỹ"

def split_grn_nouns():
    old = []
    new = []
    with open("morfo/L/grn/lex/n_raizG.lex", encoding='utf8') as file:
        for line in file:
            line = line.strip()
            if ' ' in line:
                old.append(line)
            elif len(line) > 2 and line[-3] in GNACC and line.endswith('va'):
                new.append(line)
            else:
                old.append(line)
    return old, new

def proc_grn_roots(pos=None, features=None):
    """Count different feature-value combinations for each Guarani root that appears
    in word token list."""
    result = {}
    with open("../LingData/Gn/words5.txt.anl", encoding='utf8') as inf:
        for line in inf:
            item, count = line.split()
            if ';' in item:
                # Otherwise no real analysis, so ignore the line
                count = int(count)
                word, anals = item.split(';')
                anals = anals.split('|')
                nanals = len(anals)
                count1 = count / nanals
#                if count1 < 0.2:
#                    print("count1: {}, item: {}, count: {}, n: {}".format(count1, item, count, nanals))
                for anal in anals:
                    root_feats = anal.split(':')
                    if len(root_feats) == 1:
                        # No features
                        if features:
                            continue
                        root = root_feats[0]
                        if pos and '_' + pos not in root:
                            continue
                        if root not in result:
                            result[root] = {}
                        root_feats = result[root]
                        if None not in root_feats:
                            root_feats[None] = 0
                        root_feats[None] += count1
                        continue
                    root, feats = anal.split(':')
                    if pos and '_' + pos not in root:
                        continue
                    if '*' in root:
                        root = root.replace('*', word)
                    root = root.split('_')[0]
                    if root not in result:
                        result[root] = {}
                    root_feats = result[root]
                    if feats == '[]':
                        feats = None
                        if features:
                            continue
                    else:
                        feats = morfo.fs.FeatStruct(feats)
                        feats.freeze()
                        if features:
                            fv = [(feat, feats.get(feat, 'out')) for feat in features]
                            for feat, value in fv:
                                if value != 'out':
                                    if feat not in root_feats:
                                        root_feats[feat] = {}
                                    if value not in root_feats[feat]:
                                        root_feats[feat][value] = 0
                                    rfv = root_feats[feat][value]
                                    rfv = round(rfv + count1, 2)
                                    root_feats[feat][value] = rfv
    todel = []
    for key in result:
        if not result[key]:
            todel.append(key)
    for key in todel:
        del result[key]
##    for item, counts in result.items():
##        for feat, vcounts in counts.items():
##            vcounts = list(vcounts.items())
##            vcounts.sort(key=lambda x: x[1], reverse=True)
##            counts[feat] = vcounts
##    if write:
##        result = list(result.items())
##        result.sort(key=lambda x: x[0])
##        with open(write, 'w', encoding='utf8') as file:
##            for item, counts in result:
##                if counts:
##                    item = item.split('_')[0]
##                    print("{} :: {}".format(item, counts), file=file)
    return result

def segment(fst, form, printout=True):
    seg = fst.anal(form, segment=True)
    if seg:
        if len(seg) > 20:
            seg = "TOO MANY SEGMENTATIONS"
        else:
            seg = ', '.join(["{}:{}".format(x[0], x[1].get('v')) for x in seg])
    else:
        seg = "FAILED"
    if printout:
        print("{} -- {}".format(form, seg))
    else:
        return form, seg

def segall(fst, forms):
    for form in forms:
        segment(fst, form, True)

def analyze(fst, form, printout=True):
    a = fst.anal(form)
    if a:
        if len(a) > 20:
            a = "TOO MANY ANALYSES"
        else:
            a = ', '.join(["{}:{};{};{}".format(x[0], x[1].get('v'), x[1].get('as'), x[1].get('vc')) for x in a])
    else:
        a = "FAILED"
    if printout:
        print("{} -- {}".format(form, a))
    else:
        return form, a

def analall(fst, forms):
    for form in forms:
        analyze(fst, form, True)

def main():
    pass

if __name__ == "__main__": main()
