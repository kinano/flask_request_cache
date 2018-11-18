from helpers import request_cache

@request_cache.cache_func()
def get_by_id(id):
    for i in range(10000000):
        continue
    return {
        "id": id,
        "name": "Kinan",
        "email": "k@theSilentCamera.com"
    }