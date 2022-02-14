from memcache_app import memcache_obj, webapp
from flask import request
import json

@webapp.route('/put', methods = ['POST'])
def put():
    req_json = request.get_json(force=True) 
    key, value = list(req_json.items())[0]
    response = None
    if memcache_obj.getitem(key) != None:
        # Replace item if it exists
        response = memcache_obj.updateitem(key, value)
    else:
        response = memcache_obj.pushitem(key, value)
    print(response)
    return get_response()

@webapp.route('/CLEAR', methods = ['GET', 'POST'])
def clear():
    memcache_obj.clear_cache()
    return get_response()


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