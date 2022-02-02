
from flask import render_template, url_for
from app import webapp


@webapp.route('/addKey')
def add_key():
    return render_template("add_key.html")
    

