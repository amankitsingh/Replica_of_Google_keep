from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import httplib2
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker

from database import Base, todolist, todotextlist, todolinknote

app = Flask(__name__)

####### Database#######
engine = create_engine('sqlite:///todo.db',
                       connect_args={'check_same_thread': False})

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

###### Route when nothing is specified in the url######
@app.route('/keep')
@app.route('/')
def index():
    todotext = session.query(todotextlist).all()
    todolists = session.query(todolist).all()
    todolinks = session.query(todolinknote).all()
    ###### Makes to stay on the same home page######
    return render_template('main.html', todo=todotext, todolist=todolists, todolink=todolinks)

###### Adding items######
@app.route('/addtextnote', methods=['POST'])
def addtextnote():
    if request.method == 'POST':
        message = request.form['data']
        newnote = todotextlist(text=message)
        session.add(newnote)
        session.commit()
    return render_template('main.html')


@app.route('/addlistnote', methods=['POST'])
def addlistnote():
    if request.method == 'POST':
        msg = request.form['data']
        newtextnote = todolist(text=msg, complete=False)
        session.add(newtextnote)
        session.commit()
    return


@app.route('/addlinknote', methods=['POST'])
def addlinknote():
    if request.method == 'POST':
        message = request.form['url']
        print(message)
        title = request.form['title']
        newnote = todolinknote(title=title, link=message)
        session.add(newnote)
        session.commit()
    return render_template('main.html')


@app.route('/complete/<int:id>')
def complete(id):
    todo = session.query(todotextlist).filter_by(id=int(id)).first()
    todo.complete = True
    session.commit()
    ###### Makes to stay on the same home page######
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.run(debug=True, host='0.0.0.0', port=8000)
