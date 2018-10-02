#   morfo.
#
########################################################################
#
#   This file is part of morfo: morphological analysis and generation.
#
#   Copyleft 2018 PLoGS <gasser@indiana.edu>
#   
#   This program is free software: you can redistribute it and/or
#   modify it under the terms of the GNU General Public License as
#   published by the Free Software Foundation, either version 3 of
#   the License, or (at your option) any later version.
#   
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU General Public License for more details.
#   
#   You should have received a copy of the GNU General Public License
#   along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# =========================================================================
#
# Created 2018.9.11

from flask import request, session, g, redirect, url_for, abort, render_template, flash
from morfo import app, exit, load, anal_word, seg, gen, init_session

# Global variables for views; probably a better way to do this...
LANGUAGE = ANALYSES = USER = WORD = SESSION = None
USERS_INITIALIZED = False
ANAL_INDEX = 0
# Abbreviations of languages already loaded
LOADED = []

def init_word():
    ANALYSES = WORD = None
    ANAL_INDEX = 0

#def load_language(abbrev):
#    global LOADED
#    LOADED.append(abbrev)
#    load(abbrev)

def analyze():
    """Returns a list of dicts of features and values."""
    global ANALYSES
    ANALYSES = anal_word(LANGUAGE.abbrev, WORD, web=True)

@app.route('/')
def index():
    print("In index...")
    return redirect(url_for('base'))

@app.route('/base', methods=['GET', 'POST'])
def base():
    global SESSION
    global LANGUAGE
    global LOADED
    form = request.form
    print("base form: {}".format(form))
    if 'labrev' in form:
        lg_abbrev = form.get('labrev')
        SESSION = init_session(lg_abbrev, user=USER)
        LANGUAGE = SESSION.language
#        loaded = lg_abbrev in LOADED
#        LOADED.append(lg_abbrev)
        print("new session with {}".format(LANGUAGE))
        return render_template('anal.html', language=LANGUAGE, webdata=LANGUAGE.webdata,
                               labrev=lg_abbrev)
    return render_template('base.html')

@app.route('/acerca', methods=['GET', 'POST'])
def acerca():
    print("In acerca...")
    return render_template('acerca.html', language=LANGUAGE)

@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    return render_template('contacto.html', language=LANGUAGE)

# Work on this later.
@app.route('/login', methods=['GET', 'POST'])
def login():
    global USER
    form = request.form
#    print("Form for login: {}".format(form))
    if not USERS_INITIALIZED:
        initialize()
    if request.method == 'POST' and 'login' in form:
        # Try to find user with username username
        username = form.get('username')
        user = get_user(username)
        if not user:
            print("No such user as {}".format(username))
            return render_template('login.html', error='user', language=LANGUAGE)
        else:
            print("Found user {}".format(user))
            password = form.get('password')
            if user.check_password(password):
                USER = user
                return render_template('logged.html', user=username, language=LANGUAGE)
            else:
#                print("Password doesn't match")
                return render_template('login.html', error='password')
    return render_template('login.html', language=LANGUAGE)

@app.route('/logged', methods=['GET', 'POST'])
def logged():
    form = request.form
#    print("Form for logged: {}".format(form))
    return render_template('logged.html', language=LANGUAGE)

@app.route('/reg', methods=['GET', 'POST'])
def reg():
    global USER
    form = request.form
#    print("Form for reg: {}".format(form))
    if request.method == 'POST' and 'username' in form:
        if form.get('cancel') == 'Cancelar':
            return render_template('login.html')
        elif not form.get('username'):
            return render_template('reg.html', error="username", language=LANGUAGE)
        elif not form.get('email'):
            return render_template('reg.html', error="email", language=LANGUAGE)
        elif form.get('password') != form.get('password2'):
            return render_template('reg.html', error="password", language=LANGUAGE)
        else:
            user = create_user(form)
            print("Created user {}".format(user))
            USER = user
            return render_template('acct.html', user=form.get('username'), language=LANGUAGE)
    return render_template('reg.html', language=LANGUAGE)

@app.route('/acct', methods=['POST'])
def acct():
#    print("In acct...")
    return render_template('acct.html', language=LANGUAGE)

