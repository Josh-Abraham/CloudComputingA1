from flask import render_template, url_for, request, send_file
from app import webapp

@webapp.route('/show_image', methods = ['GET','POST'])
def show_image():
    if request.method == 'POST':
        key = request.form.get('key')
        return render_template('show_image.html', key=key)
    return render_template('show_image.html')

# this endpoint just returns the image. The key is the filename with extension
@webapp.route("/get_image/<key>")
def get_image(key):
    filepath = "static/images/" + key
    return send_file(filepath)
