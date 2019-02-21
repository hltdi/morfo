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
--------------------------------------------------------------------

Author: Michael Gasser <gasser@indiana.edu>

Language objects, with support mainly for morphology (separate
Morphology objects defined in morphology.py).

"""

import os, sys, re, copy, itertools

LANGUAGE_DIR = os.path.join(os.path.dirname(__file__), 'L')

from .morphology import *
# FUTURE
# from .anal import *
# from .trans import *

## Regex for extracting root from segmentation string
SEG_ROOT_RE = re.compile(r".*{(.+)}.*")

## Regexes for parsing language data
# Language name
LG_NAME_RE = re.compile(r'\s*n.*?:\s*(.*)')
# Interface language abbreviation
# l...: 
IF_RE = re.compile(r'\s*if*?:\s*(.*)')
## preprocessing function
#PREPROC_RE = re.compile(r'\s*pre*?:\s*(.*)')
# Segments (characters)
# seg...: 
SEG_RE = re.compile(r'\s*seg.*?:\s*(.*)')
# Accent dictionary
# accent:
ACC_RE = re.compile(r'\s*accent:\s*(.*)')
# Deaccent dictionary
# deaccent:
DEACC_RE = re.compile(r'\s*deaccent:\s*(.*)')
# Punctuation
# pun...: 
PUNC_RE = re.compile(r'\s*pun.*?:\s*(.*)')
# Part of speech categories
# pos:
# pos: v verbo
POS_RE = re.compile(r'\s*pos:\s*(.*)\s+(.*)')
#POS_RE = re.compile(r'\s*pos:\s*(.*)')
# Feature abbreviations
# ab...:
ABBREV_RE = re.compile(r'\s*ab.*?:\s*(.*)')
# Term translations
# tr...:
TRANS_RE = re.compile(r'\s*tr.*?:\s*(.*)')
# Beginning of feature-value list
FEATS_RE = re.compile(r'\s*feat.*?:\s*(.*)')
# Feature-value pair
FV_RE = re.compile(r'\s*(.*?)\s*=\s*(.*)')
# FV combinations, could be preceded by ! (= priority)
FVS_RE = re.compile(r'([!]*)\s*([^!]*)')
# Feature group: {f1, f2,...} (v1, v2, ...): groupname = groupvalue
FEAT_GROUP_RE = re.compile(r"\{(.+)\}\s*\((.+)\):\s*(.+)\s+([+=])\s+(.+)")
# Abbrev, with prefixes, and full name
ABBREV_NAME_RE = re.compile(r'([*%]*?)([^*%()]*?)\s*\((.*)\)\s*(\[.*\])?')
NAME_RE = re.compile(r'([*%]*)([^*%\[\]]*)\s*(\[.*\])?')
# Feature to be recorded in anal output; new 2015.03.10
# xf: g gender
# xf~: VOS voseo
# As of 2018.9.21, this may be no longer necessary
EXPL_FEAT_RE = re.compile(r'\s*xf(.*):\s*(.*)\s*=\s*(.*)')
# Preprocessing: replace characters in first list with last char
# clean: â, ä = ã
CLEAN_RE = re.compile(r'\s*cle.*?:\s*(.*)\s*=\s*(.*)')

## Regex for checking for non-ascii characters
ASCII_RE = re.compile(r'[a-zA-Z]')

class Language:
    '''A single Language, currently only handling morphology.'''

    T = TDict()

    IF = {'spa': {},
          'eng': {}}

    def __init__(self, label='', abbrev='', backup='',
                 preproc=None, postproc=None, read_cache=True,
                 # There may be a further function for post-processing
                 postpostproc=None,
                 seg_units=None,
                 # list of grammatical features to be combined with roots for statistics,
                 # e.g., voice and aspect for Amharic verb roots (assume there's only
                 # list)
                 stat_root_feats=None,
                 # list of lists of grammatical features for statistics, e.g.,
                 # [poss, expl] for Amharic (whether it's explicitly possessive)
                 stat_feats=None,
                 citation_separate=True):
#                 msgs=None, trans=None):
        """
        Set some basic language-specific attributes.

        @param preproc            Whether to pre-process input to analysis, for example,
                                  to convert non-roman to roman characters
        @param postproc           Whether to post-process output of generation, for
                                  example, to convert roman to non-roman characters
        @param seg_units          Segmentation units (graphemes)
        @param citation_separate  Whether citation form of words is separate from roots