# View for quick version of program that displays sentence and its translation in
# side-by-side windows.
@app.route('/anal', methods=['GET', 'POST'])
def anal():
    global WORD
    global SESSION
    global LANGUAGE
    global ANAL_INDEX
    global ANALYSES
    form = request.form
    ultanal = False
    print("Form for anal: {}".format(form))
    webdata = []
    lg_abbrev = form.get('labrev')
    current_lg_abbrev = None
    if LANGUAGE:
        current_lg_abbrev = LANGUAGE.abbrev
        if lg_abbrev and current_lg_abbrev != lg_abbrev:
            print("Changing language...")
            SESSION = init_session(lg_abbrev, user=USER)
            LANGUAGE = SESSION.language
            ANALYSES = WORD = None
            ANAL_INDEX = 0
        webdata = LANGUAGE.webdata
#    print("Form abbrev {}, current abbrev {}".format(lg_abbrev, current_lg_abbrev))
    if not SESSION:
#        print("Creating session for {}".format(lg_abbrev))
        SESSION = init_session(lg_abbrev, user=USER)
        LANGUAGE = SESSION.language
    username = USER.username if USER else ''
#   AYUDA
#    if 'ayuda' in form and form['ayuda'] == 'true':
#        # Opened help window. Keep everything else as is.
#        raw = SENTENCE.raw if SENTENCE else None
#        document = form.get('UanalDoc', '')
#        return render_template('sent.html', sentence=SEG_HTML, raw=raw, punc=punc,
#                               document=document, user=USER)
    if form.get('borrar') == 'true':
        print("BORRAR")
        ANALYSES = WORD = None
        ANAL_INDEX = 0
#        init_word()
        print("erased...")
        return render_template('anal.html', palabra=None, user=username, analindex=0,
                               language=LANGUAGE, labrev=lg_abbrev, analysis=None,
                               ultanal=ultanal, webdata=webdata)
    if not 'palabra' in form:
        print("no word...")
        return render_template('anal.html', palabra=None, language=LANGUAGE, analysis=None,
                               labrev=lg_abbrev, webdata=webdata, ultanal=ultanal)
    if not WORD:
        # Get the word
        WORD = form['palabra']
        print("WORD: {}".format(WORD))
        analyze()
        if not ANALYSES:
            # This should behave like 'borrar'
            ultanal = True
            ANAL_INDEX = 0
            print("no analyses...")
            return render_template('anal.html', error=True, user=username, labrev=lg_abbrev, webdata=webdata,
                                   analindex=ANAL_INDEX, ultanal=True)
    print("Analyses {}".format(ANALYSES))
    # This shouldn't be needed...
    if ANAL_INDEX >= len(ANALYSES):
        print("no more analyses...")
        return render_template('anal.html', palabra=WORD, user=username, language=LANGUAGE, labrev=lg_abbrev,
                               analysis=None, ultanal=True, webdata=webdata)
    analysis = ANALYSES[ANAL_INDEX]
    webindex = LANGUAGE.anal_get_webindex(analysis)
    ANAL_INDEX += 1
    print("Analysis {}: {}".format(ANAL_INDEX, analysis))
    html = LANGUAGE.anal2html(analysis)
    print("HTML: {}".format(html))
    if ANAL_INDEX == len(ANALYSES):
        ultanal = True
        print("Final analysis")
    print("analysis...")
    return render_template('anal.html', palabra=WORD, user=username, analindex=ANAL_INDEX,
                           language=LANGUAGE, labrev=lg_abbrev, borrar=False, ultanal=ultanal,
                           analysis=analysis, webdata=webdata, webindex=webindex, html=html)

@app.route('/fin', methods=['GET', 'POST'])
def fin():
    form = request.form
#    print("Form for fin: {}".format(form))
    modo = form.get('modo')
    global LANGUAGE
    global SESSION
    global WORD
    global USER
    global ANAL_INDEX
    exit(SESSION)
    LANGUAGE = SESSION = USER = None
    ANAL_INDEX = 0
    return render_template('fin.html', modo=modo, language=LANGUAGE)

@app.route('/proyecto')
def proyecto():
    return render_template('proyecto.html', language=LANGUAGE)

# Not needed because this is in runserver.py.
if __name__ == "__main__":
    morfo.app.run(host='0.0.0.0')
