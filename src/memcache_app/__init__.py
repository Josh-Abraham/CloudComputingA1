from flask import Flask
from memcache_app import memcache
from cachetools import LRUCache, RRCache
import os

webapp = Flask(__name__)
global memcache_obj
base_cache = memcache.get_cache(LRUCache)
memcache_obj = base_cache(2)


from memcache_app import memcache_rest