#        @param msgs               Messages in the languages (or some other)
#        @param trans              Translations of terms from english to this language
        """
        self.label = label
        self.abbrev = abbrev or label[:3]
        # Backup language for term translation, etc.
        self.backup = backup
        self.morphology = None
        self.preproc = preproc
        self.postproc = postproc
        self.postpostproc = postpostproc
        self.seg_units = seg_units or []
        self.stat_root_feats = stat_root_feats or []
        self.stat_feats = stat_feats or []
        # If any, dictionaries associating characters with their "accented" or
        # "unaccented" forms
        self.accent = None
        self.deaccent = None
        self.citation_separate = citation_separate
#        self.msgs = msgs or {}
#        self.trans = trans or {}
        self.directory = self.get_dir()
        self.tlanguages = [abbrev]
        # Interface language
        self.if_language = None
        if self.backup:
            self.tlanguages.append(self.backup)
        # Whether the language data and FSTs have been loaded
        self.load_attempted = False
        self.cached = {}
        # Cached entries read in when language is loaded
        if read_cache:
            self.read_cache()
        # New analyses since language loaded
        # each entry a wordform and list of (root, FS) analyses
        self.new_anals = {}
        # Data for web app
        self.webdata = []
        self.webdict = {}

    def __str__(self):
        return self.label or self.abbrev

    def get_if_abbrev(self):
        return self.if_language or self.abbrev

    def get_if_dict(self):
        if_abbrev = self.get_if_abbrev()
        return Language.IF[if_abbrev]

    def get_dir(self):
        """Where data for this language is kept."""
        return os.path.join(LANGUAGE_DIR, self.abbrev)

    def get_data_file(self):
        """Data file for language."""
        return os.path.join(self.get_dir(), self.abbrev + '.lg')

    def get_cache_dir(self):
        """File with cached analyses."""
        return os.path.join(self.get_dir(), 'cache')

    def get_cache_file(self, segment=False):
        d = self.get_cache_dir()
        if segment:
            name = 'seg'
        else:
            name = 'anal'
        return os.path.join(d, name + '.cch')

    def add_new_anal(self, word, anals):
        self.new_anals[word] = anals

    def write_cache(self, name=''):
        """Write a dictionary of cached entries to a cache file."""
        if self.new_anals:
            # Only attempt to cache analyses if there are new ones.
            file = self.get_cache_file(name=name)
            with open(file, 'a', encoding='utf8') as out:
                for word, analyses in self.new_anals.items():
                    # analyses is a list of root, fs pairs
                    if len(analyses) == 1 and analyses[0][0] == word and not analyses[0][1]:
                        # The word is unanalyzed
                        print("{}".format(word), file=out)
                    else:
                        anals = ["{}:{}".format(r, f.__repr__() if f else '') for r, f in analyses]
                        anals = ';'.join(anals)
                        print("{} || {}".format(word, anals), file=out)
        # Empty new_anals in case we want to add things later
        self.new_anals.clear()

    def read_cache(self, segment=False):
        """Read cached entries into self.cached from a file."""
        file = self.get_cache_file(segment=segment)
        try:
            with open(file, encoding='utf8') as f:
                print("Reading cached words")
                for line in f:
                    if '||' not in line:
                        self.cached[line.strip()] = []
                        continue
                    split_line = line.strip().split(" || ")
                    word, analyses = split_line
                    analyses = analyses.split(';')
                    analyses = [a.split(':') for a in analyses]
                    analyses = [(r, FeatStruct(a, freeze=True) if a else None) for r, a in analyses]
                    self.cached[word] = analyses
        except IOError:
            print('No such cache file as {}'.format(file))

    def get_cached_anal(self, word):
        """Returns cached analyses for word if any."""
        if word in self.cached:
            entry = self.cached[word]
            if not entry:
                return [(word, None)]
            else:
                return entry
        if word in self.new_anals:
            entry = self.new_anals[word]
            if not entry:
                return [(word, None)]
            else:
                return entry
        return False

    @staticmethod
    def root_from_seg(segmentation):
        """Extract the root from a segmentation expression."""
        r = SEG_ROOT_RE.match(segmentation)
        if r:
            return r.group(1).split("+")[0]
        return ''

    @staticmethod
    def add_IF(name, entries):
        """Add another entry to the interface dictionaries (IF)."""
        for lg_abbrev, text in entries:
            if lg_abbrev not in Language.IF:
                print("Warning: {} not in IF dictionary".format(lg_abbrev))
                return
            Language.IF[lg_abbrev][name] = text

    @staticmethod
    def make(name, abbrev, load_morph=False,
             segment=False, phon=False,
             guess=True, poss=None, verbose=False):
        """Create a language using data in the language data file."""
        lang = Language(abbrev=abbrev)
        # Load data from language file
        lang.load_data(load_morph=load_morph, segment=segment, phon=phon,
                       guess=guess, poss=poss, verbose=verbose)
#        if load_morph:
#            lang.load_morpho(verbose=verbose)
        return lang

    def load_data(self, load_morph=False, segment=False, phon=False, guess=True,
                  poss=None, verbose=False):
        if self.load_attempted:
            return
        self.load_attempted = True
        filename = self.get_data_file()
        print("Looking for language data file at {}".format(filename))
        if not os.path.exists(filename):
            print(Language.T.tformat('No language data file for {}', [self], self.tlanguages))
            pass
        else:
            if verbose:
                print(Language.T.tformat('Loading language data from {}', [filename], self.tlanguages))
            with open(filename, encoding='utf-8') as stream:
                data = stream.read()
                self.parse(data, poss=poss, verbose=verbose)
        if load_morph:
            if not self.load_morpho(segment=segment, ortho=True, phon=phon, guess=guess, verbose=verbose):
                # There is no FST of the desired type
                return False
        # Create a default FS for each POS
        for posmorph in self.morphology.values():
            if posmorph.defaultFS:
                if isinstance(posmorph.defaultFS, str):
                    posmorph.defaultFS = FeatStruct(posmorph.defaultFS)
            else:
                posmorph.defaultFS = posmorph.make_default_fs()
        return True

    def parse(self, data, poss=None, verbose=False):

        """Read in language data from a file."""
        if verbose:
            print('Parsing data for', self)

        lines = data.split('\n')[::-1]

        seg = []
        punc = []
        abbrev = {}
        fv_abbrev = {}
        trans = {}
        fv_dependencies = {}
        fv_priorities = {}
        fullpos = {}

        excl = {}
        feats = {}
        lex_feats = {}
        true_explicit = {}
        explicit = {}

        feature_groups = {}

        chars = ''

        current = None

#        current_pos = ''
        current_feats = []
        current_lex_feats = []
        current_excl = []
        current_abbrev = {}
        current_fv_abbrev = []
        current_fv_priority = []

        complex_feat = False
        current_feat = None
        current_value_string = ''
        complex_fvs = []

        current_explicit = []
        current_true_explicit = []

        current_feature_groups = {}

        while lines:

            line = lines.pop().split('#')[0].strip() # strip comments

            # Ignore empty lines
            if not line: continue

            # Beginning of segmentation units
            m = SEG_RE.match(line)
            if m:
                current = 'seg'
                seg = m.group(1).split()
                continue

            m = ACC_RE.match(line)
            if m:
                acc = m.group(1).split(',')
                self.accent = {}
                for chars in acc:
                    u, a = chars.split(':')
                    self.accent[u.strip()] = a.strip()
                continue

            m = DEACC_RE.match(line)
            if m:
                deacc = m.group(1).split(',')
                self.deaccent = {}
                for chars in deacc:
                    a, u = chars.split(':')
                    self.deaccent[a.strip()] = u.strip()
                continue

            m = LG_NAME_RE.match(line)
            if m:
                label = m.group(1).strip()
                self.label = label
                continue

            m = IF_RE.match(line)
            if m:
                lang = m.group(1).strip()
                self.if_language = lang
#                self.tlanguages.append(lang)
                continue

            m = PUNC_RE.match(line)
            if m:
                current = 'punc'
                punc = m.group(1).split()
                continue

            m = TRANS_RE.match(line)
            if m:
                current = 'trans'
                w_g = m.group(1).split()
                if '=' in w_g:
                    w, g = w_g.split('=')
                    # Add to the global TDict
                    Language.T.add(w.strip(), g.strip(), self.abbrev)
#                    self.trans[w.strip()] = g.strip()
                continue

            m = CLEAN_RE.match(line)
            if m:
                # Ignore in morfo
                continue

            m = FEATS_RE.match(line)
            if m:
                current = 'feats'
                continue

            if current == 'feats':
                m = POS_RE.match(line)
                if m:
                    pos, fullp = m.groups()
                    pos = pos.strip()
                    fullp = fullp.strip()
#                    self.pos.append(pos)
                    # Differs in ParaMorfo below
                    # Start a set of features for a new part-of-speech category
#                    pos = m.group(1).strip()
                    current_feats = []
                    current_lex_feats = []
                    current_excl = []
                    current_abbrev = {}
                    current_fv_abbrev = []
                    current_fv_dependencies = {}
                    current_fv_priority = []
                    current_explicit = []
                    current_true_explicit = []
                    current_feature_groups = {}
                    lex_feats[pos] = current_lex_feats
                    feats[pos] = current_feats
                    excl[pos] = current_excl
                    abbrev[pos] = current_abbrev
                    fv_abbrev[pos] = current_fv_abbrev
                    fv_dependencies[pos] = current_fv_dependencies
                    fv_priorities[pos] = current_fv_priority
                    explicit[pos] = current_explicit
                    true_explicit[pos] = current_true_explicit
                    fullpos[pos] = fullp
                    feature_groups[pos] = current_feature_groups
                    continue

                m = ABBREV_RE.match(line)
                if m:
#                    current = 'abbrev'
                    abb_sig = m.group(1).strip()
                    if '=' in abb_sig:
                        abb, sig = abb_sig.split('=')
                        current_abbrev[abb.strip()] = sig.strip()
                    continue

                m = EXPL_FEAT_RE.match(line)
                # Feature to include in pretty output; ignore in morfo
                if m:
                    opt, fshort, flong = m.groups()
                    fshort = fshort.strip()
                    opt = opt.strip()
                    current_abbrev[fshort] = flong.strip()
#                    current_explicit.append(fshort)
#                    if opt and opt == '~':
#                        current_true_explicit.append(fshort)
                    continue

                m = FEAT_GROUP_RE.match(line)
                if m:
                    groupfeats, groupvalues, groupname, oper, groupvalue = m.groups()
                    groupfeats = tuple([f.strip() for f in groupfeats.split(',')])
                    groupvalues = [v.strip() for v in groupvalues.split(',')]
                    for i, v in enumerate(groupvalues):
                        if v.isdigit():
                            groupvalues[i] = int(v)
                        elif v == "False":
                            groupvalues[i] = False
                        elif v == "True":
                            groupvalues[i] = True
                    groupvalues = tuple(groupvalues)
                    groupname = groupname.strip()
#                    print("groupfeats {}, groupname {}, gvalues {}, add {}".format(groupfeats, groupname, groupvalues, oper))
                    if groupfeats in current_feature_groups:
                        current_feature_groups[groupfeats].append((groupvalues, groupname, groupvalue, oper=='='))
                    else:
                        current_feature_groups[groupfeats] = [(groupvalues, groupname, groupvalue, oper=='=')]
                    if groupname not in current_explicit:
                        current_explicit.append(groupname)
#                    print("feature groups {}".format(current_feature_groups))
                    continue

                m = FV_RE.match(line)
                if m:
                    # A feature and value specification
                    feat, val = m.groups()
                    if '+' in feat or '-' in feat:
                        # Expansion for a set of boolean feature values
                        # See if there's a ! (=priority) prefix
                        m2 = FVS_RE.match(feat)
                        priority, fvs = m2.groups()
                        # An abbreviation for one or more boolean features with values
                        fvs = fvs.split(',')
                        fvs = [s.strip() for s in fvs]
                        fvs = [s.split('=') if '=' in s else [s[1:], (True if s[0] == '+' else False)] for s in fvs]
                        current_fv_abbrev.append((fvs, val))
                        if priority:
                            current_fv_priority.append(fvs)
                    elif '=' in val:
                        # Complex feature (with nesting)
                        complex_feat = self.proc_feat_string(feat, current_abbrev, current_excl, current_lex_feats,
                                                             current_fv_dependencies,
                                                             current_explicit, current_true_explicit, top=True)
                        vals = val.split(';')
                        for fv2 in vals:
                            fv2 = fv2.strip()
                            if fv2:
                                m2 = FV_RE.match(fv2)
                                if m2:
                                    feat2, val2 = m2.groups()
                                    f = self.proc_feat_string(feat2, current_abbrev, current_excl, current_lex_feats,
                                                              current_fv_dependencies,
                                                              current_explicit, current_true_explicit, top=False)
                                    v = self.proc_value_string(val2, f, current_abbrev, current_excl,
                                                               current_fv_dependencies, current_fv_abbrev)
                                    complex_fvs.append((f, v))
                        if len(vals) == 1:
                            current_feats.append((complex_feat, complex_fvs))
                            complex_feat = None
                            complex_fvs = []
                    else:
                        fvs = line.split(';')
                        if len(fvs) > 1:
                            # More than one feature-value pair (or continuation)
                            if not complex_feat:
                                complex_feat = current_feat
                            for fv2 in fvs:
                                fv2 = fv2.strip()
                                if fv2:
                                    m2 = FV_RE.match(fv2)
                                    if m2:
                                        # A single feature-value pair
                                        feat2, val2 = m2.groups()
                                        f = self.proc_feat_string(feat2, current_abbrev, current_excl, current_lex_feats,
                                                                  current_fv_dependencies,
                                                                  current_explicit, current_true_explicit, top=False)
                                        v = self.proc_value_string(val2, f, current_abbrev, current_excl,
                                                                   current_fv_dependencies, current_fv_abbrev)
                                        complex_fvs.append((f, v))
                        elif complex_feat:
                            # A single feature-value pair
                            f = self.proc_feat_string(feat, current_abbrev, current_excl, current_lex_feats,
                                                      current_fv_dependencies,
                                                      current_explicit, current_true_explicit, top=False)
                            v = self.proc_value_string(val, f, current_abbrev, current_excl,
                                                       current_fv_dependencies, current_fv_abbrev)
                            complex_fvs.append((f, v))
                            current_feats.append((complex_feat, complex_fvs))
                            complex_feat = None
                            complex_fvs = []
                        else:
                            # Not a complex feature
                            current_feat = self.proc_feat_string(feat, current_abbrev, current_excl, current_lex_feats,
                                                                 current_fv_dependencies,
                                                                 current_explicit, current_true_explicit, top=True)
                            current_value_string = ''
                            val = val.strip()
                            if val:
                                # The value is on this line
                                # Split the value by |
                                vals = val.split('|')
                                vals_end = vals[-1].strip()
                                if not vals_end:
                                    # The line ends with | so the value continues
                                    current_value_string = val
                                else:
                                    v = self.proc_value_string(val, current_feat, current_abbrev, current_excl,
                                                               current_fv_dependencies, current_fv_abbrev)
                                    current_feats.append((current_feat, v))

                else:
                    # Just a value
                    val = line.strip()
                    current_value_string += val
                    # Split the value by | to see if it continues
                    vals = val.split('|')
                    if vals[-1].strip():
                        v = self.proc_value_string(current_value_string, current_feat, current_abbrev, current_excl,
                                                   current_fv_dependencies, current_fv_abbrev)
                        current_feats.append((current_feat, v))
                        current_value_string = ''

            elif current == 'seg':
                seg.extend(line.strip().split())

            elif current == 'punc':
                punc.extend(line.strip().split())

            elif current == 'pos':
                pos.extend(line.strip().split())

            elif current == 'trans':
                wd, gls = line.strip().split('=')
                # Add to the global TDict
                Language.T.add(wd.strip(), gls.strip(), self.abbrev)
#                self.trans[wd] = gls.strip()

            else:
                raise ValueError("bad line: {}".format(line))

        if punc:
            # Make punc list into a string
            punc = ''.join(punc)

        if seg:
            # Make a bracketed string of character ranges and other characters
            # to use for re
            chars = ''.join(set(''.join(seg)))
            chars = self.make_char_string(chars)
            # Make the seg_units list, [chars, char_dict], expected for transduction,
            # composition, etc.
            self.seg_units = self.make_seg_units(seg)

        if feats and not self.morphology:
            pos_args = []
#            print("feats {}".format(feats))
            for pos in feats:
                if not poss or pos in poss:
                    # Make feature_groups into a list, sorted by length of feature matches
                    fgroups = list(feature_groups[pos].items())
                    fgroups.sort(key=lambda x: -len(x[0]))
                    pos_args.append((pos, feats[pos], lex_feats[pos], excl[pos], abbrev[pos],
                                     fv_abbrev[pos], fv_dependencies[pos], fv_priorities[pos],
                                     fgroups, fullpos[pos],
                                     explicit[pos], true_explicit[pos]))
            morph = Morphology(pos_morphs=pos_args,
                               punctuation=punc, characters=chars)
            self.set_morphology(morph)

    def proc_feat_string(self, feat, abbrev_dict, excl_values, lex_feats, fv_dependencies,
                         explicit, true_explicit, top=True):
        prefix = ''
        depend = None
        m = ABBREV_NAME_RE.match(feat)

        if m:
            prefix, feat, name, depend = m.groups()
            abbrev_dict[feat] = name
        else:
            m = NAME_RE.match(feat)
            prefix, feat, depend = m.groups()

#        print('Prefix {}, feat {}, depend {}'.format(prefix, feat, depend))

        if not '*' in prefix and not '%' in prefix:
            if top:
                explicit.append(feat)
        else:
            # * means that the feature's values are not reported in analysis output
            if '*' in prefix:
                excl_values.append(feat)
            # % means that the feature is lexical
            if '%' in prefix:
                lex_feats.append(feat)

        if depend:
            # Feature and value that this feature value depends on
            # Get rid of the []
            depend = depend[1:-1]
            # Can be a comma-separated list of features
            depends = depend.split(',')
            for index, dep in enumerate(depends):
                dep_fvs = [fvs.strip() for fvs in dep.split()]
                if dep_fvs[-1] == 'False':
                    dep_fvs[-1] = False
                elif dep_fvs[-1] == 'True':
                    dep_fvs[-1] = True
                elif dep_fvs[-1] == 'None':
                    dep_fvs[-1] = None
                depends[index] = dep_fvs
            fv_dependencies[feat] = depends

        return feat

    def proc_value_string(self, value_string, feat, abbrev_dict, excl_values, fv_dependencies,
                          fv_abbrev):
        '''value_string is a string containing values separated by |.'''
#        print("Processing feat {}; value string {}, fv abbrev {}".format(feat, value_string, fv_abbrev))
        values = [v.strip() for v in value_string.split('|')]
        res = []
        prefix = ''
        for value in values:
            name = ''
            if not value:
                continue
            if value == '+-':
                res.extend([True, False])
            else:
                m = ABBREV_NAME_RE.match(value)
                if m:
                    prefix, value, name, depend = m.groups()
                else:
                    m = NAME_RE.match(value)
                    prefix, value, depend = m.groups()

                value = value.strip()

                if value == 'False':
                    value = False
                elif value == 'True':
                    value = True
                elif value == 'None':
                    value = None
                elif value == '...':
#                    print('prefix {}, value {}, depend {}'.format(prefix, value, depend))
                    value = FeatStruct('[]')
                elif value.isdigit():
                    value = int(value)

                # Value abbrev
                if name:
                    fv_abbrev.append(([[feat, value]], name))
#                    abbrev_dict[value] = name

                if '*' in prefix:
                    excl_values.append((feat, value))

                if depend:
                    # Feature and value that this feature value depends on
                    depend = depend[1:-1]
                    dep_fvs = [fvs.strip() for fvs in depend.split()]
                    if dep_fvs[-1] == 'False':
                        dep_fvs[-1] = False
                    elif dep_fvs[-1] == 'True':
                        dep_fvs[-1] = True
                    elif dep_fvs[-1] == 'None':
                        dep_fvs[-1] = None
                    elif dep_fvs[-1] == '...':
#                        print('prefix {}, value {}, depend {}'.format(prefix, value, depend))
                        dep_fvs[-1] = FeatStruct('[]')
                    fv_dependencies[(feat, value)] = dep_fvs

                res.append(value)
        return tuple(res)

    def make_char_string(self, chars):
        non_ascii = []
        for char in chars:
            if not ASCII_RE.match(char):
                non_ascii.append(char)
        non_ascii.sort()
        non_ascii_s = ''.join(non_ascii)
        return r'[a-zA-Z' + non_ascii_s + r']'

    def make_seg_units(self, segs):
        """Convert a list of segments to a seg_units list + dict."""
        singletons = []
        dct = {}
        for seg in segs:
            c0 = seg[0]
            if c0 in dct:
                dct[c0].append(seg)
            else:
                dct[c0] = [seg]
        for c0, segs in dct.items():
            if len(segs) == 1 and len(segs[0]) == 1:
                singletons.append(c0)
        for seg in singletons:
            del dct[seg]
        singletons.sort()
        return [singletons, dct]

#    def get_trans(self, word):
#        return self.trans.get(word, word)

    def preprocess(self, form):
        '''Preprocess a form.'''
        if self.preproc:
            return self.preproc(form)
        return form

    def postprocess(self, form):
        '''Postprocess a form.'''
        if self.postproc:
            return self.postproc(form)
        return form

    def postpostprocess(self, form):
        '''Postprocess a form that has already been postprocessed.'''
        if self.postpostproc:
            return self.postpostproc(form)
        return form

    def preprocess_file(self, filein, fileout):
        '''Preprocess forms in filein, writing them to fileout.'''
#        fin = codecs.open(filein, 'r', 'utf-8')
#        fout = codecs.open(fileout, 'w', 'utf-8')
        fin = open(filein, 'r', encoding='utf-8')
        fout = open(fileout, 'w', encoding='utf-8')
        for line in fin:
            fout.write(str(self.preproc(line), 'utf-8'))
        fin.close()
        fout.close()

    def set_morphology(self, morphology, verbosity=0):
        '''Assign the Morphology object for this Language.'''
        self.morphology = morphology
        morphology.language = self
        for pos in morphology.values():
            pos.language = self
        morphology.directory = self.directory
        morphology.seg_units = self.seg_units
        morphology.phon_fst = morphology.restore_fst('phon', create_networks=False)

    def load_morpho(self, fsts=None, ortho=True, phon=False,
                    segment=False, recreate=False, guess=True, verbose=False):
        """Load words and FSTs for morphological analysis and generation."""
        fsts = fsts or self.morphology.pos
        opt_string = ''
        if segment:
            opt_string = 'segmentation'
        elif phon:
            opt_string = 'phonetic'
        if not self.has_cas(generate=phon, guess=False,
                            phon=phon, segment=segment):
            print('No {} FST available for {}!'.format(opt_string, self))
#            return False
        msg_string = Language.T.tformat('Loading morphological data for {0}{1} ...',
                                        [self, ' (' + opt_string + ')' if opt_string else ''],
                                        self.tlanguages)
        print(msg_string)
#        print()
        # In any case, assume the root frequencies will be needed?
        self.morphology.set_root_freqs()
        self.morphology.set_feat_freqs()
        if ortho:
            # Load unanalyzed words
            self.morphology.set_words(ortho=True)
            # Load pre-analyzed words
            self.morphology.set_analyzed(ortho=True)
            self.morphology.set_suffixes(verbose=verbose)
        if phon:
            # Load unanalyzed words
            self.morphology.set_words(ortho=False)
            # Load pre-analyzed words
            self.morphology.set_analyzed(ortho=False)
            self.morphology.set_suffixes(verbose=verbose)
        for pos in fsts:
            # Load pre-analyzed words if any
            if ortho:
                self.morphology[pos].set_analyzed(ortho=True)
                self.morphology[pos].make_generated()
            if phon:
                self.morphology[pos].set_analyzed(ortho=False)
            # Load lexical anal and gen FSTs (no gen if segmenting)
            if ortho:
                self.morphology[pos].load_fst(gen=not segment,
                                              create_casc=False,
                                              phon=False, segment=segment,
                                              recreate=recreate, verbose=verbose)
            if phon:
                self.morphology[pos].load_fst(gen=True,
                                              create_casc=False,
                                              phon=True, segment=segment,
                                              recreate=recreate, verbose=verbose)
            # Load guesser anal and gen FSTs
            if not segment and guess:
                if ortho:
                    self.morphology[pos].load_fst(gen=True, guess=True, phon=False, segment=segment,
                                                  create_casc=False,
                                                  recreate=recreate, verbose=verbose)
                if phon:
                    self.morphology[pos].load_fst(gen=True, guess=True, phon=True, segment=segment,
                                                  create_casc=False,
                                                  recreate=recreate, verbose=verbose)
        return True

    def get_fsts(self, generate=False, phon=False, segment=False):
        '''Return all analysis FSTs (for different POSs) satisfying phon and segment contraints.'''
        fsts = []
        for pos in self.morphology.pos:
            if phon:
                fst = self.morphology[pos].get_fst(generate=True, phon=True)
            else:
                fst = self.morphology[pos].get_fst(generate=generate, segment=segment)
            if fst:
                fsts.append(fst)
        return fsts

    def has_cas(self, generate=False, guess=False, phon=False, segment=False):
        """Is there at least one cascade file for the given FST features?"""
        for pos in self.morphology.pos:
            if self.morphology[pos].has_cas(generate=generate, 
                                            guess=guess, phon=phon, segment=segment):
                return True
        return False

    ### Analyze words or sentences

    def anal_file(self, pathin, pathout=None, preproc=True, postproc=True, pos=None,
                  root=True, citation=True, segment=False, gram=True,
                  knowndict=None, guessdict=None, cache=True, no_anal=True,
                  phon=False, only_guess=False, guess=True, raw=False,
                  sep_punc=True, word_sep='\n', sep_ident=False, minim=False,
                  feats=None, simpfeats=None,
                  # Ambiguity
                  rank=True, report_freq=True, nbest=100,
                  report_n=50000,
                  lower=True, lower_all=False, nlines=0, start=0):
        """Analyze words in file, either writing results to pathout, storing in
        knowndict or guessdict, or printing out.
        saved is a dict of saved analyses, to save analysis time for words occurring
        more than once.
        """
        preproc = preproc and self.preproc
        postproc = postproc and self.postproc
        citation = citation and self.citation_separate
        storedict = True if knowndict != None else False
        try:
            filein = open(pathin, 'r', encoding='utf-8')
            # If there's no output file and no outdict, write analyses to terminal
            out = sys.stdout
            if segment:
                print('Segmenting words in', pathin)
            else:
                print('Analyzing words in', pathin)
            if pathout:
                # Where the analyses are to be written
                fileout = open(pathout, 'w', encoding='utf-8')
                print('Writing to', pathout)
                out = fileout
            fsts = pos or self.morphology.pos
            n = 0
            # Save words already analyzed to avoid repetition
            if no_anal:
                no_anal = []
            else:
                no_anal = None
            # Store final representations here; these depend not only on analyses but also
            # on various options to this method, like minim
            local_cache = {}
            # If nlines is not 0, keep track of lines read
            lines = filein.readlines()
            if start or nlines:
                lines = lines[start:start+nlines]
            for line in lines:
                if n % report_n == 0:
                    print("Analyzed {} lines".format(n))
                n += 1
                # Separate punctuation from words
                if sep_punc:
                    line = self.morphology.sep_punc(line)
                identifier = ''
                string = ''
                if sep_ident:
                    # Separate identifier from line
                    identifier, line = line.split('\t')
                    string = "{}\t".format(identifier)
                # Segment into words
                for w_index, word in enumerate(line.split()):
                    # Ignore punctuation
#                    if word in self.morphology.punctuation:
#                        continue
                    # Lowercase on the first word, assuming a line is a sentence
                    if lower_all or (lower and w_index == 0):
                        word = word.lower()
                    if word in local_cache:
#                        print("{} already in cache: {}".format(word, local_cache[word]))
                        analysis = local_cache[word]
                        if storedict:
                            if analysis:
                                add_anals_to_dict(self, analysis, knowndict, guessdict)
                        elif minim:
                            if w_index != 0:
                                string += " "
                            string += analysis
                        elif raw or not minim:
                            print(analysis, file=out)
                    else:
                        # If there's no point in analyzing the word (because it contains
                        # the wrong kind of characters or whatever), don't bother.
                        # (But only do this if preprocessing.)
                        analysis = preproc and self.morphology.trivial_anal(word)
                        if analysis:
                            if minim:
                                analysis = word
                            elif raw:
                                analysis = (word, [])
                            elif segment:
                                analysis = "{}: {}\n".format(word, analysis)
                            else:
                                analysis = 'word: ' + analysis + '\n'
                        else:
                            # Attempt to analyze the word
                            form = word
                            if preproc:
                                form = self.preproc(form)
                            analyses = self.anal_word(form, fsts=fsts, guess=guess,
                                                      phon=phon, only_guess=only_guess, segment=segment,
                                                      root=root, stem=True, citation=citation and not raw, gram=gram, 
                                                      preproc=False, postproc=postproc and not raw,
                                                      cache=cache, no_anal=no_anal,
                                                      rank=rank, report_freq=report_freq, nbest=nbest,
                                                      string=not raw, print_out=False,
                                                      only_anal=storedict)
                            if minim:
                                analysis = self.minim_string(form, analyses, feats=feats, simpfeats=simpfeats)
                            elif raw and analyses: 
                                analyses = (form, [(anal[0], anal[1], anal[2]) if len(anal) > 2 else (anal[0],) for anal in analyses])
                            # If we're storing the analyses in a dict, don't convert them to a string
                            if storedict or raw:
                                analysis = analyses
                            # Otherwise (for file or terminal), convert to a string
                            elif not minim:
                                if analyses:
                                    # Convert the analyses to a string
                                    analysis = self.analyses2string(word, analyses, seg=segment, form_only=not gram,
                                                                    word_sep=word_sep)
                                elif segment:
                                    analysis = "{}: {}\n".format(word, form)
                                else:
                                    analysis = '?word: ' + word + '\n'
                        # Either store the analyses in the dict or write them to the terminal or the file
                        if storedict:
                            if analysis:
                                add_anals_to_dict(self, analysis, knowndict, guessdict)
                        elif minim:
                            if w_index != 0:
                                string += " "
                            string += analysis
                        elif raw:
                            analysis = self.pretty_analyses(analysis)
                            print(analysis, file=out)
                        elif not minim:
                            print(analysis, file=out)
                        local_cache[word] = analysis
                if minim:
                    # End of line
                    print(string, file=out)
            filein.close()
            if pathout:
                fileout.close()
        except IOError:
            print('No such file or path; try another one.')

    def minim_string(self, form, analyses=None, feats=None, simpfeats=None):
        """Create a minimal string representing the analysis of a word.
        feats are features to include from the FeatStruct(s) in the
        analyses."""
#        print('form {}, analyses {}'.format(form, analyses))
        analysis = "{}".format(form)
        if analyses:
            root_pos = set()
            if len(analyses) == 1:
                if analyses[0][0]:
                    a = analyses[0]
                    # There is a real analysis
                    pos = a[0]
                    root = a[1]
                    suffixes = ''
                    if '+' in root:
                        # This would not work for prefixes
                        root, x, suffixes = root.partition('+')
                    rpg_string = "{}:{}".format('*' if root==form else root, pos)
                    part_fs = ''
                    if feats:
                        fs = a[3]
                        if fs:
                            part_fs = fs.part_copy(feats, simpfeats).__repr__()
                            rpg_string = "{}:{}".format(rpg_string, part_fs)
                    if suffixes:
                        analysis = "{};{} ({})".format(analysis, rpg_string, suffixes)
                    else:
                        analysis = "{};{}".format(analysis, rpg_string)
            else:
                for anal in analyses:
                    pos = anal[0]
                    root = anal[1]
                    rpg_string = '*' if root==form else root
                    if pos:
                        rpg_string = "{}:{}".format('*' if root==form else root, pos)
                        if feats:
                            fs = anal[3]
                            if fs:
                                part_fs = fs.part_copy(feats, simpfeats).__repr__()
                                rpg_string = "{}:{}".format(rpg_string, part_fs)
                    root_pos.add(rpg_string)
#                    if pos:
#                        root_pos.add((root, ":" + pos))
#                    else:
#                        root_pos.add((root, ''))
                if root_pos:
                    rp_string = '|'.join(root_pos)
# ["{}{}".format(r, p) for r, p in root_pos])
                    analysis = "{};{}".format(analysis, rp_string)
        return analysis

    def pretty_analyses(self, analyses):
        """Print raw analyses."""
        if not analyses:
            return ''
        form = analyses[0]
        anals = analyses[1]
        s = '- ' + form + '\n'
        if anals:
            for anal in anals:
                if len(anal) == 1:
                    s += '  {}\n'.format(anal[0])
                else:
                    # root, features, frequency
                    s += '  {} {} {}\n'.format(anal[0], anal[1].__repr__(), anal[2])
        return s

    def analyses2string(self, word, analyses, seg=False, form_only=False, word_sep='\n',
                        webdicts=None):
        '''Convert a list of analyses to a string, and if webdicts, add analyses to dict.'''
#        print("analyses2string: {}".format(analyses))
        if seg:
            if analyses:
                analyses = [':'.join((a[0], a[1])) for a in analyses]
                return "{} -- {}{}".format(word, ';;'.join(analyses), word_sep)
            else:
                return word + word_sep
        elif form_only:
            if analyses:
#                print('analyses', analyses)
                return word + ': ' + ', '.join(analyses) + word_sep
            else:
                return word + word_sep
        s = ''
        if not analyses:
            s += '?'
        s += Language.T.tformat('{}: {}\n', ['word', word], self.tlanguages)
        for analysis in analyses:
            pos = analysis[0]
            if pos:
                webdict = None
                pos = pos.replace('?', '')
                if webdicts != None:
                    webdict = {}
                    webdicts.append(webdict)
                if pos in self.morphology:
                    if self.morphology[pos].anal2string:
                        s += self.morphology[pos].anal2string(analysis, webdict=webdict)
                    else:
                        s += self.morphology[pos].pretty_anal(analysis, webdict=webdict)
                elif self.morphology.anal2string:
                    s += self.morphology.anal2string(analysis, webdict=webdict)
        return s

    def analysis2dict(self, analysis, record_none=False, ignore=[]):
        """Convert an analysis (a FeatStruct) to a dict."""
        dct = {}
        for k, v in analysis.items():
            if isinstance(v, FeatStruct):
                v_dict = self.analysis2dict(v, record_none=record_none, ignore=ignore)
                if v_dict:
                    # Could be {}
                    dct[k] = v_dict
            elif not v:
                # v is None, False, '', or 0
                if record_none:
                    dct[k] = None
            elif k not in ignore:
                dct[k] = v
        return dct

    def cache(self, form, root, fs, dct):
        """Add an analysis to the cache dictionary."""
        if form in dct:
            dct[form].append((root, fs))
        else:
            dct[form] = [(root, fs)]

    def anal_word(self, word, fsts=None, guess=True, only_guess=False,
                  phon=False, segment=False, webdicts=None,
                  root=True, stem=True, citation=True, gram=True,
                  get_all=True, to_dict=False, preproc=False, postproc=False,
                  cache=True, no_anal=None, string=False, print_out=False,
                  rank=True, report_freq=True, nbest=100,
                  only_anal=False):
        '''Analyze a single word, trying all existing POSs, both lexical and guesser FSTs.

        [ [POS, {root|citation}, FSSet] ... ]
        '''
        # Before anything else, check to see if the word is in the list of words that
        # have failed to be analyzed
        if no_anal != None and word in no_anal:
            return None
        # Whether the analyses are found in the cache
        found = False
        preproc = preproc and self.preproc
        postproc = postproc and self.postproc
        citation = citation and self.citation_separate
        analyses = []
        to_cache = [] if cache else None
        fsts = fsts or self.morphology.pos
        # See if the word is cached (before preprocessing/romanization)
        cached = self.get_cached_anal(word)
        if cached:
            found = True
#            print("Found cached anal for {}".format(word))
            analyses = self.proc_anal(word, cached, None,
                                      show_root=root, citation=citation, stem=stem,
                                      segment=segment, guess=False,
                                      postproc=postproc, gram=gram,
                                      freq=rank or report_freq)
        else:
            if preproc:
                # Convert to roman, for example
                form = self.preproc(word)
            else:
                form = word
            # See if the word is unanalyzable ...
            unal_word = self.morphology.is_word(form)
            if unal_word:
                if only_anal:
                    return []
                a = self.simp_anal([unal_word], postproc=postproc, segment=segment)
                if cache:
                    to_cache.append((form, ''))
                if segment:
                    analyses.append(form)
                else:
                    analyses.append(a)
            # ... or is already analyzed, without any root/stem (for example, there is a POS and/or
            # a translation
            elif form in self.morphology.analyzed:
                if only_anal:
                    return []
                # Assume these are the *only* analyses
                get_all = False
                a = self.proc_anal_noroot(form, self.morphology.get_analyzed(form), segment=segment)
                if cache:
                    to_cache.extend(a)
                analyses.extend(a)
            else:
                # Try stripping off suffixes
                suff_anal = self.morphology.strip_suffixes(form)
                if suff_anal:
                    if cache:
                        to_cache.extend(suff_anal)
                    for stem, fs in suff_anal:
                        cat = fs.get('pos', '')
                        analyses.append((cat, stem, stem, fs, 100))
            if not analyses or get_all:
                if not only_guess:
                    for pos in fsts:
                        #... or already analyzed within a particular POS
                        preanal = self.morphology[pos].get_analyzed(form, sep_anals=True)
                        if preanal:
                            if cache:
                                to_cache.extend(preanal)
                            analyses.extend(self.proc_anal(form, preanal, pos,
                                                           show_root=root, citation=citation, stem=stem,
                                                           segment=segment, guess=False,
                                                           postproc=postproc, gram=gram,
                                                           freq=rank or report_freq))
                if not analyses or get_all:
                    if not only_guess:
                        # We have to really analyze it; first try lexical FSTs for each POS
                        for pos in fsts:
                            analysis = self.morphology[pos].anal(form, phon=phon, segment=segment,
                                                                 to_dict=to_dict, sep_anals=True)
                            if analysis:
                                if cache:
                                    to_cache.extend(analysis)
                                # Keep trying if an analysis is found
                                analyses.extend(self.proc_anal(form, analysis, pos,
                                                               show_root=root, citation=citation and not segment,
                                                               segment=segment, stem=stem,
                                                               guess=False, postproc=postproc, gram=gram,
                                                               freq=rank or report_freq))
                    # If nothing has been found, try guesser FSTs for each POS
                    if not analyses and guess:
                        # Accumulate results from all guessers
                        for pos in fsts:
                            analysis = self.morphology[pos].anal(form, guess=True, phon=phon, segment=segment,
                                                                 to_dict=to_dict, sep_anals=True)
                            if analysis:
                                if cache:
                                    to_cache.extend(analysis)
                                analyses.extend(self.proc_anal(form, analysis, pos, show_root=root,
                                                               citation=citation and not segment,
                                                               segment=segment, guess=True, gram=gram,
                                                               postproc=postproc, freq=rank or report_freq))
        if cache and not found:
#            print("Adding new anal {}, {}".format(word, to_cache))
            # Or use form instead of word
            self.add_new_anal(word, to_cache)
        if not analyses:
            # Impossible to analyze the word/form.
            if no_anal != None:
                no_anal.append(word)
            if cache and not found:
#                print("Caching unanalyzed word: {}".format(word))
                # Or use form instead of word
                self.add_new_anal(word, to_cache)
            return analyses
        if rank and len(analyses) > 1:
            analyses.sort(key=lambda x: -x[-1])
        # Select the n best analyses
        analyses = analyses[:nbest]
        string = ''
        if print_out or webdicts != None:
            # Print out stringified version and/or add analyses to webdicts
            string = self.analyses2string(word, analyses, seg=segment,
                                          form_only=not gram, webdicts=webdicts)
            if print_out:
                print(string)
        elif not string and not segment:
            analyses =  [(anal[1], anal[-2], anal[-1]) if len(anal) > 2 else (anal[1],) for anal in analyses]

        return analyses

    def simp_anal(self, analysis, postproc=False, segment=False):
        '''Process analysis for unanalyzed cases.'''
        if segment:
            return analysis[0], analysis[1], 100000
#            return analysis[0]
        elif postproc:
            # Convert the word to Geez.
            analysis[1] = self.postproc(analysis[1])
#            analysis[0] = self.postproc(analysis[0])
        pos, form = analysis
        return pos, form, None, 100000
#        return None, analysis[0], None, 100000

    def proc_anal_noroot(self, form, analyses, segment=False):
        '''Process analyses with no roots/stems.'''
        return [(analysis.get('pos'), None, None, analysis, None, 0) for analysis in analyses]

    def proc_anal(self, form, analyses, pos, show_root=True, citation=True,
                  segment=False, stem=True, guess=False,
                  postproc=False, gram=True, string=False,
                  freq=True):
        '''Process analyses according to various options, returning a list of analysis tuples.
        If freq, include measure of root and morpheme frequency.'''
#        print("Proc anal {} ; {} ; {}".format(form, pos, analyses))
        results = set()
        if segment:
            res = []
            for analysis in analyses:
                feats = analysis[1]
                if not feats:
                    # No analysis
                    continue
                if isinstance(feats, str):
                    pos1 = feats
                else:
                    pos1 = feats.get('pos')
                pos = pos1 or pos
                root = self.postpostprocess(analysis[0])
                # Remove { } from root
                real_root = Language.root_from_seg(root)
#                print("Root {}, real root {}".format(root, real_root))
                root_freq = 0
                if freq:
#                    print("Figuring freq for root {} and feats {}".format(real_root, feats.__repr__()))
                    root_freq = self.morphology.get_root_freq(real_root, feats)
                    feat_freq = self.morphology.get_feat_freq(feats)
                    root_freq *= feat_freq
                res.append((pos, root, root_freq))
#            print("Processed: {}".format(res))
            return res
        for analysis in analyses:
            root = self.postpostprocess(analysis[0])
#            root = analysis[0]
            grammar = analysis[1]
            if not grammar:
#                results.add((root, None, 0))
                continue
#                p = pos or ''
            elif not pos:
                p = grammar.get('pos', '')
            else:
                p = pos
            cat = '?' + p if guess else p
            # grammar is a single FS
            if not show_root and not segment:
                analysis[0] = None
            if postproc and p in self.morphology and self.morphology[p].postproc:
                self.morphology[p].postproc(analysis)
#            proc_root = analysis[0]
            root_freq = 0
#            for g in grammar:
            if freq and grammar:
                # The freq score is the count for the root-feature combination
                # times the product of the relative frequencies of the grammatical features
                root_freq = self.morphology.get_root_freq(root, grammar)
                feat_freq = self.morphology.get_feat_freq(grammar)
                root_freq *= feat_freq
            # Find the citation form of the root if required
            cite = None
            if citation and p and self.morphology[p].citation:
                citeform = self.morphology[p].citation(root, grammar, guess, stem)
                if postproc and citeform:
                    cite = self.postprocess(citeform)
            # Prevent analyses with same citation form and FS (results is a set)
            # Include the grammatical information at the end in case it's needed
            results.add((cat, root, cite, grammar if gram else None, grammar, round(root_freq)))
        return list(results)

    def ortho2phon(self, word, gram=False, raw=False, return_string=False,
                   gram_pre='-- ', postpostproc=False,
                   rank=True, nbest=100, report_freq=True):
        '''Convert a form in non-roman to roman, making explicit features that are missing in orthography.
        @param word:     word to be analyzed
        @type  word:     string or unicode
        @param gram:     whether a grammatical analysis is to be included
        @type  gram:     boolean
        @param return_string: whether to return string analyses (needed for phon_file)
        @type  return_string: boolean
        @param gram_pre: prefix to put before form when grammatical analyses are included
        @type  gram_pre: string
        @param postpostproc: whether to call postpostprocess on output form
        @type  postpostproc: boolean
        @param rank: whether to rank the analyses by the frequency of their roots
        @type  rank: boolean
        @param nbest: return or report only this many analyses
        @type  nbest: int
        @param report_freq: whether to report the frequency of the root
        @type  report_freq: boolean
        @return:         a list of analyses
        @rtype:          list of (root, feature structure) pairs
        '''
        preproc = self.preprocess(word)
        # An output form to count, analysis dictionary
        results = {}
        # Is the word in the word or analyzed lists?
        analyzed = self.morphology.ortho2phon(preproc)
        if analyzed:
            # Just add each form with no analysis to the dict
            if postpostproc:
                analyzed = [self.postpostprocess(a) for a in analyzed]
            results = dict([(a, '') for a in analyzed])
        else:
            # Try to analyze it with FSTs
            for posmorph in self.morphology.values():
                output = posmorph.ortho2phon(preproc, rank=rank)
                if output:
                    # Analyses found for posmorph; add each to the dict
                    for form, anal in output.items():
#                        root_count = count_anal[0]
#                        anal = count_anal[1:]
                        if gram:
                            if not raw:
                                anal = [(a[0], posmorph.anal2string(a[1:], None)) for a in anal]
                            else:
                                anal = [(a[0], a[2], a[4]) for a in anal]
                        else:
                            anal = [(a[0], a[1:]) for a in anal]
                        if postpostproc:
                            form = self.postpostprocess(form)
                        results[form] = results.get(form, []) + anal
            if not results:
                # No analysis
                # First phoneticize the form and mark as unknown ('?')
                form = '?' + self.morphology.phonetic(preproc)
                if postpostproc:
                    form = self.postpostprocess(form)
                # Then add it to the dict
                results = {form: ''}
        # Now do something with the results
        # Convert the result dict to a list (ranked if rank=True)
        result_list = []
        for f, anals in results.items():
            count = 0
            anal_list = []
            if anals:
                for a in anals:
                    count += a[0]
                    anal_list.append(a[1:])
            result_list.append((f, count, anal_list))
        if rank:
            result_list.sort(key=lambda x: -x[1])
        result_list = result_list[:nbest]
        if gram:
            # Include grammatical analyses
            if not raw:
                if return_string:
                    # Return the results as a string
                    return [(r[0], r[1:]) for r in result_list]
                # Print out the results
                for f, c, anals in result_list:
                    print(gram_pre + f)
                    for anal in anals:
                        print(anal[0], end='')
            else:
                # Return the raw results
                return result_list
        elif raw or return_string:
            # Return only the forms and frequencies
            if rank and report_freq:
                return [(r[0], r[1]) for r in result_list]
            else:
                return [r[0] for r in result_list]
        else:
            # Print out only the forms
            for anal, count in [(r[0], r[1]) for r in result_list]:
                if rank and report_freq:
                    print('{} ({})'.format(anal, count), end=' ')
                else:
                    print('{}'.format(anal), end=' ')
            print()

    def ortho2phon_file(self, infile, outfile=None, gram=False,
                        word_sep='\n', anal_sep=' ', print_ortho=True,
                        postpostproc=False,
                        rank=True, report_freq=True, nbest=100,
                        start=0, nlines=0):
        '''Convert non-roman forms in file to roman, making explicit features that are missing in the orthography.
        @param infile:   path to a file to read the words from
        @type  infile:   string
        @param outfile:  path to a file where analyses are to be written
        @type  outfile:  string
        @param gram:     whether a grammatical analysis is to be included
        @type  gram:     boolean
        @param word_sep:  word separator (only when gram=False)
        @type  word_sep:  string
        @param anal_sep:  analysis separator (only when gram=False)
        @type  anal_sep:  string
        @param print_ortho: whether to print the orthographic form first
        @type  print_ortho: boolean
        @param postpostproc: whether to call postpostprocess on output form
        @type  postpostproc: boolean
        @param rank: whether to rank the analyses by the frequency of their roots
        @type  rank: boolean
        @param report_freq: whether to report the frequency of the root
        @type  report_freq: boolean
        @param start:    line to start analyzing from
        @type  start:    int
        @param nlines:   number of lines to analyze (if not 0)
        @type  nlines:   int
        '''
        try:
#            filein = codecs.open(infile, 'r', 'utf-8')
            filein = open(infile, 'r', encoding='utf-8')
            # Whether to write analyses to terminal
            out = sys.stdout
            # Dictionary to store analyzed words in
            saved_dct = {}
            print('Analyzing words in', infile)
            if outfile:
                # Where the analyses are to be written
#                out = codecs.open(outfile, 'w', 'utf-8')
                out = open(outfile, 'w', encoding='utf-8')
                print('Writing analysis to', outfile)
            lines = filein.readlines()
            if start or nlines:
                lines = lines[start:start+nlines]
            begun = False
            for line in lines:
                # Separate punctuation from words
                line = self.morphology.sep_punc(line)
                # Segment into words
                for word in line.split():
                    if word in saved_dct:
                        # Don't bother to analyze saved words
                        analysis = saved_dct[word]
                    else:
                        # Analyze the word
                        analysis = self.ortho2phon(word, gram=gram,
                                                   postpostproc=postpostproc,
                                                   raw=False, return_string=True,
                                                   rank=rank, report_freq=report_freq, nbest=nbest)
                        saved_dct[word] = analysis
                    # Write the analysis to file or stdout
                    if gram:
                        print("{0}".format(word), file=out)
                        for form, anal in analysis:
                            print("-- {0}".format(form), file=out)
                            for a in anal[1:]:
                                for a1 in a:
                                    print("{0}".format(a1[0]), end='', file=out)
                        print(file=out)
                    else:
                        # Start with the word_sep string
                        if begun:
                            print(file=out, end=word_sep)
                        if print_ortho:
                            # Print the orthographic form
                            print("{0} ".format(word), end='', file=out)
                        for anal in analysis[:-1]:
                            # Print an analysis followed by the analysis separator
                            print("{0} ({1})".format(anal[0], anal[1]), end=anal_sep, file=out)
                        # Print the last analysis with no analysis separator
                        if analysis:
                            print("{0} ({1})".format(analysis[-1][0], analysis[-1][1]), end='', file=out)
                    begun=True
            if not gram:
                # Final newline
                print(file=out)
            filein.close()
            if outfile:
                out.close()
        except IOError:
            print('No such file or path; try another one.')

    def set_web(self):
        """Set the features and number of values and index for each POS."""
        if not self.webdata:
            ifdict = self.get_if_dict()
            multpos = True
            limit1 = 5
            limit2 = 12
            if len(self.morphology) == 1 and 'all' in self.morphology:
                multpos = False
                limit1 = 6
                limit2 = 14
            for index1, posmorph in enumerate(self.morphology.values()):
                # Set web features if this hasn't already happened
                posmorph.set_web_feats()
                webfeats = posmorph.web_features
                html = "<tr>"
                if multpos:
                    html += "<td class='pos'><span class='poslabeloff'>"
                    html += ifdict.get('pos_label')
                    html += "</span><br/><span class='vallabeloff'>"
                    html += posmorph.name
                    html += "</span></td>"
                html += "<td class='raiz'><span class='poslabeloff'>"
                html += ifdict.get('root_label')
                html += "</span><br/>"
                html += "<textarea class='raiz'></textarea></td>"
                for index2, feature in enumerate(webfeats):
                    value = feature[0]
                    html += "<td class='raiz'><span class='featlabeloff'>"
                    html += value
                    html += "</span><br /><textarea class='raiz'></textarea></td>"
                    if index2 == limit1 or index2 == limit2:
                        html += "</tr><tr>"
                        if multpos:
                            html += "<td></td>"
                html += "</tr></td></tr><tr><td colspan='8'><hr class='possep'><td></tr>"
                self.webdata.append((posmorph.name, posmorph.web_features, html))
                self.webdict[posmorph.name] = index1

    def anal_get_webindex(self, anal):
        """Get the index among the POS features displayed in the web app for the analysis."""
        pos = anal.get('POS', 'verb')
        return self.webdict.get(pos, 0)

    def anal2html(self, anal):
        """Convert a (web app) analysis to an HTML string."""
        pos = anal.get('pos')
        if not pos:
            print("No POS in analysis {}".format(anal))
            posmorph = self.morphology['all']
        else:
            posmorph = self.morphology[pos]
        webfeats = posmorph.web_features
        ifdict = self.get_if_dict()
        multpos = True
        limit1 = 5
        limit2 = 12
        if len(self.morphology) == 1 and 'all' in self.morphology:
            multpos = False
            limit1 = 6
            limit2 = 14
        html = "<tr>"
        if multpos:
            html += "<td class='pos'><span class='poslabel'>"
            html += ifdict.get('pos_label')
            html += "</span><br/><span class='vallabel'>"
            html += posmorph.name
            html += "</span></td>"
        html += "<td class='raiz'><span class='poslabel'>"
        html += ifdict.get('root_label')
        html += "</span><br/>"
        html += "<textarea class='raiz'>"
        html += "{}".format(anal.get('root', 'root'))
        html += "</textarea></td>"
        for index, feature in enumerate(webfeats):
            featname = feature[0]
            html += "<td class='raiz'><span class='featlabel'>"
            html += featname
            html += "</span><br/>"
            value = anal.get(featname)
            rows = 1
            if isinstance(value, list):
                rows = len(value)
                if len(value) > 1:
                    value = '\n'.join(value)
                else:
                    value = value[0]
            height = rows * 20
            html += "<textarea style='height: {}px' class='value'>".format(height)
            if value:
                html += "{}".format(value)
            html += "</textarea></td>"
            if index == limit1 or index == limit2:
                html += "</tr><tr>"
                if multpos:
                    html += "<td></td>"
        html += "</tr></td></tr><tr><td colspan='8'><hr class='possep'><td></tr>"
        return html

for name, entry in \
  [
   ('language_menu', (('eng', 'LANGUAGE'), ('spa', 'IDIOMA'))),
   ('login_menu', (('eng', 'LOG IN'), ('spa', 'IDENTIFICARSE'))),
   ('about_menu', (('eng', 'ABOUT'), ('spa', 'ACERCA DE'))),
   ('word_instruc', (('eng', 'Type a word in the space and hit the "Enter" key.'),
                     ('spa', 'Escriba una palabra y presione la tecla "Intro/Entrar."'))),
   ('another_instruc', (('eng', 'To analyze another word, click on the "Delete" button.'),
                        ('spa', 'Para analizar otra palabra, presione el botón "Borrar".'))),
   ('next_instruc', (('eng', 'To see another analysis, click on the "Next" button.'),
                     ('spa', 'Para ver otro análisis, presione el botón "Próximo".'))),
   ('delete_button', (('eng', 'Delete'), ('spa', 'Borrar'))),
   ('copy_button', (('eng', 'Copy'), ('spa', 'Copiar'))),
   ('next_button', (('eng', 'Next'), ('spa', 'Próximo'))),
   ('pos_label', (('eng', 'part of speech'), ('spa', 'categoría gramatical'))),
   ('root_label', (('eng', 'root'), ('spa', 'raíz'))),
   ('analysis_head', (('eng', 'Morphological analysis'), ('spa', 'Análisis morfológico'))),
   ('analysis_label', (('eng', 'Analysis'), ('spa', 'Análisis')))
   ]:
   Language.add_IF(name, entry)
