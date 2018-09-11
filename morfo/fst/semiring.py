"""
This file is part of L3Morpho, which is part of the PLoGS project.

    <http://homes.soic.indiana.edu/gasser/plogs.html>

    Copyleft 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2016, 2017.
    PLoGS and Michael Gasser <gasser@indiana.edu>.

    L3Morpho is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    L3Morpho is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with L3Morpho.  If not, see <http://www.gnu.org/licenses/>.
--------------------------------------------------------------------

Rudimentary implementation of semirings for use in weighted FSTs.
Includes feature structures sets, as in Amtrup (2003).
Feature structures based on those in NLTK <http://www.nltk.org/>.

Author: Michael Gasser <gasser@indiana.edu>

2009-06-11: unification modified to accommodate 'fail' result
2011-06-04:
  Parsing of disjunctions in string FS representations:
  +-feat
  feat=val1|val2
2013-02-23:
  Sets of FeatStructs get cast properly to FSSets.
2017.05.10
  Add method for getting a feature value within a FSSet.
  Override union for FSSet so it returns an FSSet.
"""

from .fs import *
from .utils import *
# import re

######################################################################
# FeatStruct Sets
######################################################################

## Regular expressions needed for splitting strings into feature-value
## pairs

# either
# {+,-,+-} value
# or
# feat = value
SIMP_FVAL_RE = re.compile(r'([+-]{1,2}\w+?|\w+?\s*=\s*[^\]]+?)(?:,|\]|$)')

# feat = [...]
COMP_FVAL_RE = re.compile(r'(\w+?\s*=\s*\[.+?\])')

class FSSet(set):
    """Sets of feature structures."""

    def __init__(self, *items):
        '''Create a feature structure set from items, normally a list of feature structures or strings.'''
        # This may sill be needed for unpickling, when items is a tuple of a list of FeatStructs
        if len(items) > 0 and isinstance(items[0], (list, set)):
            items = items[0]
        if not isinstance(items, set):
            items = [(FeatStructParser().parse(i) if (isinstance(i, str) or isinstance(i, str)) else i) for i in items]
            # Freeze each feature structure
            for index, itm in enumerate(items):
                if isinstance(itm, FeatStruct):
                    itm.freeze()
                else:
                    # Umm...how is it possible for itm not to be a feature structure?
                    items[index] = tuple(itm)
        set.__init__(self, items)

    def __repr__(self):
        string = ''
        for i, fs in enumerate(self):
            string += fs.__repr__()
            if i < len(self) - 1:
                string += ';'
        return string

    def union(self, fsset):
        """Override set union method by casting result to FSSet."""
        res = set.union(self, fsset)
        return FSSet(res)

    def copy(self):
        """Return a copy of the FSSet."""
        fss = set()
        for fs in self:
            fss.add(fs.copy())
        return FSSet(fss)

    def remove(self, FS):
        """Remove the FS from all FSs in the set, returning the new FSSet (as a list!)."""
        fsset = self.unfreeze()
        to_remove = []
        for fs in fsset:
            for key in list(FS.keys()):
                # Assume there's only one level
                fs.pop(key)
            if not fs:
                # Nothing left in it; remove it
                to_remove.append(fs)
        for fs in to_remove:
            fsset.remove(fs)
        return fsset

    def unify(self, fs2, verbose=False):
        fs2_list = list(fs2)
        fs1_list = list(self)
        if verbose:
            print('FSS1: {}, FSS2: {}'.format(fs1_list, fs2_list))
        result1 = [simple_unify(f1, f2) for f1 in fs1_list for f2 in fs2_list]
        if verbose:
            print('Result1', result1)
        if every(lambda x: x == TOP, result1):
            # If everything unifies to TOP, return one of them
            return TOPFSS
        else:
            # Get rid of all instances of TOP and unification failures
            return FSSet(*filter(lambda x: x != 'fail', result1))

    def get(self, feature, default=None):
        """Get the value of the feature in the first FeatStruct that has one."""
        for fs in self:
            value = fs.get(feature)
            if value:
                return value
        return default

    def inherit(self):
        """Inherit feature values for all members of set, returning new set."""
        items = [item.inherit() for item in self]
        return FSSet(*items)

    @staticmethod
    def parse(string):
        """string could be a single FS or several separated by ';'."""
        if string == '[]':
            return TOPFSS
        strings = [s.strip() for s in string.split(';')]
        strings = reduce_lists([FSSet.proc_fv(s) for s in strings])
        return FSSet(*strings)

    @staticmethod
    def proc_fv(fv):
        '''Process a string representing feature-value pairs, returning
        a list of strings, one for each combination of alternatives
        specified by | or +-.
        '''
        fv_split = FSSet.split_rep(fv)
        if not fv_split:
            return fv
        res = FSSet.split_fval(fv_split[0])
        if len(fv_split) > 1:        
            for fv in fv_split[1:]:
#                print('res', res, 'fv', fv)
                res = FSSet.incorp_fval(res, fv)
        return ['[' + r + ']' for r in res]

    @staticmethod
    def split_rep(rep):
        '''Split a featstruc string representation into top-level feat-value
        pairs, assuming at most one level of nesting.'''
        rep0 = rep[1:-1]
        pos = 0
        res = []
        while pos < len(rep0):
            char = rep0[pos]
            if char in ', ':
                pos += 1
            else:
                comp = COMP_FVAL_RE.match(rep0[pos:])
                if comp:
                    fv = comp.group(1)
                    res.append(fv)
                    pos = pos + comp.end()
                else:
                    simp = SIMP_FVAL_RE.match(rep0[pos:])
                    if simp:
                        fv = simp.group(1)
                        res.append(fv)
                        pos = pos + simp.end()
                    else:
                        print('Something wrong at position', pos, char, 'in', rep)
        return res

    @staticmethod
    def split_fval(fval):
        '''Process a feature-value string returning alternatives if
        it contains | or +-.
        '''
        if '|' not in fval and '+-' not in fval:
            return [fval]
        elif '[' in fval or '=' in fval:
            fv0 = fval.partition('=')
            feat = fv0[0]
            values = fv0[2]
            if '[' in values:
                return [feat + '=' + x for x in FSSet.proc_fv(values)]
            else:
                # |
                return [feat + '=' + v for v in values.split('|')]
        else:
            # +-
            fv0 = fval.partition('+-')
            feat = fv0[-1]
            return ['+' + feat, '-' + feat]

    @staticmethod
    def incorp_fval(strings, fval):
        splitv = FSSet.split_fval(fval)
        return [s + ',' + x for s in strings for x in splitv]

    @staticmethod
    def cast(obj):
        """Cast object to a FSSet."""
        if isinstance(obj, FSSet):
            return obj
        elif isinstance(obj, FeatStruct):
            return FSSet(obj)
        elif isinstance(obj, (str, str)):
            return FSSet.parse(obj)
        else:
            return TOPFSS

    @staticmethod
    def update(fsset, feats):
        """Return a new fsset with feats updated to match each fs in fsset."""
        fslist = []
        for fs in fsset:
            fs_copy = feats.copy()
            fs_copy.update(fs)
            fslist.append(fs_copy)
        return FSSet(*fslist)

    @staticmethod
    def setfeats(fsset, condition, feature, value):
        """A new FSSet with feature set to value if condition is satisfied."""
        fslist = []
        for fs in fsset:
            if not condition or unify(fs, condition):
                # Copy because it's frozen
                fs_copy = fs.copy()
                fs_copy.setdefault(feature, value)
                fslist.append(fs_copy)
            else:
                fslist.append(fs)
        return FSSet(*fslist)

    def unfreeze(self):
        """A copy of the FSSet (as a list!) that is a set of unfrozen FSs."""
        return [fs.copy() for fs in self]

    @staticmethod
    def compare(fss):
        """Compare feature values in the FS set, returning a pair of dicts: shared values, different values."""
        if len(fss) == 1:
            return list(fss)[0], {}
        feats = set()
        shared = {}
        diffs = {}
        for fs in fss:
            feats.update(list(fs.keys()))
        for f in feats:
            # values of features f in all FSs
            values = [fs.get(f, None) for fs in fss]
            v0 = values[0]
            same = True
            index = 1
            while same and index < len(values):
                v = values[index]
                if v != v0:
                    same = False
                index += 1
            if same:
                shared[f] = v0
            else:
                diffs[f] = values
        return shared, diffs
            
## Feature structure that unifies with anything.
TOP = FeatStruct('[]')
TOP.freeze()
TOPFSS = FSSet(TOP)

class Semiring:

    def __init__(self, addition = None, multiplication = None,
                 in_set = None, zero = None, one = None):
        self.addition = addition
        self.multiplication = multiplication
        self.zero = zero
        self.one = one
        self.in_set = in_set

    def multiply(self, x, y):
        return self.multiplication(x, y)

    def add(self, x, y):
        return self.addition(x, y)

    def is_in_set(self, x):
        return self.in_set(x)

    def parse(self, s):
        """Parse a string into a weight."""
        if not s:
            # Default weight for this SR
            return self.one
        elif self == UNIFICATION_SR:
            return FSSet.parse(s)
        else:
            # Number
            return float(s)

### Three semirings

PROBABILITY_SR = Semiring(addition = lambda x, y: x + y,
                          multiplication = lambda x, y: x * y,
                          in_set = lambda x: isinstance(x, float) and x >= 0.0,
                          zero = 0.0,
                          one = 1.0)

TROPICAL_SR = Semiring(addition = lambda x, y: min([x, y]),
                       multiplication = lambda x, y: x + y,
                       in_set = lambda x: isinstance(x, float),
                       zero = None,  # really +infinity
                       one = 0.0)

### Operations for Unification semiring
def uni_add(x, y):
    return x.union(y)

def uni_mult(x, y):
    return x.unify(y)

def uni_inset(x):
    return isinstance(x, FSSet)

UNIFICATION_SR = Semiring(addition = uni_add,
                          multiplication = uni_mult,
                          in_set = uni_inset,
                          zero = set(),
                          one = TOPFSS)
