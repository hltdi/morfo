"""
This file is part of morfo, which is a project of PLoGS.

Copyleft 2018, PLoGS and Michael Gasser.

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

# Created 2018.9.14

# Sessions with a user (possibly None) interacting with morfo in the web app.
"""

import datetime, sys, os, yaml
from werkzeug.security import generate_password_hash, check_password_hash

class Session:

    directory = os.path.join(os.path.dirname(__file__), 'sessions')

    def __init__(self, language, user=None):
        self.language = language
        self.user = user

    def __repr__(self):
        return ">>{}<<".format(self.language.abbrev)

class User:
    """User of the system who is registered and whose feedback is saved."""

    # Dictionary of users, with usernames as keys.
    users = {}
    # Dictionary of users created during the most recent session, with usernames as keys.
    new_users = {}

    # Special anonymous user
    anon_user = 'anon'
    anon_pw = 'sin_nombre'
    anon_name = 'anónima'
    anon_email = 'gasser@indiana.edu'

    prefix = "{U}"
    file = "users"

    def __init__(self, username='', email='', password='', name='', level=1, pw_hash='',
                 creation=None, nsessions=0, nprocs=0, update=None, score=0.0,
                 new=False):
        """name and level are optional. Other fields are required."""
        self.username = username
        self.email = email
        # Guarani ability
        self.level = level
        self.name = name
        self.creation = creation if creation else User.time()
        if pw_hash:
            self.pw_hash = pw_hash
        else:
            self.set_password(password)
        # Initial values to be updated later
        self.nsessions = nsessions
        self.nprocs = nprocs
        # Time data last updated
        self.update = update or self.creation
        # Score based on evaluation of translations
        self.score = score
        # Add to dict of all users
        User.users[self.username] = self
        # If this is a new user, save it here so it can be written to all.usr at the end
        # of the session.
        if new:
            User.new_users[self.username] = self

    def __repr__(self):
        return "{}::{}".format(USER.prefix, self.username)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
#        print("Checking password {} with hash {}".format(password, self.pw_hash))
        res = check_password_hash(self.pw_hash, password)
#        print("Result {}".format(res))
        return res

    def add_user(self):
        User.users[self.username] = self

    @staticmethod
    def time():
        time = get_time()
        return time.strftime(SHORT_TIME_FORMAT)

    @staticmethod
    def from_file(username):
        path = User.get_path(username)
        with open(path, encoding='utf8') as file:
            d = yaml.load(file)
            u = User.dict2user(d, new=False)
        return u

    def user2dict(self):
        """Create a dictionary of user properties."""
        d = {}
        d['username'] = self.username
        d['level'] = self.level
        d['name'] = self.name
        d['email'] = self.email
        d['creation'] = self.creation
        d['update'] = self.update
        d['nsentences'] = self.nsentences
        d['nsessions'] = self.nsessions
        d['score'] = self.score
        d['pw_hash'] = self.pw_hash
        return d

    @staticmethod
    def dict2user(dct, new=True):
        level = dct.get('level', 1)
#        if isinstance(level, str):
#            level = int(level)
        return User(username=dct.get('username', ''),
                    password=dct.get('password', ''),
                    pw_hash=dct.get('pw_hash'),
                    email=dct.get('email', ''),
                    name=dct.get('name', ''),
                    creation=dct.get('creation'),
                    update=dct.get('update'),
                    nsentences=dct.get('nsentences', 0),
                    nsessions=dct.get('nsessions', 0),
                    score=dct.get('score', 0.0),
                    level=level,
                    new=new)

    @staticmethod
    def get_user(username):
       return User.users.get(username)

    def write(self, file=sys.stdout):
        print("{};{};{};{};{}".format(self.username, self.pw_hash, self.email, self.name, self.level), file=file)

    @staticmethod
    def get_users_path():
        return os.path.join(Session.directory, User.file)

    def get_session_path(self):
        name = self.username + '.sess'
        return os.path.join(Session.directory, name)

    def read_sessions(self):
        """Read in the sessions file for this user, returning a list of session dicts."""
        path = self.get_session_path()
        # catch?
        return yaml.load(open(path, encoding="utf8"))

    @staticmethod
    def get_path(username):
        # File where the user's data is stored
        filename = "{}.usr".format(username)
        return os.path.join(Sessions.directory, filename)

    @staticmethod
    def read_all():
        """Read in current users from all.usr, adding them to User.users."""
        with open(User.get_users_path(), encoding='utf8') as file:
            for line in file:
                username, pw_hash, email, name, level = line.strip().split(';')
                level = int(level)
                user = User.from_file(username)
#                userfile = User.get_path()
#                user = User(username=username, pw_hash=pw_hash, email=email, name=name, level=level,
#                            new=False)
                User.users[username] = user

    @staticmethod
    def write_new():
        """Enter all new users (normally at most one) in the users file.
        Create a user file for each new user.
        """
        if User.new_users:
            print("Creando nuevos usuarios {}".format(User.new_users))
            with open(User.get_users_path(), 'a', encoding='utf8') as file:
                for username, user in User.new_users.items():
                    print("  Usuario {}".format(user))
                    user.create_user_file()
                    user.write(file=file)

    def create_user_file(self):
        """Create user file with basic data about the user (to be changed later)."""
        d = self.user2dict()
        with open(User.get_path(self.username), 'w', encoding='utf8') as file:
            yaml.dump(d, file, default_flow_style=False)

    @staticmethod
    def get_user(username):
        return User.users.get(username)

    @staticmethod
    def get_anon():
        """Get the anonymous user; if it doesn't exist, create it."""
        anon = User.get_user(User.anon_user)
        if not anon:
            anon = User(username=User.anon_user, email=User.anon_email, password=User.anon_pw, name=User.anon_name, new=True)
        return anon

    

