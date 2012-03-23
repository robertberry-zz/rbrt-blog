"""
Quick blog.
"""

__author__ = "Robert Berry"
__email__ = "rjberry@gmail.com"

from flask import Flask, url_for, render_template

from blog.models import User, Post
from blog.environment import Environment

CONFIG_PATH = "config.yml"
POSTS_PER_PAGE = 20

app = Flask(__name__)

@app.before_request:
def before_request():
    g.env = Environment(CONFIG_PATH)
    g.session = g.env.create_database_session()

@app.teardown_request:
def teardown_request():
    g.session.close()

@app.route("/")
def index():
    posts = g.session.query(Post).join(User).order_by(Post.created) \
        .limit(POSTS_PER_PAGE)
    return render_template('index.html', posts=posts)

@app.route("/post/<id>")
def post(post_id):
    post = g.session.query(Post).filter_by(Post.id == int(post_id)).one()
    return render_template('post.html', post=post)

if __name__ == "__main__":
    app.run(debug=True)

