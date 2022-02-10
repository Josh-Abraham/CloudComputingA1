
from flask import render_template, url_for
from app import webapp


@webapp.route('/')
@webapp.route('/home')
def home():
    return render_template("home.html")
