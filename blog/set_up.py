"""Functions for helping set up blog.
"""

from werkzeug.security import generate_password_hash

from models import Base, User, Post

def init_database(env):
    """Creates all the tables in the database.
    """
    Base.metadata.create_all(env.database_engine)

def populate_test_data(env):
    """Creates test data in the database.
    """
    session = env.create_database_session()
    me = User(username=u"rob", first_name=u"Rob", last_name=u"Berry", \
                  password=unicode(generate_password_hash("password")))
    test_post = Post(title=u"Test post!", body=u"This is a test post :D", \
                         author=me)
    session.add(me)
    session.add(test_post)
    session.commit()
