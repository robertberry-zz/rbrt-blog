"""
Quick blog.
"""

__author__ = "Robert Berry"
__email__ = "rjberry@gmail.com"

from optparse import OptionParser

from flask import Flask, url_for, render_template, g, redirect, session, request

from sqlalchemy.orm.exc import NoResultFound

from werkzeug.security import check_password_hash

from blog.models import User, Post
from blog.environment import Environment
from blog.set_up import init_database, populate_test_data
from blog.utils import login_required

CONFIG_PATH = "config.yml"
POSTS_PER_PAGE = 20

app = Flask(__name__)
env = Environment(CONFIG_PATH)

app.secret_key = "4xfaExc0xf8nxbdxb2" #env.config['secret_key']

@app.before_request
def before_request():
    g.env = env
    g.session = g.env.create_database_session()

    try:
        user_id = session["user_id"]
        g.user = g.session.query(User).filter(User.id == user_id).one()
    except KeyError:
        g.user = None
    except NoResultFound:
        # log the error here? user id was invalid in session.
        g.user = None

@app.teardown_request
def teardown_request(a):
    g.session.close()

@app.route("/")
def index():
    posts = g.session.query(Post).join(User).order_by(Post.created) \
        .limit(POSTS_PER_PAGE)
    return render_template('index.html', posts=posts)

@app.route("/post/", methods=["GET", "POST"])
@login_required
def new_post():
    errors = []
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        if not title:
            errors.append("You must supply a title.")
        if not body:
            errors.append("Post may not be empty.")
        if not errors:
            post = Post(title=title, body=body, author=g.user)
            g.session.add(post)
            g.session.commit()
            return redirect(post.url)
    else:
        return render_template('new_post.html', errors=errors)

@app.route("/post/<id>/")
def post(id):
    post = g.session.query(Post).filter(Post.id == int(id)).one()
    return render_template('post.html', post=post)

@app.route("/login/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        try:
            username = request.form["username"]
            password = request.form["password"]
            # do the log in
            try:
                user = g.session.query(User).filter(User.username == username) \
                    .one()
                if check_password_hash(user.password, password):
                    session['user_id'] = user.id
                    return redirect(request.args.get('next', url_for('index')))
                else:
                    error = "Incorrect password"
            except NoResultFound:
                error = "No user called '%s'" % username
        except KeyError:
            error = "Please supply both username and password"
    return render_template('login.html', error=error)

@app.route("/logout/", methods=["GET", "POST"])
def logout():
    session["user_id"] = None
    return redirect(url_for("index"))

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-i", "--init-database", dest="init_database", \
                          help="Set up database structure.", default=False)
    (options, args) = parser.parse_args()

    if (options.init_database):
        init_database(env)
        populate_test_data(env)
    else:
        app.run(debug=True)
