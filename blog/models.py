"""
Models.
"""

import sqlalchemy

from sqlalchemy import Column, Integer, Unicode, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship, backref
from sqlalchemy import func

from flask import url_for

Base = declarative_base()

class Defaults(object):
    @declared_attr
    def __tablename__(cls):
        # fairly dumb way of getting plural form of class name
        return cls.__name__.lower() + "s"

    # id is always this
    id = Column("id", Integer, primary_key=True)

class Post(Base, Defaults):
    author_id = Column("author_id", Integer, ForeignKey("users.id"))
    title = Column("title", Unicode)
    body = Column("body", Unicode)
    created = Column("created", DateTime, default=func.now())
    modified = Column("modified", DateTime, default=func.now())

    author = relationship("User", backref=backref("posts", order_by=created))

    @property
    def url(self):
        return url_for('post', id=self.id)

class User(Base, Defaults):
    user_name = Column("user_name", Unicode)
    first_name = Column("first_name", Unicode)
    last_name = Column("last_name", Unicode)

    @property
    def full_name(self):
        return u"%s %s" % (self.first_name, self.last_name)
