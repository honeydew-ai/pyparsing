# # Import required components for working with Python objects
# from cpython.dict cimport PyDict_GetItem, PyDict_SetItem, PyDict_Clear

# cdef class _CacheType:
#     """Optimized version of dict for caching purposes."""

#     # Internal cache storage - same as Python dict
#     cdef dict cache

#     def __cinit__(self):
#         """Constructor for the class"""
#         self.cache = {}

#     def get(self, key, default=None):
#         """Optimized version of get"""
#         # Use PyDict_GetItem directly
#         cdef void* result = PyDict_GetItem(self.cache, key)
#         if result != NULL:  # C-level pointer comparison
#             return <object>result  # Cast to Python object
#         return default

#     def set(self, key, value):
#         """Optimized version of set"""
#         PyDict_SetItem(self.cache, key, value)

#     def clear(self):
#         """Optimized version of clear"""
#         # PyDict_Clear(self.cache)


# from cpython.dict cimport PyDict_GetItem, PyDict_SetItem

# cdef class _CacheType:
#     """Optimized version of dict for caching purposes."""

#     cdef dict cache

#     def __cinit__(self):
#         self.cache = {}

#     def get(self, key, default=None):
#         cdef void* result = PyDict_GetItem(self.cache, key)
#         if result != NULL:
#             return <object>result
#         return default

#     def set(self, key, value):
#         PyDict_SetItem(self.cache, key, value)

#     def clear(self):
#         """Optimized version of clear by reinitializing the dictionary."""
#         self.cache = {}  # Faster reset of the cache