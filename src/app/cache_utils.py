from app.db_connection import get_db
import time

def get_cache_params():
    try:
        cnx = get_db()
        cursor = cnx.cursor(buffered = True)
        query = '''SELECT * FROM cache_properties WHERE param_key = (SELECT MAX(param_key) FROM cache_properties LIMIT 1)'''
        cursor.execute(query)
        if(cursor._rowcount):# if key exists in db
            cache_params=cursor.fetchone()
            return cache_params
        return None
    except:
        return "ERROR"

def set_cache_params(max_capacity, replacement_method):
    try:
        cnx = get_db()
        epoch_date = time.time() - 18000
        cursor = cnx.cursor(buffered = True)
        print(int(epoch_date), max_capacity, replacement_method)
        query_add = ''' INSERT INTO cache_properties (epoch_date, max_capacity, replacement_method) VALUES (%s,%s,%s)'''
        cursor.execute(query_add,(epoch_date,max_capacity, replacement_method))
        cnx.commit()
        
        return epoch_date
    except:
        return "FAILURE"