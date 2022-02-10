from memcache import get_cache
from cachetools import LRUCache, RRCache
import random
import time
import constants
#script /testing

start = time.time()
base_cache = get_cache(LRUCache)
memcache = base_cache(2)

print("size of memcache")
print(memcache.__sizeof__())

i = 0
while(i < 2*pow(2,8)):
    memcache.pushitem(i, "value " )
    # print("input: ", 2*pow(2,20) - i)
    i += 1

i = 0
while(i < 2*pow(2,3)):
    memcache.updateitem(i, "key value ")
    i += 1

i = 0
while(i < pow(2,2)):
    # print("Popped Item: ", i)
    response = memcache.popitem()
    # memcache.getitem(key)
    i += 1

# print("currsize is: ", memcache.currsize)

i = 0
while(i < 2*pow(2,8)):
    # print("get item: ", i)
    memcache.getitem(i)
    i += 1


print("currsize is: ", memcache.currsize)
print("current_size is: ", memcache.current_size)

# resizing the cache 
new_memcache = memcache.resized_cache(3)
memcache = new_memcache
print("after resizing")
# print(memcache)
print("maxsize after resize", memcache.maxsize)
print("currsize after resize", memcache.currsize)
print("hit is ", memcache.hit)
print("miss is ", memcache.miss)
print("hit rate is ", memcache.hit/(memcache.hit + memcache.miss))
stop = time.time()

print("time taken is: ", stop - start)

# global new_memcache

# new_memcache = memcache.resized_cache(1)
# memcache.clear()
# memcache = new_memcache
# print("hit is ", memcache.hit)
# print("miss is ", memcache.miss)
# print("hit rate is ", memcache.hit/(memcache.hit + memcache.miss))

# response = memcache.popitem()
# print(response)

# print(memcache.__getitem__(1))
# print(memcache.__getitem__(2))
# print(memcache.__getitem__(4))
# print(memcache.__getitem__(2000))
# print(memcache.__delitem__(1))
# print(memcache.__getitem__(2))
# print("hit", memcache.hit)
# print("miss", memcache.miss)

# # resize
# response = memcache.resize(3)
# if(response == False):
#     new_memcache = memcache.__copy__(3)
# memcache.clear()
# memcache = new_memcache
# print("after resizing")
# print("hit", memcache.hit)
# print("miss", memcache.miss)

#     print(type(memcache.keys()))
#     new_memcache = MemRRCache(3)
#     for key in memcache.keys():
#         new_memcache.additem(key, list(memcache.get(key)))
#     memcache.clear()
#     memcache = new_memcache

# print("after resizing")
# print("maxsize before resize", memcache.maxsize)
# print("currsize after resize", memcache.currsize)
# print("clear cache")
# new_memcache.clear()
# memcache.clear()
