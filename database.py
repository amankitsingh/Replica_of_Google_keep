from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class todotextlist(Base):
    __tablename__ = 'todotextlist'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String(250), nullable=False)


class todolist(Base):
    __tablename__ = 'todolist'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String(250), nullable=False)
    complete = Column(Boolean)


class todolinknote(Base):
    __tablename__ = 'todolinknote'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(250), nullable=False)
    link = Column(String(250), nullable=False)


engine = create_engine('sqlite:///todo.db')
Base.metadata.create_all(engine)
