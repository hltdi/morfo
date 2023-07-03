"""
This file is part of morfo, which is part of the PLoGS project.

    <http://homes.soic.indiana.edu/gasser/plogs.html>

    Copyleft 2018, 2019, 2023.
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

2023.07.01
Created Languages class.

"""
import time
from .language import *
from .session import *
from importlib import reload
import sys
# import anal_gui

###
### Loading languages
###

#class MorfoSession(dict):
#
#    def __init__(self):
#        dict.__init__(self)
#        self['languages'] = {}
#
#    def __repr__(self):
#        return "@@MS@@: {} languages".format(len(self['languages']))

LANGUAGES = {}

# Convert 2-character to 3-character language codes
ISO1to3 = {'qu': 'quz',
           'es': 'spa',
           'gn': 'grn',
           'ki': 'quc',
           'ks': 'gru',
           'ch': 'sgw',
           'sl': 'stv'}

def get_lang_id(string):
    '''Get a 3-character language identifier from a string which may be the name
    of the language or a 2-character code.'''
    # Expand code if
    string = ISO1to3.get(string, string)
    lang = string if len(string) <= 3 else string.replace("'", "")[:2]
    return lang.lower()

def get_lang_dir(abbrev):
    return os.path.join(LANGUAGE_DIR, abbrev)

def load_lang(lang, phon=False, segment=False, load_morph=True,
              session=None, interaction=None,
              # False, '', or the name of a cache file
              cache=True, guess=True, poss=None, verbose=True):
    """Load Morphology objects and FSTs for language with lang_id."""
    print("** load lang; session {} interaction {}".format(session, interaction))
    print("** morfo modules: {}".format([m for m in list(sys.modules) if 'morfo' in m]))
    lang_id = get_lang_id(lang)
    reload_file = False
    if session and lang_id not in session.get('languages', []):
        reload_file = True
    print("** reload {}".format(reload_file))
    language = None
    if lang_id == 'am':
        if reload_file:
            try:
                reload(am_lang)
            except:
                from . import am_lang
        else:
            from . import am_lang
        language = am_lang.AM
    elif lang_id == 'ti':
        if reload_file:
            try:
                reload(ti_lang)
            except:
                from . import ti_lang
        else:
            from . import ti_lang
        language = ti_lang.TI
    elif lang_id == 'es':
        if reload_file:
            try:
                reload(es_lang)
            except:
                from . import es_lang
        else:
            from . import es_lang
        language = es_lang.ES
    if language:
        # Attempt to load additional data from language data file;
        # and FSTs if load_morph is True.
        loaded = language.load_data(load_morph=load_morph, segment=segment,
                                    phon=phon, guess=guess, poss=poss, verbose=verbose)
        if not loaded:
            # Impossible to load additional data
            pass
    else:
        # Create the language from scratch
        language = Language.make('', lang_id, load_morph=load_morph,
                                 segment=segment, phon=phon, guess=guess, poss=poss,
                                 verbose=verbose)
        if not language:
            # Impossible to make language with desired FST
            return False
#    if cache != False:
#        language.read_cache(segment=segment)
    print("** Created language {}".format(language))
    interaction['languages'][lang_id] = language
#    interaction['language'] = language
    if session:
        print("** session languages: {}".format(session['languages']))
        session['languages'].add(lang_id)
#    print("** Stored {}".format(language))
#    LANGUAGES[lang_id] = language
    if language.backup:
        # If there's a backup language, load its data file so the translations
        # can be used.
        load_lang(language.backup, load_morph=False, guess=guess, session=session,
                  interaction=interaction,
                  verbose=verbose)
    return True

def get_language(language, load=True, phon=False, segment=False, guess=True,
                 load_morph=True, cache='', verbose=False, session=None, interaction=None):
    """
    Get the language with lang_id, attempting to load it if it's not found
    and load is True.
    """
    print("** get language; session {} interaction {}".format(session, interaction))
    if isinstance(language, Language):
        return language
    lang_id = get_lang_id(language)
#    lang = LANGUAGES.get(lang_id, None)
    lang = interaction['languages'].get(lang_id, None)
    if lang:
        print("** Found language in session languages")
    if not lang:
        if load:
            print("** Loading language {}".format(lang_id))
            if not load_lang(lang_id, phon=phon, segment=segment, guess=guess,
                             session=session, interaction=interaction,
                             load_morph=load_morph, cache=cache,
                             verbose=verbose):
                return False
        return interaction['languages'].get(lang_id, None)
#    LANGUAGES.get(lang_id, None)
    if load_morph and not lang.morpho_loaded:
        print("** Loading morphology")
        lang.load_morpho(phon=phon, segment=segment, guess=guess)
        return lang
    if not load_morph:
        return lang
    fst = lang.get_fsts(phon=phon, segment=segment)
    if not fst and load:
        print("Couldn't find FSTs")
#        print("You cannot do both morphological analysis and segmentation in the same session!")
#        if segment:
#            print("Please exit() and start a new session to do segmentation!")
#        else:
#            print("Please exit() and start a new session to do morphological analysis!")
        return
    return lang
    
def load_pos(language, pos, scratch=False):
    """Load FSTs for a single POS, overriding compiled FST if scratch is True."""
    language.morphology[pos].load_fst(scratch, recreate=True, verbose=True)

def load_langs(abbrev, l1, poss1, l2, poss2,
               load_lexicons=True, session=None, interaction=None, verbose=True):
    """Load two languages for translation between them."""
    load_lang(l1, phon=False, segment=False, load_morph=True, session=session, interaction=interaction,
              guess=False, poss=poss1, verbose=verbose)
    load_lang(l2, phon=False, segment=False, load_morph=True, session=session, interaction=interaction,
              guess=False, poss=poss2, verbose=verbose)
    lang1 = get_language(l1, verbose=verbose, session=session)
    lang2 = get_language(l2, verbose=verbose, session=session)
    return Multiling(abbrev, (lang1, poss1), (lang2, poss2),
                     load_lexicons=load_lexicons)
    
