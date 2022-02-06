from flask import render_template
from app import webapp

@webapp.route('/key_store')
def key_store():
    keys = [0, 1, 2, 3, 4]
    total=len(keys)
    return render_template('key_store.html', title='Home', keys=keys, total=total)
