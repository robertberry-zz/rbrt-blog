"""
Quick blog.
"""

__author__ = "Robert Berry"
__email__ = "rjberry@gmail.com"



from flask import Flask, url_for, render_template

from blog.models import User, Post
from blog.environment import Environment

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/post/<id>")
def post(post_id):
    pass

if __name__ == "__main__":
    app.run(debug=True)

