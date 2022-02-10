from memcache_app import memcache, webapp
from flask import request
import json

@webapp.route('/put', methods = ['POST'])
def put():
    req_json = request.get_json(force=True) 
    key, value = list(req_json.items())[0]
    
    if key in memcache:
        # Remove old key from dictionary
        memcache.pop(key)

    # TODO: Add the memory replacement logic here
    memcache[key] = value

    return get_response()

@webapp.route('/clear', methods = ['GET', 'POST'])
def clear():
    memcache.clear()
    return get_response()


def get_response():
    response = webapp.response_class(
        response=json.dumps("OK"),
        status=200,
        mimetype='application/json'
    )

    return response