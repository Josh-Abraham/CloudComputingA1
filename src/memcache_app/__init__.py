from flask import Flask
from memcache_app import memcache
from cachetools import LRUCache
import requests
from app.db_connection import get_db
import os
from app.config import db_config
webapp = Flask(__name__)
global memcache_obj

base_cache = memcache.get_cache(LRUCache)
memcache_obj = base_cache(2)

from memcache_app import memcache_rest
import threading
import time
import mysql.connector
from datetime import datetime

def background_job(db_config):
    print("Background Job Start")

    while True:
        time.sleep(5)
        query_add = '''INSERT INTO cache_stats (created_at, cache_size, key_count, request_count, miss_count) VALUES (%s,%s,%s,%s,%s)'''
        cnx = mysql.connector.connect(user=db_config['user'], password=db_config['password'], host=db_config['host'], database=db_config['database'])
        cnx.autocommit = False
        cursor = cnx.cursor(buffered=True)

        if not threading.currentThread().isDaemon():
            cursor.execute(query_add, (datetime.now(),memcache_obj.current_size, memcache_obj.access_count, memcache_obj.hit + memcache_obj.miss, memcache_obj.miss))
            cnx.commit()
        
        cnx.close()
        print("Inside background job - threadname: ", threading.currentThread())
        print(threading.enumerate())
        
    print("Exit Background Job")
    return "success" 

threading.Thread(target=background_job, args= (db_config,)).start()
