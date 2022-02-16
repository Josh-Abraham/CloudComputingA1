import os, requests
from app.db_connection import get_db

def get_cache_params():
    try:
        cnx = get_db()
        cursor = cnx.cursor(buffered = True)
        query = ''' SELECT MAX(param_key) FROM cache_params'''
        cursor.execute(query)
        for elem in cursor:
            print(elem)
        cnx.commit()

        return "OK"
    except:
        return "FAILURE"

def set_cache_params(epoch_date, max_capacity, replacement_method):
    try:
        cnx = get_db()
        cursor = cnx.cursor(buffered = True)
        query_add = ''' INSERT INTO cache_properties (epoch_date, max_capacity, replacement_method) VALUES (%d,%d, %s)'''
        cursor.execute(query_add,(epoch_date, max_capacity, replacement_method))
        
        for elem in cursor:
            print(elem)
        cnx.commit()

        return "OK"
    except:
        return "FAILURE"