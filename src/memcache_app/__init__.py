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
import mysql.connector
from datetime import datetime
event = threading.Event()
lock = threading.Lock()

def background_job(db_config, memcache_obj):
    """ Background Job to update the statistics of memcache 
     Parameters:
            db_config: dictionary containing the database configuration
            memcache_obj: the global memcache object, whose statistics are
                            being stored in cache_stats tables

        Return:
            string -> "success"
    This method runs on a different thread and this is how it doesn't interfere with 
    webapplication requests.

    """
    print("Background Job Start")

    while True:
        event.wait(5)
        query_add = '''INSERT INTO cache_stats (created_at, cache_size, key_count, 
                            request_count, miss_count) VALUES (%s,%s,%s,%s,%s)'''
        cnx = mysql.connector.connect(user=db_config['user'], password=db_config['password'], 
                                        host=db_config['host'], database=db_config['database'])
        cnx.autocommit = False
        cursor = cnx.cursor(buffered=True)
        
        with lock:
            if threading.active_count() > 2 :
                cursor.execute(query_add, (datetime.now(),memcache_obj.current_size, memcache_obj.currsize, 
                                memcache_obj.access_count, memcache_obj.miss))
                cnx.commit()
        cnx.close()
        
    print("Exit Background Job")
    return "success" 

print("main thread: native_id:", threading.get_native_id())
threading.Thread(target=background_job, args= (db_config,memcache_obj)).start()
