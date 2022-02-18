from flask import render_template, request, send_file, redirect, url_for, g, jsonify
from app import webapp
from app.db_connection import get_db
from app.image_utils import save_image, write_image_base64
import requests, time, datetime
from app.cache_utils import *
import app.config as conf

cache_host = "http://localhost:5001"

@webapp.before_first_request
def set_cache_db_settings():
    set_cache_params(conf.max_capacity, conf.replacement_policy)

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
    global cache_host
    if request.method == 'POST':
        key = request.form.get('key')
        jsonReq={"keyReq":key}
        res= requests.post(cache_host + '/get', json=jsonReq)
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
                base64_image = write_image_base64(filename)
                jsonReq = {key:base64_image}
                res = requests.post(cache_host + '/put', json=jsonReq)
                return render_template('show_image.html', exists=True, filename=base64_image)
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
    keys = [] #will recieve keys from db
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
    global cache_host
    cache_params = get_cache_params()
    update_time = time.ctime(cache_params[1])
    capacity = cache_params[2]
    replacement_policy = cache_params[3]
    date = datetime.datetime.strptime(update_time, "%a %b %d %H:%M:%S %Y")
    date.strftime("YYYY/MM/DD HH:mm:ss (%Y%m%d %H:%M:%S)")

    if request.method == 'POST':

        if not request.form.get("clear_cache") == None:
            requests.post(cache_host + '/clear')
            return render_template('memcache_params.html', capacity=capacity, replacement_policy=replacement_policy, update_time=date, status="CLEAR")
        else:
            new_cap = request.form.get('capacity')
            if new_cap.isdigit():
                print("In here")
                new_policy = request.form.get('replacement_policy')
                new_time = set_cache_params(new_cap, new_policy)
                if not new_time == None:
                    new_time = datetime.datetime.strptime(time.ctime(new_time), "%a %b %d %H:%M:%S %Y")
                    new_time.strftime("YYYY/MM/DD HH:mm:ss (%Y%m%d %H:%M:%S)")
                    resp = requests.post(cache_host + '/refreshConfiguration')
                    if resp.json() == 'OK':
                        return render_template('memcache_params.html', capacity=new_cap, replacement_policy=new_policy, update_time=new_time, status="FALSE")
            # On error, reset to old params
            return render_template('memcache_params.html', capacity=capacity, replacement_policy=replacement_policy, update_time=date, status="TRUE")
    return render_template('memcache_params.html', capacity=capacity, replacement_policy=replacement_policy, update_time=date)


error_message={"success":"false" , "error":{"code"}}
@webapp.route('/api/list_keys', methods = ['POST'])
def list_keys():
    try:
        cnx = get_db()
        cursor = cnx.cursor()
        query = "SELECT image_key FROM image_table"
        cursor.execute(query)
        keys = [] #will recieve keys from db
        for key in cursor:
            keys.append(key[0])
        cnx.close()
        data_out={"success":"true" , "keys":keys}
        return jsonify(data_out)
    except Exception as e:
        error_message={"success":"false" , "error":{"code":e.code, "message":e.message}}
        return(jsonify(error_message))

@webapp.route('/api/key/<key_value>', methods = ['POST'])
def one_key(key_value):
    try:
        #str(request.url_rule).strip().split('/')[-1]
        jsonReq={"keyReq":key_value}
        res= requests.post('http://localhost:5001/get', json=jsonReq)
        if(res.text=='Unknown key'):#res.text is the file path of the image from the memcache
            #get from db and update memcache
            cnx = get_db()
            cursor = cnx.cursor(buffered=True)
            query = "SELECT image_tag FROM image_table where image_key= %s"
            cursor.execute(query, (key_value,))
            if(cursor._rowcount):# if key exists in db
                image_tag=str(cursor.fetchone()[0]) #cursor[0] is the imagetag recieved from the db
                #close the db connection
                cnx.close()

                #put into memcache
                filename=image_tag
                base64_image = write_image_base64(filename)
                jsonReq = {key:base64_image}
                res = requests.post(cache_host + '/put', json=jsonReq)
                data_out={"success":"true" , "content":base64_image}
                return jsonify(data_out)
                #output json with db values
            else:#the key is not found in the db
                #TODO what should we output if key is not in DB???

                data_out={"success":"false" , "error":{"code": "406 Not Acceptable", "message":"specified key does not not exist"}}
                return jsonify(data_out)

        else:
            data_out={"success":"true" , "content":res.text}
            return jsonify(data_out)

    except Exception as e:
        error_message={"success":"false" , "error":{"code":e.code, "message":e.message}}
        return(jsonify(error_message))


@webapp.route('/api/upload', methods = ['POST'])
def upload():
    try:
        key = request.form.get('key')
        status = save_image(request, key)
        if status=="INVALID" or status== "FAILURE":
            data_out={"success":"false" , "error":{"code": "500 Internal Server Error", "message":"Failed to upload image"}}
            return jsonify(data_out)

        data_out={"success":"true"}
        return jsonify(data_out)

    except Exception as e:
        error_message={"success":"false" , "error":{"code":e.code, "message":e.message}}
        return(jsonify(error_message))

