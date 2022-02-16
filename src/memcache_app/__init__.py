from flask import Flask
from memcache_app import memcache
from app.config import memcache_params
from memcache_app import memcache_rest
from memcache_app.cache_utils import set_cache_params

webapp = Flask(__name__)
global memcache_obj
base_cache = memcache.get_cache(memcache_params['max_capacity'])
memcache_obj = base_cache(memcache_params['replacement_policy'])

# Set cache params into DB on initializationg
set_cache_params(memcache_params['epoch_date'], memcache_params['max_capacity'], memcache_params['replacement_policy'])

