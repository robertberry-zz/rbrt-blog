"""
Quick blog.
"""

__author__ = "Robert Berry"
__email__ = "rjberry@gmail.com"

from optparse import OptionParser

from flask import Flask, url_for, render_template, g

from blog.models import User, Post, Base
from blog.environment import Environment

CONFIG_PATH = "config.yml"
POSTS_PER_PAGE = 20

app = Flask(__name__)

def init_database():
    """Creates all the tables in the database.
    """
    env = Environment(CONFIG_PATH)
    Base.metadata.create_all(env.database_engine)

def populate_test_data():
    """Creates test data in the database.
    """
    env = Environment(CONFIG_PATH)
    session = env.create_database_session()
    me = User(user_name=u"rob", first_name=u"Rob", last_name=u"Berry")
    test_post = Post(title=u"Test post!", body=u"This is a test post :D", \
                         author=me)
    session.add(me)
    session.add(test_post)
    session.commit()

@app.before_request
def before_request():
    g.env = Environment(CONFIG_PATH)
    g.session = g.env.create_database_session()

@app.teardown_request
def teardown_request(a):
    g.session.close()

@app.route("/")
def index():
    posts = g.session.query(Post).join(User).order_by(Post.created) \
        .limit(POSTS_PER_PAGE)
    return render_template('index.html', posts=posts)

@app.route("/post/<id>/")
def post(id):
    post = g.session.query(Post).filter(Post.id == int(id)).one()
    return render_template('post.html', post=post)

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-i", "--init-database", dest="init_database", \
                          help="Set up database structure.", default=False)
    (options, args) = parser.parse_args()

    if (options.init_database):
        init_database()
        populate_test_data()
    else:
        app.run(debug=True)

