"""
This file is part of morfo, which is a project of PLoGS

    2018. Michael Gasser.

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

------------------------------------------------------
Author: Michael Gasser <gasser@indiana.edu>

morpho:

This package includes modules that deal with finite-state transducers (FSTs) weighted
with feature structure sets (as in Amtrup, 2003).

Transduction handles ambiguity, returning output strings and accumulated weights for
all paths through an FST.

Composition of weighted FSTs is also supported.
"""

__version__ = '4.0'
__author__ = 'Michael Gasser'

from .fst import *
