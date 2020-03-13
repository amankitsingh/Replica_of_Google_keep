from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import httplib2
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database import Base, User, todolist, todotextlist, todolinknote, todomapnote
# Import Login session
from flask import session as login_session
import random
import string

# imports for gconnect
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

# import login decorator
from functools import wraps

app = Flask(__name__)

####### Database#######
engine = create_engine('sqlite:///todo.db',
                       connect_args={'check_same_thread': False})

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

CLIENT_ID = json.loads(
    open('client_secret.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Replica of Google Keep"


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_name' not in login_session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function


@app.route('/login')
def showlogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(0, 32))
    login_session['state'] = state

    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Gathers data from Google Sign In API and
    # places it inside a session variable.
    # validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(
            json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application-json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # upgrade the authorization code in credentials object
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code'), 401)
        response.headers['Content-Type'] = 'application-json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1].decode("utf-8"))
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Access token within the app
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    response = make_response(
        json.dumps("successfully connected user"), 401)

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    login_session['provider'] = 'google'
    login_session['username'] = data['name']
    login_session['email'] = data['email']

    # See if user exists or if it doesn't make a new one
    print('User email is'+str(login_session['email']))
    user_id = getUserID(login_session['email'])
    if user_id:
        print('Existing user#'+str(user_id)+'matches this email')
    else:
        user_id = createUser(login_session)
        print('New user_id#'+str(user_id)+'created')
    login_session['user_id'] = user_id
    print('Login session is tied to :id#'+str(login_session['user_id']))

    output = ''
    output += '<h1 style="text-align:center;">Welcome,</br> '
    output += login_session['username']
    output += '!</h1>'
    print("done!")
    return output


# Helper Functions
def createUser(login_session):
    newUser = User(
        name=login_session['username'], email=login_session['email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).first()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).first()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).first()
        return user.id
    except:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session.
@app.route('/gdisconnect')
def gdisconnect():
    # only disconnect a connected User
    access_token = login_session.get('access_token')
    print('In gdisconnect access token is %s', access_token)
    print('User name is: %s', login_session['username'])
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    df = 'https://'
    url = df+'accounts.google.com/o/oauth2/revoke?token=%s' % login_session
    ['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
            json.dumps("Failed to revoke token for given user."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/logout')
def logout():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['user_id']
        del login_session['provider']
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


###### Route when nothing is specified in the url######
@app.route('/keep')
@app.route('/')
def index():
    if 'username' not in login_session:
        return redirect('/login')
    todotext = session.query(todotextlist).filter_by(
        user_id=login_session['user_id']).all()
    todolists = session.query(todolist).filter_by(
        user_id=login_session['user_id']).all()
    todolinks = session.query(todolinknote).filter_by(
        user_id=login_session['user_id']).all()
    todomaplinks = session.query(todomapnote).filter_by(
        user_id=login_session['user_id']).all()
    ###### Makes to stay on the same home page######
    return render_template('main.html', todo=todotext, todolist=todolists, todolink=todolinks, todomap=todomaplinks)


###### Adding items######
@app.route('/addtextnote', methods=['POST'])
def addtextnote():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        message = request.form['data']
        newnote = todotextlist(text=message,  user_id=login_session['user_id'])
        session.add(newnote)
        session.commit()
    return render_template('main.html')


@app.route('/addlistnote', methods=['POST'])
def addlistnote():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        msg = request.form['data']
        newtextnote = todolist(
            text=msg, complete=False, user_id=login_session['user_id'])
        session.add(newtextnote)
        session.commit()
    return


@app.route('/addlinknote', methods=['POST'])
def addlinknote():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        message = request.form['url']
        print(message)
        title = request.form['title']
        newnote = todolinknote(title=title, link=message,
                               user_id=login_session['user_id'])
        session.add(newnote)
        session.commit()
    return render_template('main.html')


@app.route('/addmapnote', methods=['POST'])
def addmapnote():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        title = request.form['title']
        loc = request.form['location']
        newmapnote = todomapnote(
            title=title, location=loc, user_id=login_session['user_id'])
        session.add(newmapnote)
        session.commit()
    return redirect('/keep')


@app.route('/deletetextnote/<int:text>')
def deletetextnote(text):
    if 'username' not in login_session:
        return redirect('/login')
    textToDelete = session.query(
        todotextlist).filter_by(id=text).one()
    session.delete(textToDelete)
    session.commit()
    return redirect('/keep')


@app.route('/deletemapnote/<int:text>')
def deletemapnote(text):
    if 'username' not in login_session:
        return redirect('/login')
    textToDelete = session.query(
        todomapnote).filter_by(id=text).one()
    session.delete(textToDelete)
    session.commit()
    return redirect('/keep')


@app.route('/deletelinknote/<int:link>')
def deletelinknote(link):
    if 'username' not in login_session:
        return redirect('/login')
    linkToDelete = session.query(
        todolinknote).filter_by(id=link).one()
    session.delete(linkToDelete)
    session.commit()
    return redirect('/keep')


@app.route('/complete/<int:id>')
def complete(id):
    if 'username' not in login_session:
        return redirect('/login')
    todo = session.query(todotextlist).filter_by(id=int(id)).first()
    todo.complete = True
    session.commit()
    ###### Makes to stay on the same home page######
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.run(debug=True, host='0.0.0.0', port=8000)
