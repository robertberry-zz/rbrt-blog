"""
Models.
"""

import sqlalchemy

from sqlalchemy import Column, Integer, Unicode, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class Post(Base):

    __tablename__ = "posts"

    id = Column("id", Integer, primary_key=True)
    author_id = Column("author_id", Integer, ForeignKey("users.id"))
    title = Column("title", Unicode)
    body = Column("body", Unicode)
    created = Column("created", DateTime)
    modified = Column("modified", DateTime)

    author = relationship("User", backref=backref("posts", order_by=created))

class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True)
    user_name = Column("user_name", Unicode)
    first_name = Column("first_name", Unicode)
    last_name = Column("last_name", Unicode)

    
