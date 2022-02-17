from memcache_app import memcache_obj, webapp
from flask import request
import json

@webapp.route('/put', methods = ['POST'])
def put():
    req_json = request.get_json(force=True)
    key, value = list(req_json.items())[0]
    memcache_obj.pushitem(key, value)
    return get_response()

@webapp.route('/clear', methods = ['GET', 'POST'])
def clear():
    memcache_obj.clear_cache()
    return get_response(True)

@webapp.route('/get', methods = ['POST'])
def get():
    req_json = request.get_json(force=True)
    key = req_json["keyReq"]
    response=memcache_obj.getitem(key)
    if response==None:
        print (response)
        return "Unknown key"
    else:
        print (response)
        return response

@webapp.route('/test/<key>/<value>')
def test(key,value):
    response=memcache_obj.pushitem(key,value)
    return get_response(response)

@webapp.route('/invalidate', methods = ['POST'])
def invalidate():
    req_json = request.get_json(force=True)
    memcache_obj.invalidate(req_json["key"])
    return get_response(True)


def get_response(input=False):
    if input:
        response = webapp.response_class(
            response=json.dumps("OK"),
            status=200,
            mimetype='application/json'
        )
    else:
        response = webapp.response_class(
            response=json.dumps("Bad Request"),
            status=400,
            mimetype='application/json'
        )

    return response

def get_response_no_key():
    response = webapp.response_class(
        response=json.dumps("Unknown key"),
        status=400,
        mimetype='application/json'
    )

    return response

def put_response():
    response = webapp.response_class(
        response=json.dumps("OK"),
        status=200,
        mimetype='application/json'
    )

    return response
