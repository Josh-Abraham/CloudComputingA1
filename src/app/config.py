import time
from memcache_app.constants import LRU

db_config = {'user': 'root', 
             'password': 'ece1779pass',
             'host': '127.0.0.1',
             'database': 'ImageStore'}

memcache_params = {
    'epoch_date': time.time(), 
    'max_capacity': 100,
    'replacement_policy': LRU
}