"""
This file is part of morfo, which is a project of PLoGS.

Copyleft 2018, 2019, 2023. PLoGS and Michael Gasser.

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

# __all__ = ['languages', 'language', 'morphology', 'strip', 'session', 'fst']

from flask import Flask, url_for, render_template, session
from flask_session import Session
_version = '1.0'

from .trans import *

print('\n@@@@ This is morfo, version {} @@@@\n'.format(_version))

app = Flask(__name__)
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

INTERACTION = None

@app.route('/set/')
def set():
    session['key'] = 'value'
    return 'ok'

@app.route('/get/')
def get():
    return session.get('key', 'not set')

#print("** app session interface: {}".format(app.session_interface))

def init_session(lg_abbrev, user=None, segment=False, web=True, session=None, interaction=None):
    """Create a session with the given language and user."""
#    if session:
#        session.clear()
    print("*** Creating interaction with session {}".format(session))
    if web:
        if 'languages' not in session:
            session['languages'] = {''}
        if 'user' not in session:
            session['user'] = User()
    if not interaction:
        # Create a MorfoSession for non-web interaction
        interaction = Interaction(user=user)
    language = get_language(lg_abbrev, segment=segment, session=session, interaction=interaction)
    if not language:
        print("WARNING: language {} not found!".format(lg_abbrev))
    if web:
        print("** setting language {} in session".format(lg_abbrev))
        session['language'] = lg_abbrev
        # Set web data for language
        language.set_web()
    return interaction
#    return Interaction(language, user=user)

def exit(session, save=True, cache=''):
    """Exit the program, caching any new analyses for each loaded language
    if save is True."""
    print("Quitting...")
    if not save:
        really_save = input("Are you sure you want to discard new anaylses?\n[Y]es/[N]o ")
        if really_save and really_save[0].lower() == 'y':
            return
    for abbrev in session['languages']:
        print("** Should be writing language {} here ***".format(abbrev))
#        languages.LANGUAGES.items():
#        language.write_cache(name=cache)
    session['languages'] = {''}
#    languages.LANGUAGES.clear()

def load(language, phon=False, segment=False, load_morph=True, cache='',
         guess=True, verbose=False):
    """Load a language's morphology.

    @param language: a language label
    @type  language: string
    """
    load_lang(language, phon=phon, segment=segment, load_morph=load_morph, cache=cache,
              guess=guess, verbose=verbose)

def seg_word(language, word, nbest=100, raw=False):
    '''Segment a single word and print out the results.
    
    @param language: abbreviation for a language
    @type  language: string
    @param word:     word to be analyzed
    @type  word:     string or unicode
#    @return:         a list of analyses (only if raw is True)
#    @rtype:          list of (root, feature structure) pairs
    '''
    language = get_language(language, phon=False, segment=True)
    if language:
        analysis = language.anal_word(word, preproc=True, postproc=True,
                                      gram=False, segment=True, only_guess=False,
                                      print_out=not raw, string=True)
        if raw:
            return analysis

def seg_file(language, infile, outfile=None,
             preproc=True, postproc=True, start=0, nlines=0):
    '''Analyze the words in a file, writing the analyses to outfile.

    @param infile:   path to a file to read the words from
    @type  infile:   string
    @param outfile:  path to a file where analyses are to be written
    @type  outfile:  string
    @param preproc:  whether to preprocess inputs
    @type  preproc:  boolean
    @param postproc: whether to postprocess outputs
    @type  postproc: boolean
    @param start:    line to start analyzing from
    @type  start:    int
    @param nlines:   number of lines to analyze (if not 0)
    @type  nlines:   int
    '''
    language = get_language(language, phon=False, segment=True)
    if language:
        language.anal_file(infile, outfile, gram=False,
                           pos=None, preproc=preproc, postproc=postproc,
                           segment=True, only_guess=False, guess=False,
                           start=start, nlines=nlines)

def anal_word(language, word, root=True, citation=True, gram=True,
              roman=False, segment=False, guess=False, dont_guess=False,
              web=None, cache='', rank=True, freq=True, nbest=100, raw=False,
              interaction=None,
              display_feats=None):
    '''Analyze a single word, trying all available analyzers, and print out
    the analyses.
    
    @param language: abbreviation for a language
    @type  language: string
    @param word:     word to be analyzed
    @type  word:     string or unicode
    @param root:     whether a root is to be included in the analyses
    @type  root:     boolean
    @param citation: whether a citation form is to be included in the analyses
    @type  citation: boolean
    @param gram:     whether a grammatical analysis is to be included
    @type  gram:     boolean
    @param roman:    whether the language is written in roman script
    @type  roman:    boolean
    @param segment:  whether to return the segmented input string rather than
                     the root/stem
    @type  segment:  boolean
    @param guess:    try only guesser analyzer
    @type guess:     boolean
    @param dont_guess: try only lexical analyzer
    @type dont_guess:  boolean
    @param web:      whether to create dicts to use in the web app
    @type web:       boolean
    @param rank:     whether to rank the analyses by the frequency of their roots
    @type  rank:     boolean
    @param freq:     whether to report frequencies of roots
    @type  freq:     boolean
    @param nbest:    maximum number of analyses to return or print out
    @type  nbest:    int
    @param raw:      whether the analyses should be returned in "raw" form
    @type  raw:      boolean
    @param display_feats: features to show in output string
    @type display_feats: list of strings or None
    @return:         a list of analyses (if raw is True); dict of features (if web is True)
    @rtype:          list of (root, feature structure) pairs or string->string dict
    '''
    global INTERACTION
    if not INTERACTION:
        INTERACTION = init_session(language, web=False)
#        interaction = Interaction()
    language = get_language(language, cache=cache, phon=False, segment=segment, interaction=INTERACTION)
    if language:
        if web:
            web = []
        analysis = language.anal_word(word, preproc= not roman,
                                      postproc=not roman and not raw,
                                      root=root, citation=citation, gram=gram,
                                      segment=segment, only_guess=guess,
                                      guess=not dont_guess, webdicts=web,
                                      nbest=nbest, display_feats=display_feats,
                                      string=not raw, print_out=not raw)
        if raw:
            return analysis
        elif web:
            return web

anal = anal_word

def anal_files(language, infiles, outsuff='.out',
               root=True, citation=True, gram=True,
               preproc=True, postproc=True, guess=False, raw=False,
               dont_guess=False, rank=True, freq=True, nbest=100):
    """Analyze the words in a set of files, writing the analyses to
    files whose names are the infile names with outpre prefixed to them.
    See anal_file for description of parameters."""
    language = get_language(language)
    if language:
        # Dict for saving analyses
        saved = {}
        for infile in infiles:
            outfile = infile + outsuff
            language.anal_file(infile, outfile, root=root, citation=citation, gram=gram,
                               pos=None, preproc=preproc, postproc=postproc,
                               nbest=nbest,
                               only_guess=guess, guess=not dont_guess,
                               raw=raw, saved=saved)

def anal_file(language, infile, outfile=None,
              root=True, citation=True, gram=True,
              preproc=True, postproc=True, guess=False, raw=False,
              dont_guess=False, sep_punc=True, lower_all=False,
              feats=None, simpfeats=None, word_sep='\n', sep_ident=False, minim=False,
              rank=True, freq=True, nbest=100,
              start=0, nlines=0):
    '''Analyze the words in a file, writing the analyses to outfile.

    @param infile:   path to a file to read the words from
    @param outfile:  path to a file where analyses are to be written
    @param root:     whether a root is to be included in the analyses
    @param citation: whether a citation form is to be included in the analyses
    @param gram:     whether a grammatical analysis is to be included
    @param preproc:  whether to preprocess inputs
    @param postproc: whether to postprocess outputs
    @param guess:    try only guesser analyzer
    @param dont_guess: try only lexical analyzer
    @param feats:    list of grammatical features to be printed out for each analysis
    @param simpfeats: dict of simplifications (FS->string) for recording FSs
    @param word_sep: character to separate words (unless minim is True)
    @param minim:    whether to print simplified descriptions of each word, separated
                     by spaces
    @param sep_ident: whether there are tab-separated identifiers in the source file
                     that should be maintained in the output
    @param rank:     whether to rank the analyses by the frequency of their roots
    @param freq:     whether to report frequencies of roots
    @param raw:      whether the analyses should be printed in "raw" form
    @param start:    line to start analyzing from
    @param nlines:   number of lines to analyze (if not 0)
    '''
    language = get_language(language)
    if language:
        language.anal_file(infile, outfile, root=root, citation=citation, gram=gram,
                           pos=None, preproc=preproc, postproc=postproc,
                           only_guess=guess, guess=not dont_guess, raw=raw, nbest=nbest,
                           sep_punc=sep_punc, feats=feats, simpfeats=simpfeats,
                           word_sep=word_sep, sep_ident=sep_ident, minim=minim,
                           lower_all=lower_all, start=start, nlines=nlines)

##def anal_gui(language, infile, outfile=None):
##    '''Open a window for reading in a file where words can be clicked for analysis.'''
##    language = get_language(language)
##    if language:
##        app = anal_gui.App(language, fname=infile)
##        app.MainLoop()

def gen(language, root, features=[], pos=None, guess=False, phon=False,
        roman=False, non_roman=True, interact=False, return_word=False):
    '''Generate a word, given stem/root and features (replacing those in default).
    If pos is specified, check only that POS; otherwise, try all in order until one succeeeds.

    @param root:     root or stem of a word
    @type  root:     string (roman)
    @param features: grammatical features to be added to default
    @type  features: string containing bracketed expression, e.g., '[sb=[+p1,+plr]]'
    @param pos:      part-of-speech: use only the generator for this POS
    @type  pos:      string
    @param guess:    whether to use guess generator if lexical generator fails
    @type  guess:    boolean
    @param roman:    whether the languages uses a roman script
    @type roman:      boolean
    @param non_roman: whether the language uses a non-roman script
    @type  non_roman: boolean
    @param return_word: whether to return the word, rather than printing it out
    @tyupe return_word: boolean
    '''
    language = get_language(language, segment=False, phon=phon)
    if language:
        is_not_roman = not roman and non_roman
        morf = language.morphology
        if pos:
            posmorph = morf[pos]
            output = posmorph.gen(root, update_feats=features, interact=interact,
                                  postproc=is_not_roman, guess=guess)
            if output:
                o = output[0][0]
                if return_word:
                    return o
                else:
                    print(o)
                    return
        else:
            for posmorph in list(morf.values()):
                output = posmorph.gen(root, update_feats=features, interact=interact,
                                      postproc=is_not_roman, guess=guess)
                if output:
                    o = output[0][0]
                    if return_word:
                        return o
                    else:
                        print(o)
                        return
        print("This word can't be generated!")

def phon_word(lang_abbrev, word, gram=False, raw=False,
              postproc=False, rank=True, nbest=100, freq=True,
              return_string=False):
    '''Convert a form in non-roman to roman, making explicit features that are missing in the orthography.
    @param lang_abbrev: abbreviation for a language
    @type  lang_abbrev: string
    @param word:     word to be analyzed
    @type  word:     string or unicode
    @param gram:     whether a grammatical analysis is to be included
    @type  gram:     boolean
    @param postproc: whether to run postpostprocess on the form
    @type  postproc: boolean
    @param rank:     whether to rank the analyses by the frequency of their roots
    @type  rank:     boolean
    @param nbest:    maximum number of analyses to return or print out
    @type  nbest:    int
    @param freq:     whether to report frequencies of roots
    @type  freq:     boolean
    @return:         a list of analyses
    @rtype:          list of (root, feature structure) pairs
    '''
    language = get_language(lang_abbrev, phon=True, segment=False)
    if language:
        return language.ortho2phon(word, gram=gram,
                                   report_freq=freq, nbest=nbest,
                                   postpostproc=postproc, rank=rank,
                                   raw=raw, return_string=return_string)

phon = phon_word

def phon_file(lang_abbrev, infile, outfile=None, gram=False,
              word_sep='\n', anal_sep=' ', print_ortho=True,
              postproc=False, rank=True, freq=True, nbest=100,
              start=0, nlines=0):
    '''Convert non-roman forms in file to roman, making explicit features that are missing in the orthography.
    @param lang_abbrev: abbreviation for a language
    @type  lang_abbrev: string
    @param infile:   path to a file to read the words from
    @type  infile:   string
    @param outfile:  path to a file where analyses are to be written
    @type  outfile:  string
    @param gram:     whether a grammatical analysis is to be included
    @type  gram:     boolean
    @param word_sep: separator between words (when gram=False)
    @type  word_sep: string
    @param anal_sep: separator between analyses (when gram=False)
    @type  anal_sep: string
    @param print_ortho: whether to print out orthographic form (when gram=False)
    @type  print_ortho: boolean
    @param postproc: whether to run postpostprocess on the form
    @type  postproc: boolean
    @param rank:     whether to rank the analyses by the frequency of their roots
    @type  rank:     boolean
    @param freq:     whether to report frequencies of roots
    @type  freq:     boolean
    @param nbest:    maximum number of analyses to return or print out for each word
    @type  nbest:    int
    @param start:    line to start analyzing from
    @type  start:    int
    @param nlines:   number of lines to analyze (if not 0)
    @type  nlines:   int
    '''
    language = get_language(lang_abbrev, phon=True, segment=False)
    if language:
        language.ortho2phon_file(infile, outfile=outfile, gram=gram,
                                 word_sep=word_sep, anal_sep=anal_sep, print_ortho=print_ortho,
                                 postpostproc=postproc, rank=rank, nbest=nbest,
                                 report_freq=freq,
                                 start=start, nlines=nlines)

def get_features(language, pos=None):
    '''Return a dict of features and their possible values for each pos.

    @param language:  abbreviation for a language
    @type  language:  string
    @param pos:       part-of-speech; if provided, return only
                      features for this POS
    @type  pos:       string
    @return:          dictionary of features and possible values; if
                      there is more than one POS, list of such
                      dictionaries.
    @rtype:           dictionary of feature (string): possible values (list)
                      pairs or list of (pos, dictionary) pairs
    '''
    language = get_language(language)
    if language:
        morf = language.morphology
        if pos:
            return morf[pos].get_features()
        elif len(morf) == 1:
            return list(morf.values())[0].get_features()
        else:
            feats = []
            for pos, posmorph in list(morf.items()):
                feats.append((pos, posmorph.get_features()))
            return feats

### Processing word count files.

def anal_word_counts(language, path, features, write=False):
    """Process a file consisting of a word and a count on each line, displaying only
    features in analysis. If write is True, write the results to a file (path with
    additional extension 'anl'). Otherwise return a list of results."""
    language = get_language(language)
    result = []
    if language:
        n = 0
        with open(path, encoding='utf8') as file:
            for line in file:
                n += 1
                word, count = line.split()
                anal = language.anal_word(word, display_feats=features)
                if not anal:
                    anal = word
                result.append("{} {}".format(anal, count))
                if n % 500 == 0:
                    print("Processed {} words".format(n))
        if write:
            with open(path + '.anl', 'w', encoding='utf8') as file:
                for line in result:
                    print(line, file=file)
        else:
            return result

### Functions for debugging and creating FSTs

def cascade(language, pos, gen=False, phon=False, segment=False, 
            verbose=False):
    '''Returns a cascade for the language and part-of-speech.
    @param language: abbreviation for a language, for example, 'gn'
    @type  language: string
    @param pos:    part-of-speech for the cascade, for example, 'v'
    @type  pos:    string
    @param phon:   whether the cascade is for phonology
    @type  phon:   boolean
    @param segment: whether the cascade is for segmentation
    @type  segment: boolean
    @param invert: whether to return the inverted cascade (for generation).
    @type  invert: boolean
    @param verbose: whether to print out various messages
    @type  verbose: boolean
    @return:       cascade for the the language and POS: a list of FSTs
    @rtype:        instance of the FSTCascade class (subclass of list)
    '''
    pos = get_pos(language, pos, phon=phon, segment=segment, load_morph=False, verbose=verbose)
    if not gen and pos.casc:
        return pos.casc
    if gen:
        if pos.casc_inv:
            return pos.casc_inv
        if pos.casc:
            casc_inv = pos.casc.inverted()
            pos.casc_inv = casc_inv
            return casc_inv
    pos.load_fst(True, create_fst=False, generate=gen, invert=gen, gen=gen,
                 segment=segment, verbose=verbose)
    if gen:
        return pos.casc_inv
    return pos.casc

def recompile(language, pos, phon=False, segment=False, gen=False, backwards=False,
              save=True, verbose=True):
    '''Recompiles the cascade FST for the language and part-of-speech.
    @param language: abbreviation for a language, for example, 'gn'
    @type  language: string
    @param pos:    part-of-speech for the cascade, for example, 'v'
    @type  pos:    string
    @param phon:   whether the cascade is for phonology
    @type  phon:   boolean
    @param segment: whether the cascade is for segmentation
    @type  segment: boolean
    @param gen:    whether to compile the cascade for generation (rather than analysis)
    @type  gen:    boolean
    @param backwards: whether to compile the FST from top (lexical) to bottom (surface)
                      for efficiency's sakd
    @type  backwards: boolean
    @param save:   whether to save the compiled cascade as an FST file
    @type  save:   boolean
    @param verbose: whether to print out various messages
    @type  verbose: boolean
    @return:       the POS morphology object
    @rtype:        instance of the POSMorphology class
    '''
    pos_morph = get_pos(language, pos, phon=phon, segment=segment, load_morph=False, verbose=verbose)
    fst = pos_morph.load_fst(True, segment=segment, generate=gen, invert=gen,
                             compose_backwards=backwards,
                             phon=phon, verbose=verbose)
    if not fst and gen == True:
        # Load analysis FST
        pos_morph.load_fst(True, verbose=True)
        # ... and invert it for generation FST
        pos_morph.load_fst(generate=True, invert=True, gen=True, verbose=verbose)
    if save:
        pos_morph.save_fst(generate=gen, segment=segment, phon=phon)
    return pos_morph

def test_fst(language, pos, string, gen=False, phon=False, segment=False,
             fst_label='', fst_index=0):
    """Test a individual FST within a cascade, identified by its label or its index,
    on the transduction of a string.
    @param language: abbreviation for a language, for example, 'gn'
    @type  language: string
    @param pos:    part-of-speech for the cascade, for example, 'v'
    @type  pos:    string
    @param phon:   whether the cascade is for phonology
    @type  phon:   boolean
    @param segment: whether the cascade is for segmentation
    @type  segment: boolean
    @param gen:     whether to use the inverted cascade (for generation).
    @type  gen:     boolean
    @param verbose: whether to print out various messages
    @type  verbose: boolean
    @return:       a list of analyses, each a list consisting of a root and a feature-structure set
    @rtype:        list of lists, each of the form [str, FSSet]
    """
    casc = cascade(language, pos, gen=gen, phon=phon, segment=segment)
    if not casc:
        print('No cascade found')
        return
    return casc.transduce1(string, fst_label=fst_label, fst_index=fst_index)

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
    load_lang(abbrev, segment=segment, phon=phon, load_morph=load_morph,
              guess=guess, verbose=verbose)
    lang = get_language(abbrev, phon=phon, segment=segment, load=load_morph,
                        verbose=verbose)
    if lang:
        return lang.morphology[pos]

# Import views. This has to appear after the app is created.
import morfo.views
