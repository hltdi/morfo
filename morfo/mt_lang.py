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

Create Language, Morphology, and POSMorphology objects for Maltese.
"""
from . import language

MT = language.Language("Malti", 'Mt',
                       seg_units=[[# consonants
                                   'b', 'ċ', 'd', 'f', 'ġ', 'h', 'ħ', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'z', 'ż',
                                   # vowels
                                   'a', 'e', 'i', 'o', 'u', 'è',
                                   # only in foreign words
                                   'y'
                                   ],
                                  {'g': ['g', 'għ']}
                                  ])

## Create Morphology object and verb POSMorphology object for Maltese,
## including punctuation and ASCII characters that are part of the romanization.
MT.set_morphology(language.Morphology((),
                                      pos_morphs=[('v', [], [], [])]))
#                                                  ('n', [], [], []),
#                                                  ('a', [], [], [])]))
