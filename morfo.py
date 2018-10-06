#!/usr/bin/env python3

"""
This file is part of morfo, which is part of the PLoGS project.

    <http://homes.soic.indiana.edu/gasser/plogs.html>

    Copyleft 2018.
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

def get_lang(abbrev, guess=True, phon=False, cache='', verbose=False):
    """Return the language with abbreviation abbrev, loading it
    if it's not already loaded."""
    return morfo.get_language(abbrev, cache=cache, phon=phon, guess=guess,
                                  load=True,
                                  verbose=verbose)

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
                                  verbose=verbose)
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
        f = morfo.morpho.semiring.FSSet(fs)
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

def ti_stem():
    casc = morfo.fst.FSTCascade.load("morfo/L/ti/cas/vb_stem.cas", dirname='ti',
                                     seg_units=[['a', 'e', 'E', 'i', 'I', 'o', 'u', '@', 'A',
                                                 'w', 'y', "'", '`', '|', '_'],
                                                {'b': ['b', 'bW'], 'c': ['c', 'cW'],
                                                 'C': ['C', 'CW'], 'd': ['d', 'dW'],
                                                 'f': ['f', 'fW'], 'g': ['g', 'gW'],
                                                 'h': ['h', 'hW'], 'H': ['H', 'HW'],
                                                 'j': ['j', 'jW'], 'k': ['k', 'kW'],
                                                 'K': ['K', 'KW'], 'l': ['l', 'lW'],
                                                 'm': ['m', 'mW'], 'n': ['n', 'nW'],
                                                 'p': ['p', 'pW'], 'P': ['P', 'PW'],
                                                 'N': ['N', 'NW'], 'q': ['q', 'qW'],
                                                 'Q': ['Q', 'QW'], 'r': ['r', 'rW'],
                                                 's': ['s', 'sW'], 'S': ['S', 'SW'],
                                                 't': ['t', 'tW'], 'T': ['T', 'TW'],
                                                 'v': ['v', 'vW'], 'x': ['x', 'xW'],
                                                 'z': ['z', 'zW'], 'Z': ['Z', 'ZW']}])
    return casc.compose(relabel=False)

def main():
    pass

if __name__ == "__main__": main()
