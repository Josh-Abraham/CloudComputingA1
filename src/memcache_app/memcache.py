from cachetools import LRUCache, RRCache
import random
import time
from memcache_app import constants
from threading import Lock

lock = Lock()

#[todo] logging
def get_cache(cache):
    class MemCache(cache):

        def __init__(self, size):
            if (cache == LRUCache):
                super().__init__(maxsize = self.MB_to_Bytes(size), getsizeof= None)
                self.replace_policy = constants.LRU
            else:
                super().__init__(maxsize = self.MB_to_Bytes(size), choice = random.choice, getsizeof= None)
                self.replacement_policy = constants.RR
            self.maximum_size = self.MB_to_Bytes(size)
            self.current_size = 0
            self.hit = 0
            self.miss = 0
            self.access_count = 0
        
        def pushitem(self, key, value):
            response = self.__setitem__(key, value)
            self.access_count += 1
            return response

        def updateitem(self, key, new_value):
            if(self.__getitem__(key)):
                current_value = self._Cache__data[key]
                self.current_size -= len(current_value)
                self._Cache__data[key] = new_value
                self.current_size += len(new_value)
                return True
            return False

        def popitem(self):
            if (self.currsize > 0):
                response = super().popitem()
                if(response != None):
                    (key, value) = response
                    self.current_size -= len(value.encode('utf-8'))
                    return(key, value)
            return None

        def getitem(self, key):
            response = self.__getitem__(key)
            if(response == None):
                self.miss += 1
            else:
                # print(response)
                self.hit += 1
            self.access_count += 1
            return response

        def invalidate(self, key):
            response = self.__getitem__(key)
            if(response != None):
                (_, value) = response
                super().pop(key)
                self.current_size -= len(value.encode('utf-8'))
                return "OK"
            return None
        
        def clear_cache(self):
            with lock:
                while self.currsize > 0:
                    self.popitem()

        def refreshConfiguration(self, size, replacement_policy):
            self.replace_policy = replacement_policy
            self.resized_cache(size)
            return self.__copy__(size)
            
        def __copy__(self, size):
            print(self.replace_policy)
            if (self.replace_policy == constants.LRU):
                base_cache = get_cache(LRUCache)
            else:
                base_cache = get_cache(RRCache)
            new_memcache = base_cache(size)
            new_memcache.maximum_size = self.maximum_size
            new_memcache.current_size = self.current_size
            new_memcache.replace_policy = self.replace_policy
            new_memcache.hit = self.hit
            new_memcache.miss = self.miss
            data = self._Cache__data
            for key,value in data.items():
                new_memcache.pushitem(key, value)
            return new_memcache

        def __missing__(self, key): #[todo] what else can be returned?
            return None

        def __getitem__(self, key):
            response = super().__getitem__(key)
            return response

        def __setitem__(self, key, value):
            if(self.current_size + len(value.encode('utf-8')) >= self.maximum_size):
                while(self.current_size + len(value.encode('utf-8'))>= self.maximum_size and self.currsize > 0):
                    self.popitem()
            print(self.maximum_size)
            print(self.current_size)
            print(len(value.encode('utf-8')))
            if(key != None and value != None and (self.current_size + len(value.encode('utf-8'))) <= self.maximum_size):
                super().__setitem__(key, value)
                self.current_size +=  len(value.encode('utf-8'))
                return True
            return False

        def resized_cache(self, new_size):
            self.maximum_size = self.MB_to_Bytes(new_size)
            if(self.MB_to_Bytes(new_size) < self.maxsize):
                while(self.current_size > self.maximum_size and self.currsize > 0):
                    self.popitem()
            return self.__copy__(new_size)

        def MB_to_Bytes(self, size):
            return(size*pow(2,20))

        def KB_to_Bytes(self, size):
            return(size*pow(2,10))
    return MemCache
