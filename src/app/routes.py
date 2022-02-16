from flask import render_template, request, send_file, redirect, url_for, g
from app import webapp
from app.db_connection import get_db
from app.image_utils import save_image
import requests
import time
import datetime

update_time = time.ctime(time.time())

@webapp.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@webapp.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@webapp.route('/')
@webapp.route('/home')
def home():
    return render_template("home.html")

@webapp.route('/add_key', methods = ['GET','POST'])
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
        jsonReq={"keyReq":key}
        res= requests.post('http://localhost:5001/get', json=jsonReq)
        if(res.text=='Unknown key'):#res.text is the file path of the image from the memcache
            #get from db and update memcache
            cnx = get_db()
            cursor = cnx.cursor(buffered=True)
            query = "SELECT image_tag FROM image_table where image_key= %s"
            cursor.execute(query, (key,))
            if(cursor._rowcount):# if key exists in db
                image_tag=str(cursor.fetchone()[0]) #cursor[0] is the imagetag recieved from the db
                #close the db connection
                cnx.close()

                #put into memcache
                filename=image_tag
                jsonReq = {key:filename}
                res = requests.post('http://localhost:5001/put', json=jsonReq)
                return render_template('show_image.html', exists=True, filename=filename)
            else:#the key is not found in the db
                return render_template('show_image.html', exists=False, filename="does not exist")

        else:# the key was found in memcache
            print("memcache response is:", res.text)
            return render_template('show_image.html', exists=True, filename=res.text)
    return render_template('show_image.html')

# this endpoint just returns the image. The key is the filename with extension
@webapp.route("/get_image/<filename>")
def get_image(filename):
    filepath = "static/images/" + filename
    return send_file(filepath)

@webapp.route('/key_store')
def key_store():
    cnx = get_db()
    cursor = cnx.cursor()
    query = "SELECT image_key FROM image_table"
    cursor.execute(query)
    keys = [] #will recieve keys from either memcache or db
    for key in cursor:
        keys.append(key[0])
    total=len(keys)
    
    #close db connection
    cnx.close()

    if keys:
        return render_template('key_store.html', keys=keys, total=total)
    else:
        return render_template('key_store.html')


@webapp.route('/memcache_params', methods = ['GET','POST'])
def memcache_params():
    # TODO: Add in a DB call to get base values
    global update_time
    capacity = "100MB"
    replacement_policy = "LRU" 
    date = datetime.datetime.strptime(update_time, "%a %b %d %H:%M:%S %Y")
    date.strftime("YYYY/MM/DD HH:mm:ss (%Y%m%d %H:%M:%S)")

    if request.method == 'POST':
        print(request.form)
        if not request.form.get("clear_cache") == None:
            requests.post('http://localhost:5001/clear')
            return render_template('memcache_params.html', capacity=capacity, replacement_policy=replacement_policy, update_time=date)
        else:
            new_cap = request.form.get('capacity')
            if not new_cap == "":
                capacity = new_cap
            replacement_policy = request.form.get('replacement_policy')
            update_time = time.ctime(time.time())
            date = datetime.datetime.strptime(update_time, "%a %b %d %H:%M:%S %Y")
            date.strftime("YYYY/MM/DD HH:mm:ss (%Y%m%d %H:%M:%S)")
            return render_template('memcache_params.html', capacity=capacity, replacement_policy=replacement_policy, update_time=date)
    return render_template('memcache_params.html', capacity=capacity, replacement_policy=replacement_policy, update_time=date)
