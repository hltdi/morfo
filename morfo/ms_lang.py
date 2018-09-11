"""
This file is part of L3Morpho.

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
Author: Michael Gasser <gasser@cs.indiana.edu>

Create Language, Morphology, and POSMorphology objects for Malay.
"""
from . import language

MS = language.Language("Bahasa Melayu", 'Ms',
                       seg_units=[[# consonants
                                   'b', 'c', 'd', 'f', 'h', 'j', 'l', 'm', 'p', 'r', 't', 'v', 'w', 'y', 'z',
                                   # vowels
                                   'a', 'e', 'i', 'o', 'u',
                                   # within-word punctuation
                                   '-',
                                   # Upper-case
                                   'B', 'C', 'D', 'F', 'H', 'J', 'L', 'M', 'P', 'R', 'T', 'V', 'W', 'Y', 'Z',
                                   'A', 'E', 'I', 'O', 'U'
                                   ],
                                  {'g': ['g', 'gh'],
                                   'G': ['G', 'Gh'],        # Gh may not be possible
                                   'k': ['k', 'kh'],
                                   'K': ['K', 'Kh'],
                                   'n': ['n', 'ng', 'ny'],
                                   'N': ['N', 'Ng', 'Ny'],  # Ng may not be possible
                                   's': ['s', 'sy'],
                                   'S': ['S', 'Sy']
                                   }
                                  ])

## Create Morphology object and verb POSMorphology object for Malay,
## including punctuation and ASCII characters that are part of the romanization.
MS.set_morphology(language.Morphology((), pos_morphs=[('all',)]))

def anal2string(anal):
    '''Convert an analysis to a string.

    anal is ("all", root, citation, gramFS, 'real' gramFS)
    '''
    root = anal[1]
    fs = anal[3]
    pos = fs.get('pos', '?')
    s = 'POS: {}, '.format(pos)
    pre = fs.get('pre')
    if pre and pre != '0':
        s += '{}-'.format(pre)
    if root:
        s += '<{}>'.format(root)
    suf = fs.get('suf')
    if suf and suf != '0':
        s += '-{}'.format(suf)
    s += '\n'
    return s

## Function that converts analyses to strings; the same for all POS.
MS.morphology['all'].anal2string = lambda fss: anal2string(fss)
