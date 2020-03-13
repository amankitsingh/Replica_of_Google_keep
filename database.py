from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

### table for user ###


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

### table for text note ###


class todotextlist(Base):
    __tablename__ = 'todotextlist'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User)

### table for list note ###


class todolist(Base):
    __tablename__ = 'todolist'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String(250), nullable=False)
    complete = Column(Boolean)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User)

### table for link note ###


class todolinknote(Base):
    __tablename__ = 'todolinknote'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(250), nullable=False)
    link = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User)

### table for map note ###


class todomapnote(Base):
    __tablename__ = 'todomapnote'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(250), nullable=False)
    location = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User)


engine = create_engine('sqlite:///todo.db')
Base.metadata.create_all(engine)
