from flask import Flask
import os

global memcache

webapp = Flask(__name__)
memcache = {}


from memcache_app import mem_cache_utils


