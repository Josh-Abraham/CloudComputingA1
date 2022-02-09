from flask import render_template, request, send_file
from app import webapp, UPLOAD_FOLDER
import os, requests, json


@webapp.route('/')
@webapp.route('/home')
def home():
    return render_template("home.html")

@webapp.route('/addKey', methods = ['GET','POST'])
def add_key():
    if request.method == 'POST':
        key = request.form.get('key')
        status = save_image(request, key)
        return render_template("add_key.html", save_status=status)
    return render_template("add_key.html")

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


def save_image(request, key):
    img_url = request.form.get('img_url')
    if img_url == "":
        file = request.files['img_file']
        _, extension = os.path.splitext(file.filename)
        filename = key + extension
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        jsonReq = {key:filename}
        res = requests.post('http://localhost:5001/put', json=jsonReq)
        return str(res.json())
    
    try:
        response = requests.get(img_url)
        if response.status_code == 200:
            _, extension = os.path.splitext(img_url)
            filename = key + extension
            with open(UPLOAD_FOLDER + "/" + filename, 'wb') as f:
                f.write(response.content)
            jsonReq = {key:filename}
            res = requests.post('http://localhost:5001/put', json=jsonReq)
            return str(res.json())
        return "INVALID"
    except:
        return "INVALID"