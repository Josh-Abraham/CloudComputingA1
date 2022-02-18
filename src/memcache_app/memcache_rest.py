from memcache_app import memcache_obj, webapp
from app.cache_utils import get_cache_params
from flask import request
import json

@webapp.route('/put', methods = ['POST'])
def put():
    """ Put request to add key to memecache

        Parameters:
            request (Request): key and base64 image

        Return:
            response (JSON): "OK" or "ERROR"
    """
    req_json = request.get_json(force=True)
    key, value = list(req_json.items())[0]
    memcache_obj.pushitem(key, value)
    return get_response(True)

@webapp.route('/clear', methods = ['GET', 'POST'])
def clear():
    """ Clear cache values

        Return:
            response (JSON): "OK"
    """
    memcache_obj.clear_cache()
    return get_response(True)

@webapp.route('/get', methods = ['POST'])
def get():
    """ Get key from cache

        Parameters:
            request (Request): key

        Return:
            response: "OK" or "Unknown Key"
    """
    req_json = request.get_json(force=True)
    key = req_json["keyReq"]
    response=memcache_obj.getitem(key)
    if response==None:
        return "Unknown key"
        #check db and put into memcache
    else:
        return response

@webapp.route('/test/<key>/<value>')
def test(key,value):
    response=memcache_obj.pushitem(key,value)
    return get_response(response)

@webapp.route('/invalidate', methods = ['POST'])
def invalidate():
    """ Invalidate key in cache

        Parameters:
            request (Request): key

        Return:
            response (JSON): "OK"
    """
    req_json = request.get_json(force=True)
    memcache_obj.invalidate(req_json["key"])
    return get_response(True)

@webapp.route('/refreshConfiguration', methods = ['POST'])
def refresh_configs():
    """ Refresh configuration with new parameters

        Parameters:
            request (Request): Capacity and replacement policy

        Return:
            response (JSON): "OK"
    """
    cache_params = get_cache_params()
    if not cache_params == None:
        capacity = cache_params[2]
        replacement_policy = cache_params[3]
        memcache_obj.refreshConfiguration(capacity, replacement_policy)
        return get_response(True)
    return None

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
