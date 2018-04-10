
# from werkzeug.contrib.cache import SimpleCache
#
# CACHE_TIMEOUT = 300
#
# cache = SimpleCache()
#
# class cached(object):
#
#     def __init__(self, timeout=None):
#         self.timeout = timeout or CACHE_TIMEOUT
#
#     def __call__(self, f):
#         def decorator(*args, **kwargs):
#             response = cache.get(request.path)
#             if response is None:
#                 response = f(*args, **kwargs)
#                 cache.set(request.path, response, self.timeout)
#             return response
#         return decorator
#
#     @app.before_request
#     def return_cached():
#         # if GET and POST not empty
#         if not request.values:
#             response = cache.get(request.path)
#             if response:
#                 return response
#
#     @app.after_request
#     def cache_response(response):
#         if not request.values:
#             cache.set(request.path, response, CACHE_TIMEOUT)
#         return response
from werkzeug.contrib.cache import GAEMemcachedCache
cache = GAEMemcachedCache()